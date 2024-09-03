## Logger Abstraction For Python

### Basic Python Project setup

- Create virtual environment
    - `python -m venv venv`
- Activate the venv created
    - `source venv/bin/activate`
- Install the Project dependencies listed in requirements.txt
    - `pip install -r requirements.txt`
    - To define a target where the dependencies will be fetched and kept
        - `pip install --no-deps --target=./deps -r requirements.txt`
- verify the installed packages
    - `pip list`

### About Logger configs

- **Configuration File:**
    - The user can provide their own configuration file by passing the config_file_path when initializing the logger.
    - If no file is provided, it defaults to log_config.json in the current directory.
    - Sample config file log_config.json , is provided in the package itself for reference.
    - Example: While initialising logger in code provide the log config path as below
        - `logger = Logger(config_file_path="path/to/custom_log_config.json")`
- **Environment Variables:**
    - Users can override specific configurations using environment variables like
        - LOG_LEVEL, LOG_DESTINATION, LOG_FILE_PATH, and LOG_FORMAT.
    -
        - **Supported Log file formats**
        - json
        - plain

- **Supported Destinations**
    - file
    - console
    -

### **Anonymizer Configs**

- **"anonymize_fields"** populate this field with the arguments that are explicitly passed to the logs , to annonymize
  them
    - EG: ["user_id", "email", "ssn"] it is an array of fields, all these arguments will be anonymized in the logs
- **"anonymize_patterns"** these are pattern (regex) that will be used to annonymize messages, it will be better to keep
  them low, or it can impact writes.
- Disabling anonymizer
    - set "use_anonymizer": false in log_config.json

### Example usage

- Initialising the logger with custom log config
    - `from abstract_logger.logger import Logger`
    - `logger = Logger(config_file_path="custom_log_config.json")`

- Using the logger:
    - `logger.log("info", "This is an info message", user="john_doe", action="login")`
    - `logger.log("error", "An error occurred", error_code=500, path="/api/resource")`

### Creating the logger as a package and making it reusable

- Add `__init__.py` which is a special file in Python that is used to mark a directory as a package.
    - When you include an __init__.py file in a directory, it indicates to Python that this directory should be treated
      as a package, allowing you to import modules from that directory.
- Create s setup.py file so that we can version and distribute it as a package
    - If your goal is to create a reusable Python package that can be shared with others, uploaded to PyPI, or installed
      via pip install my_package, you need a setup.py file.
    - This file allows you to define metadata, dependencies, and configurations that are required when others install
      your package.
- Build the package with below command
    - `python setup.py sdist bdist_wheel`