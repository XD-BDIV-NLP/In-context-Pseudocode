import json
import os
import argparse
import io
import sys
import multiprocessing


def load_problems(problems_file_path):
    """Loads HumanEval+ problems from a specified JSON file."""
    problems = {}

    with open(problems_file_path, 'r', encoding='utf-8') as f:
        all_problems_data = json.load(f)

    if isinstance(all_problems_data, list):
        for problem_data in all_problems_data:
            if 'task_id' in problem_data:
                problems[problem_data['task_id']] = problem_data
            else:
                print(f"Warning: Problem data missing 'task_id': {problem_data}")

    elif isinstance(all_problems_data, dict):
        problems = all_problems_data

    else:
        raise ValueError(
            f"Unexpected format for problems data: {type(all_problems_data)}"
        )

    return problems


def load_solutions(solutions_file_path):
    """Loads generated solutions from a specified JSONL file."""
    solutions = {}

    with open(solutions_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            solution_data = json.loads(line.strip())

            if 'task_id' in solution_data and 'completion' in solution_data:
                solutions[solution_data['task_id']] = solution_data['completion']
            else:
                print(
                    f"Warning: Solution data missing 'task_id' or 'completion': {solution_data}"
                )

    return solutions


def _worker_exec(code_to_execute, return_dict):
    """在独立子进程中执行代码的 Worker 函数，防止主进程被大模型代码卡死"""
    exec_globals = {}

    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output

    try:
        # 执行危险/不可控代码
        exec(code_to_execute, exec_globals)
        return_dict['passed'] = True
        return_dict['details'] = "All tests passed."
    except Exception as e:
        return_dict['passed'] = False
        return_dict['details'] = f"Test failed: {type(e).__name__} - {e}"
    finally:
        sys.stdout = old_stdout
        captured_output = redirected_output.getvalue()
        if captured_output:
            return_dict['details'] += f"\nCaptured Output:\n{captured_output}"


def execute_solution(
        problem,
        solution_code,
        include_prompt=True,
        save_file=None,
        timeout=10.0
):
    """Executes a solution against a problem's test cases using isolated processes."""

    print(f"Executing solution for problem {problem['task_id']}...")

    # 使用双换行防止代码拼接时缩进混淆
    test_setup = f"\n\ncheck({problem['entry_point']})\n"

    if include_prompt:
        code_to_execute = (
                problem['prompt']
                + "\n"
                + solution_code
                + "\n\n"
                + problem['test']
                + test_setup
        )
    else:
        code_to_execute = (
                solution_code
                + "\n\n"
                + problem['test']
                + test_setup
        )

    # 保存拼装后的代码，方便出错时人工 debug
    if save_file is not None:
        os.makedirs(os.path.dirname(save_file), exist_ok=True)
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(code_to_execute)

    # 跨进程共享结果字典
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    return_dict['passed'] = False
    return_dict['details'] = "Execution failed due to unknown error or abrupt crash."

    # 启动子进程执行测试
    p = multiprocessing.Process(target=_worker_exec, args=(code_to_execute, return_dict))
    p.start()

    # 等待设定的超时时间
    p.join(timeout)

    # 如果超时后子进程依然存活（比如陷入了 while True），则强制抹杀
    if p.is_alive():
        p.terminate()
        p.join()
        return_dict['passed'] = False
        return_dict[
            'details'] = f"Test failed: Execution Timed Out after {timeout} seconds (Infinite loop or too slow)."

    return {
        "task_id": problem['task_id'],
        "passed": return_dict['passed'],
        "details": return_dict['details']
    }


def evaluate(
        problems_file_path,
        solutions_file_path,
        save_path
):
    """Main evaluation function."""

    print(f"Loading problems from: {problems_file_path}")
    problems = load_problems(problems_file_path)
    print(f"Found {len(problems)} problems.")

    print(f"Loading generated solutions from: {solutions_file_path}")
    generated_solutions = load_solutions(solutions_file_path)
    print(f"Found {len(generated_solutions)} generated solutions.")

    gt_results = []
    generated_results = []

    generated_code_dir = os.path.join(save_path, "assembled_generated")
    gt_code_dir = os.path.join(save_path, "assembled_gt")

    os.makedirs(generated_code_dir, exist_ok=True)
    os.makedirs(gt_code_dir, exist_ok=True)

    for task_id, problem in problems.items():
        task_id_safe = task_id.replace("/", "_")

        # Evaluate Ground Truth
        # (由于标准 HumanEval 数据集 GT 不包含 def，此处 include_prompt=True)
        if 'canonical_solution' in problem:
            gt_solution_code = problem['canonical_solution']
            save_file_gt = os.path.join(gt_code_dir, f"{task_id_safe}_gt.py")

            gt_result = execute_solution(
                problem,
                gt_solution_code,
                include_prompt=True,
                save_file=save_file_gt
            )
            gt_results.append(gt_result)
        else:
            gt_results.append({
                "task_id": task_id,
                "passed": False,
                "details": "No ground truth solution found in problem definition"
            })

        # Evaluate Generated
        # (由于提取的数据已是完整纯 Python 代码，此处 include_prompt=False)
        if task_id in generated_solutions:
            generated_solution_code = generated_solutions[task_id]
            save_file_gen = os.path.join(generated_code_dir, f"{task_id_safe}_gen.py")

            gen_result = execute_solution(
                problem,
                generated_solution_code,
                include_prompt=False,
                save_file=save_file_gen
            )
            generated_results.append(gen_result)
        else:
            generated_results.append({
                "task_id": task_id,
                "passed": False,
                "details": "No generated solution found"
            })

    # 汇总计算 Ground Truth
    gt_passed_count = sum(1 for r in gt_results if r['passed'])
    gt_total_count = len(gt_results)

    print("\n--- Ground Truth Evaluation Summary ---")
    print(f"Total problems: {gt_total_count}")
    print(f"GT Solutions passed: {gt_passed_count}")
    print(f"GT Pass rate: {gt_passed_count / gt_total_count * 100 if gt_total_count > 0 else 0:.2f}%")

    # 汇总计算 Generated Solutions
    gen_passed_count = sum(1 for r in generated_results if r['passed'])
    gen_total_count = len(generated_results)

    print("\n--- Generated Solutions Evaluation Summary ---")
    print(f"Total problems: {gen_total_count}")
    print(f"Generated Solutions passed: {gen_passed_count}")
    print(f"Generated Pass rate: {gen_passed_count / gen_total_count * 100 if gen_total_count > 0 else 0:.2f}%")

    # 也可以在这里把最终的 passed 结果存一个汇总 json
    summary_file = os.path.join(save_path, "evaluation_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "gt_pass_rate": gt_passed_count / gt_total_count if gt_total_count > 0 else 0,
            "generated_pass_rate": gen_passed_count / gen_total_count if gen_total_count > 0 else 0,
            "gt_details": gt_results,
            "generated_details": generated_results
        }, f, indent=4)
        print(f"\nDetailed evaluation results saved to {summary_file}")

    return gt_results, generated_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HumanEval+ Evaluation Script")

    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--task", type=str, default="humaneval_plus")
    parser.add_argument("--dataset_path", type=str, required=True)
    parser.add_argument("--source_path", type=str, required=True)
    parser.add_argument("--save_path", type=str, default="./result/")
    parser.add_argument("--run_code", action="store_true")

    args = parser.parse_args()

    os.makedirs(args.save_path, exist_ok=True)

    print(f"\n--- Running HumanEval+ Evaluation for Model: {args.model_name}, Task: {args.task} ---")

    if args.run_code:
        gt_eval_results, generated_eval_results = evaluate(
            args.dataset_path,
            args.source_path,
            args.save_path
        )
        print("Evaluation complete.")
    else:
        print("Skipping code execution as --run_code flag is not set.")
