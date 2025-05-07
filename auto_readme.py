import toml
import xml.etree.ElementTree as ET
import inspect
from dead_band import apply_deadband


def get_python_version(pyproject_path="pyproject.toml"):
    pyproject = toml.load(pyproject_path)
    try:
        return pyproject["project"]["requires-python"]
    except KeyError:
        return (
            pyproject.get("tool", {})
            .get("poetry", {})
            .get("dependencies", {})
            .get("python", "N/A")
        )


def get_coverage_percentage(coverage_file="./htmlcov/cov.xml"):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        line_rate = float(root.attrib.get("line-rate", 0))
        return f"{round(line_rate * 100, 2)}%"
    except Exception:
        return "0%"


def generate_badges(python_version, coverage_percent):
    badges = {
        "Python Version": f"https://img.shields.io/badge/python-{python_version}-blue.svg",
        "Coverage": f"https://img.shields.io/badge/coverage-{coverage_percent.replace('%', '')}%25-brightgreen.svg",
        "License": "https://img.shields.io/badge/license-MIT-green.svg",  # Altere se necessário
    }
    return "\n".join([f"![{k}]({v})" for k, v in badges.items()])


def generate_readme():
    python_version = get_python_version()
    coverage_percent = get_coverage_percentage()

    badges = generate_badges(python_version, coverage_percent)
    signature = inspect.signature(apply_deadband)
    docstring = inspect.getdoc(apply_deadband)
    readme_content = f"""# 📦 dead_band

{badges}

A Python library leveraging Cython for the implementation of deadband algorithms and related techniques, with the objective of optimizing data throughput and minimizing unnecessary data processing.

## Installation
```bash
pip install dead_band
```

## Examples: Before and After Deadband Processing

### Raw Data (Before Deadband)
<img src="./resources/png/plot.png" width="auto" height="auto">

### Compressed Data (After Deadband)
<img src="./resources/png/compressed_plot.png" width="auto" height="auto">

## Usage

### Function apply_deadband
```python
apply_deadband {signature}

{docstring}
```

### Simple Usage
```python
import pandas as pd
from datetime import datetime
from dead_band import apply_deadband

# 1. Create sample data
data = [
    (10.0, datetime(2023,1,1,12,0), 1),
    (10.2, datetime(2023,1,1,12,5), 1),
    (10.5, datetime(2023,1,1,12,10), 2),  # Quality change
    (10.5, datetime(2023,1,1,12,15), 2),
    (10.8, datetime(2023,1,1,12,20), 2),  # Variation > deadband
    (10.8, datetime(2023,1,1,12,25), 2),
    (10.8, datetime(2023,1,1,12,30), 3)   # Quality change
]

# 2. Apply deadband filter
filtered_data = apply_deadband(
    series=data,
    deadband_value=0.3,          # 0.3 unit deadband
    max_time_interval=1800,      # Force record every 30 minutes
    min_time_interval=300,       # Minimum 5 minutes between records
    time_unit='s',               # Time unit in seconds
    deadband_type='abs',         # Absolute deadband
    save_on_quality_change=True  # Save when quality changes
)

# 3. Convert to DataFrames
original_df = pd.DataFrame(data, columns=['value', 'timestamp', 'quality'])
filtered_df = pd.DataFrame(filtered_data, columns=['value', 'timestamp', 'quality'])

print("Original:", len(original_df), "points")
print("Filtered:", len(filtered_df), "points")
```
#### Expected Output
```python
Original: 7 points
Filtered: 4 points
```

### Multiples pathnames Usage
```bash
import pandas as pd
from datetime import datetime
from dead_band import apply_deadband

# 1. Create sample data with two different pathnames
data = [
    # Pathname "TAG001"
    (15.0, datetime(2023,1,1,8,0), 1, "TAG001"),
    (15.1, datetime(2023,1,1,8,5), 1, "TAG001"),
    (15.4, datetime(2023,1,1,8,10), 1, "TAG001"),  # Variation > deadband
    (15.4, datetime(2023,1,1,8,15), 2, "TAG001"),  # Quality change
    (15.4, datetime(2023,1,1,8,20), 2, "TAG001"),
    
    # Pathname "TAG002"
    (22.0, datetime(2023,1,1,8,0), 1, "TAG002"),
    (22.3, datetime(2023,1,1,8,5), 1, "TAG002"),  # Variation > deadband
    (22.3, datetime(2023,1,1,8,10), 1, "TAG002"),
    (22.8, datetime(2023,1,1,8,15), 1, "TAG002"),  # Variation > deadband
    (22.8, datetime(2023,1,1,8,20), 2, "TAG002")   # Quality change
]

# 2. Convert to DataFrame
df = pd.DataFrame(data, columns=['value', 'timestamp', 'quality', 'pathname'])

# 3. Apply deadband for each pathname
results = []
for pathname, group in df.groupby('pathname'):
    # Prepare data in (value, timestamp, quality) format
    series_data = group[['value', 'timestamp', 'quality']].values.tolist()
    
    # Apply filter
    filtered = apply_deadband(
        series=series_data,
        deadband_value=0.2,
        max_time_interval=600,  # 10 minutes
        save_on_quality_change=True
    )
    
    # Add pathname back to results
    filtered_df = pd.DataFrame(filtered, columns=['value', 'timestamp', 'quality'])
    filtered_df['pathname'] = pathname
    results.append(filtered_df)

# 4. Combine all results
final_df = pd.concat(results, ignore_index=True)

print("Results by pathname:")
print(final_df.groupby('pathname').size())

# Optional: Quick visualization
print("Filtered data:")
print(final_df.sort_values(['pathname', 'timestamp']))
```
#### Expected Output
```bash
Results by pathname:
pathname
TAG001    3
TAG002    4
Filtered data:
   value           timestamp  quality pathname
0   15.0 2023-01-01 08:00:00        1    TAG001
1   15.4 2023-01-01 08:10:00        1    TAG001
2   15.4 2023-01-01 08:15:00        2    TAG001
3   22.0 2023-01-01 08:00:00        1    TAG002
4   22.3 2023-01-01 08:05:00        1    TAG002
5   22.8 2023-01-01 08:15:00        1    TAG002
6   22.8 2023-01-01 08:20:00        2    TAG002
```





"""
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)


if __name__ == "__main__":
    generate_readme()
