# In-context Pseudocode

This repository contains the implementation of an in-context pseudocode prompting framework for code generation.

The project uses prompt templates to construct model inputs, generates code through an inference script, and evaluates the generated programs based on their execution pass rate.

## Repository Structure

```text
In-context-Pseudocode/
├── dataset/
├── eval/
│   ├── inference.py
│   ├── evaluate.py
│   ├── prompt_template.py
│   └── utils.py
├── metrics/
├── result/
└── README.md
```

## Directory Description

### `dataset`

Stores the datasets used for code-generation experiments.

The datasets are loaded during inference and evaluation. The specific dataset format should be consistent with the data-loading logic implemented in the project.

### `eval`

Contains the main scripts for code generation and evaluation.

- `inference.py`  
  Runs model inference and generates code predictions.

- `evaluate.py`  
  Evaluates the generated code and calculates the execution pass rate.

- `prompt_template.py`  
  Loads and manages the prompt templates used for code generation.

- `utils.py`  
  Contains shared utility functions used by the inference and evaluation scripts.

### `metrics/`

Stores evaluation-related scripts, metric implementations, or auxiliary files used to calculate code-generation performance.

### `result/`

Stores generated code, prediction results, and evaluation outputs.

## Workflow

The overall experimental workflow is:

```text
Dataset preparation
        ↓
Prompt template loading
        ↓
Code generation with inference.py
        ↓
Generated results
        ↓
Code evaluation with evaluate.py
        ↓
Execution pass rate
```

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/XD-BDIV-NLP/In-context-Pseudocode.git
cd In-context-Pseudocode
```

### 2. Prepare the dataset

Place the required dataset files in the `dataset/` directory.

```text
dataset/
└── your_dataset_files
```

The dataset format and file paths should match the configuration or data-loading logic used in the source code.

### 3. Configure the prompt template

Prompt templates are defined or loaded in:

```text
eval/prompt_template.py
```

Modify or select the appropriate template before running code generation.

### 4. Generate code

Run the inference script from the project root directory:

```bash
python eval/inference.py
```

The script generates code predictions based on the selected dataset and prompt template.

Generated outputs should be saved in the `result/` directory or in the output path specified in the script.

### 5. Evaluate generated code

After code generation is complete, run:

```bash
python eval/evaluate.py
```

The evaluation script executes or verifies the generated programs and calculates their pass rate.

Make sure that the prediction path, test data path, and evaluation settings in `evaluate.py` correspond to the generated results.

## Evaluation Metric

The main evaluation metric is the code execution pass rate.

It measures the proportion of generated programs that successfully pass the corresponding test cases:

```text
Pass Rate = Number of Passed Programs / Total Number of Evaluated Programs
```

A generated program is considered correct when it passes the required test cases under the evaluation settings.

## Output

The `result/` directory is used to store experiment outputs, which may include:

- Generated code
- Model predictions
- Execution results
- Evaluation logs
- Pass-rate statistics

An example output structure is:

```text
result/
├── predictions
├── evaluation_results
└── logs
```

The actual filenames and formats depend on the output logic implemented in the scripts.

## Notes

- Run the scripts from the project root directory to avoid relative-path errors.
- Check dataset and output paths before starting an experiment.
- Ensure that generated code is evaluated in a controlled environment.
- Different prompt templates may produce different code-generation results.
- Keep prediction files and evaluation results from different experiments in separate directories.

## License

Please refer to the repository license for usage and distribution terms.

## Contact

For questions, bug reports, or suggestions, please open an issue in this repository.
