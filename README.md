# scaler-module-summary-automation


# Installation

```bash
$ pip install -r requirements.txt

# Install wkhtmltopdf:

## Debian/Ubuntu:
$ sudo apt-get install wkhtmltopdf

## macOS:
$ brew install homebrew/cask/wkhtmltopdf
```

# Usage
```python
# Usage: For single batch
report = Report(
    start_time="2023-05-12",
    end_time="2023-05-31",
    batch_name="DSML Feb23 Beginner Mon 2",
    academy_module="Beginner Python 1"
)
report.generate_report()

# Usage: For all batches within a module
report = Report(
    start_time="2023-05-12",
    end_time="2023-05-31",
    academy_module="Beginner Python 1"
)
report.generate_report()

# start_time and end_time are must arguments
```
