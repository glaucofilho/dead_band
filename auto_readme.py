import toml
import re
import xml.etree.ElementTree as ET

def get_python_version(pyproject_path="pyproject.toml"):
    pyproject = toml.load(pyproject_path)
    try:
        return pyproject["project"]["requires-python"]
    except KeyError:
        return pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {}).get("python", "N/A")

def get_coverage_percentage(coverage_file="./htmlcov/cov.xml"):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        line_rate = float(root.attrib.get("line-rate", 0))
        return f"{round(line_rate * 100, 2)}%"
    except Exception:
        return "0%"

def generate_badges(python_version, coverage_percent):
    version_clean = re.sub(r"[^\d\.]", "", python_version.split(",")[-1])
    badges = {
        "Python Version": f"https://img.shields.io/badge/python-{version_clean}-blue.svg",
        "Coverage": f"https://img.shields.io/badge/coverage-{coverage_percent.replace('%', '')}%25-brightgreen.svg",
        "License": "https://img.shields.io/badge/license-MIT-green.svg",  # Altere se necessário
        "Build": "https://img.shields.io/github/actions/workflow/status/USER/REPO/python-app.yml?branch=main"
    }
    return "\n".join([f"![{k}]({v})" for k, v in badges.items()])

def generate_readme():
    python_version = get_python_version()
    coverage_percent = get_coverage_percentage()

    badges = generate_badges(python_version, coverage_percent)

    readme_content = f"""# 📦 dead_band

{badges}

Descrição curta do seu projeto.

## 🚀 Requirements

- Python {python_version}

"""
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)
    print("README.md gerado com sucesso!")
if __name__ == "__main__":
    generate_readme()
