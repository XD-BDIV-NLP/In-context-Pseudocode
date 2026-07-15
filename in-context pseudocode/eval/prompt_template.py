PROMPT_WRAPPER = """You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.
@@ Instruction
{instruction}

@@ Response
{response}"""

COT_PROMPT_WRAPPER = """You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.
@@ Instruction
{instruction}

@@ Response
Let's think step by step.
{response}"""

PROMPT_WRAPPER_ONE_SHOT = """You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.
@@ Instruction
{instruction}

@@ Response
Let's think step by step.
{response}"""

PROMPT_WRAPPER_API = """
@@ Instruction
{instruction}
@@ Response
"""

Zeroshot_PROMPT="""
You are an exceptionally intelligent coding assistant. Your task is to solve programming problems.
{instruction}

"""

CoT_PROMPT="""
Please generate a Python function based on the requirement and step-by-step solution.

{example}

New Requirement:
{instruction}

Solution:

"""

P_PROMPT = """
### SYSTEM DIRECTIVE
You are an exceptionally intelligent coding assistant. Your task is to solve programming problems.
Read the problem carefully. You MUST format your response exactly as shown in the EXAMPLE below, containing strictly TWO sections:
1. ### PseudoCode (Brief, high-level structured pseudocode inside a ```pseudocode block)
2. ### Python Code (Executable python code inside a ```python block)
Do not output any additional greetings, explanations, or text outside these blocks.

=========================================
{example}
=========================================
### YOUR TASK
{instruction}

### RESPONSE
"""

C_PROMPT = """
### SYSTEM DIRECTIVE
You are an exceptionally intelligent coding assistant. Your task is to solve programming problems.
Read the problem carefully. You MUST format your response exactly as shown in the EXAMPLE below, you should generate code first, and then using PseudoCode to explain it.

=========================================
{example}
=========================================
### YOUR TASK
{instruction}

### RESPONSE
{response}
"""

