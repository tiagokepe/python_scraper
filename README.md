# Python Scraper Framework
This project provides an initial proposal for a scraper framework to retrieve profile information from https://upwork.com.

# Interface
These are the supported API resources:
* Log in
* Load user profile
* Save user profile
* Log out

# Requirements
All required libraries with the versions used in the development environment are defined in the file `requirements.txt`.

Therefore, it only requires to run: `sudo pip3 install -r requirements.txt`

# Docker Container
We provide a docker image implementation with the Docker Compose facilities.

Run the following command inside the project's directory:

* `$: docker-compose up python_scraper`

To access the container:
* `$: docker run -it python_scraper`


# Main scraper
The [main_scraper](https://github.com/tiagokepe/python_scraper/blob/main/src/main_scraper.py) module reads a credential JSON file (ex: [credentials.json](https://github.com/tiagokepe/python_scraper/blob/main/credentials.json)). For each provided credential, it retrieves and saves the user profile information in the **user_profiles** directory.

To run the **main_scraper**, only execute:

* `$: python3 src/main_scraper.py`

The first version of this module uses the **SeleniumScraper**, but with our Scraper Interface, described below, it's possible to provide many scrapers as needed.

P.S.: A valuable feature would be to implement a fallback functionality. I already have an idea for that, which needs more time.

## Scraper Interface
New scrapers must implement the [AbstractScraper](https://github.com/tiagokepe/python_scraper/blob/main/src/abstract_scraper.py). This interface design aims to enable the easy implementation of new scrapers from different libraries, especially for fallback purposes.

A full implementation of this interface is presented in [SeleniumScraper](https://github.com/tiagokepe/python_scraper/blob/main/src/selenium_scraper.py), using the **Selenium** library to mimic the browser and then to overcome the Cloudflare firewall.

For fallback and/or performance improvements, I've started to implement a new scraper using the **cloudscraper** library, and it's partial with only the **log_in** and with code snippet in [CloudBasedScraper](https://github.com/tiagokepe/python_scraper/blob/main/src/cloud_based_scraper.py).

The new scrapers must be helpful in case of SeleniumScraper failure. We can use other scrapers as a fallback.

# Github actions for CI/CD
For now, there are three implemented actions for CI/CD workflows:
* `CodeQuality.yml`: runs many format checks
* `Docker.yml`: builds the docker image
* `Main.yml`: installs the requirements and runs the unit test scripts

The **Main** workflow generates the  [log-report artifact](https://github.com/tiagokepe/python_scraper/actions/runs/4574732726#:~:text=exit%20code%201.-,Artifacts,-Produced%20during%20runtime) for troubleshooting.

# Features
We provide some extra features, especially for troubleshooting, handling possible errors, and retrying if the scanning fails.

## LogScraper
This class provides log functionalities for the scrapers.

## ConfigureScraper
This class defines and handles the configuration knobs for the framework, such as:
* `retry_attempts`: number of retry attempts
* `log_file`: path to the log file
* `screenshot_dir`: path for the screenshot directory used by the SeleniumScraper

The configuration file must be named **.scraper.ini** and located in the project's root directory. An example would be:
```
[scraper]
num_retry_attempts = 2
log_file = log/scraper.log
screenshot_dir = log/screenshots/
```

## StateEnum
This enum class defines five scraper states:
```
STATELESS = 0
INITIALIZED = 1
LOGINTO = 2
LOADED_PROFILE = 3
LOGOUT = 4
```
Those states are valuable for logging and mainly while writing the test units.

## Models
This module is based on the **pydantic** library to provide two main models: `Credential` and `UserProfile`.
* `Credential`: this model class defines the user credential information.
* `UserProfile`: this model class holds all valuable user information scanned from the profile page.

## Tests
We use the **pytest** library to implement unit tests for the scrapers. All the test cases should be placed inside the `tests` directory.

To run the test cases: `pytest tests`

## Checks
We provide many checks using the **pre-commit** library with the hooks:
* black
* flake8
* isort
* pylint
* mypy

To run the checks:
* `$: pre-commit install`
* `$: pre-commit run -a`
