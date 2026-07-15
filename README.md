# In-context Pseudocode

Official implementation and evaluation code for **In-context Pseudocode**, a project exploring the use of pseudocode-enhanced prompts for in-context learning and natural language processing tasks.

## Overview

This repository contains scripts for constructing pseudocode-based prompts and evaluating language models under in-context learning settings.

The main components include:

* Prompt construction using natural language and pseudocode demonstrations
* Model inference
* Output processing
* Evaluation utilities
* Reproducible experiment configurations

## Repository Structure

```text
In-context-Pseudocode/
├── eval/
│   ├── inference.py          # Main inference script
│   ├── prompt_template.py    # Prompt and pseudocode templates
│   └── utils.py              # Utility functions
├── README.md
└── requirements.txt          # Python dependencies, if provided
```

The repository structure may be updated as additional datasets, models, and evaluation scripts are released.

## Requirements

The code is intended to run with Python 3.9 or later.

We recommend creating an isolated Conda environment:

```bash
conda create -n pseudocode python=3.9
conda activate pseudocode
```

Install the required packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not included, install the dependencies required by the imports in the source files.

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/XD-BDIV-NLP/In-context-Pseudocode.git
cd In-context-Pseudocode
```

### 2. Check the available arguments

```bash
python eval/inference.py --help
```

### 3. Run inference

```bash
python eval/inference.py
```

Model paths, dataset paths, prompt settings, output directories, and other experiment parameters should be configured according to the arguments defined in `eval/inference.py`.

## Prompt Templates

Prompt templates and pseudocode-based demonstrations are defined in:

```text
eval/prompt_template.py
```

This file can be modified to evaluate different prompting strategies, demonstration formats, and task instructions.

## Evaluation

Utility functions for data loading, output processing, and evaluation are provided in:

```text
eval/utils.py
```

Generated predictions and evaluation results should be stored in a separate output directory to avoid committing large experiment files to the repository.

## Reproducibility

For reproducible experiments, please record:

* Model name and version
* Dataset name and version
* Prompt template
* Number of in-context demonstrations
* Random seed
* Decoding parameters
* Software and hardware environment

## Citation

If you use this repository in your research, please cite the corresponding paper:

```bibtex
@article{incontextpseudocode,
  title   = {In-context Pseudocode},
  author  = {Author Names},
  journal = {Journal or Conference},
  year    = {2026}
}
```

The citation information will be updated after publication.

## Acknowledgements

We thank the developers and maintainers of the open-source models, datasets, and libraries used in this project.

## Contact

For questions or suggestions, please open an issue in this repository.
