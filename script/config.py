"""
Script to complete configuration of the environment
for a Machine Learning project.
Each selected option installs a limited number of
libraries for a specific purpose.
"""

import time
import subprocess
import questionary
from pathlib import Path


def py_version():
    pyv_path = Path(".python-version")
    with open(pyv_path, "r") as pyv_file:
        return pyv_file.readline().strip()


def add_pyright():
    pytoml_path = Path("pyproject.toml")
    with open(pytoml_path, "a") as py_toml:
        print('\n[tool.pyright]\nvenvPath = "."\nvenv = ".venv"', file=py_toml)


def install_packages(text: str, command: list):
    print(f"🔄 Installing packages for {text}", end="\r")
    time.sleep(1)
    if CHOICES_DICT[text] == 4:
        add_pyright()
    else:
        subprocess.check_call(command, stdout=subprocess.DEVNULL)
    print(f"✅\033[32m Installing packages for {text}\033[0m", end="\n")


CHOICES_DICT: dict = {
    "Machine Learning (sklearn, xgboost, catboost)": 0,
    "Statistics (sklearn, statsmodels, sktime, tensorflow-probability)": 1,
    "Deep Learning (mlx, pytorch, lightning, torchmetrics, torchvision, tensorboard)": 2,
    "Data Visualization (matplotlib, seaborn, plotly)": 3,
    "configuring Pyright in pyproject.toml": 4,
}


PYV = py_version()
CONFIG_TUPLE: tuple[list[str], list[str], list[str], list[str], list[str]] = (
    ["poetry", "add", "--group", "ml", "scikit-learn", "xgboost", "catboost"],
    [
        "poetry",
        "add",
        "--group",
        "stat",
        "scikit-learn",
        "statsmodels",
        "tensorflow-probability",
        "sktime",
        f"--python={PYV}",
    ],
    [
        "poetry",
        "add",
        "--group",
        "deepl",
        "mlx",
        "lightning",
        "torchmetrics",
        "torchvision",
        "tensorboard",
    ],
    ["poetry", "add", "--group", "viz", "matplotlib", "seaborn", "plotly"],
    [],
)


def main():
    configs = questionary.checkbox(
        message="Select which configuration you want to install:",
        choices=list(CHOICES_DICT.keys()),
    )

    answer = configs.ask()
    packages = [CONFIG_TUPLE[c] for c in [CHOICES_DICT[a] for a in answer]]

    for ans, pkg in zip(answer, packages):
        install_packages(ans, pkg)


if __name__ == "__main__":
    main()
