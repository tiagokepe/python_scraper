# Upwork Scraper Framework
This project provides an initial proposal for a scraper framework to retrieve profile information from https://upwork.com.

# Interface
These are the supported API resources:
* Log in
* Load user profile
* Save user profile
* Log out

# Requirements
All required libraries with the versions used in the development enviroment are defined in the file `requirements.txt`.

Therefore, it only requires to run: `sudo pip3 install -r requirements.txt`

# Docker Container
We provide a docker image implementation with the Docker Compose facilities. 

Run the following command inside the project's directory:

* `$: docker-compose up upwork_scraper`

To access the container:
* `$: docker run -it upwork_scraper`


# Main scraper
The [main_scraper](https://github.com/tiagokepe/upwork_scraper/blob/main/src/main_scraper.py) module read a credential json file (ex: [credentials.json](https://github.com/tiagokepe/upwork_scraper/blob/main/credentials.json)), for each provided credential it retrives and saves the user profile information in the **user_profiles** directory.

To run the **main_scraper** only execute: 

* `$: python3 src/main_scraper.py`

The first version of this module uses the **SeleniumScraper**, but with our Scraper Interface, described bellow, it's possible to provide many scrapers as needed.

P.S.: A valuable feature would be to implement a fallback functionality. I alraedy have an idea for that but I didn't have enough time.

## Scraper Interface
New scrapers must implement the [AbstractScraper](https://github.com/tiagokepe/upwork_scraper/blob/main/src/abstract_scraper.py). This interface design aims to enable the easy implementation of new scrapers from different libraries, specially for fallback purpose.

A full implementation of this interface is presented in [SeleniumScraper](https://github.com/tiagokepe/upwork_scraper/blob/main/src/selenium_scraper.py), using the **Selelenium** library to mimick the browser and then to overcome the Cloudfare firewall.

For fallback and/or performance improvements, I've started to implement a new scraper using **cloudscraper** library, it's partial with only the **log_in** and with code snippet in [CloudBasedScraper](https://github.com/tiagokepe/upwork_scraper/blob/main/src/cloud_based_scraper.py).

The new scrapers must be usefull in case of SeleniumScraper's failure, we can use other scrapers as fallback.


# Github actions for CI/CD
For now, there are two defined actions for CI/CD workflows:
* `CodeQuality.yml`: runs many format checks
* `Main.yml`: installs the requirements and runs the unit test scripts

The test script is not workindg on Github because of Cloudflare detection,  it is sending the captcha V2 challenge.
I believe that Cloudflare has the Github notebooks IPs in a blacklist, in someway.

![image](https://user-images.githubusercontent.com/403295/229088069-85924e5d-8b2d-42b9-bdb2-92aa1678c8c9.png)


# Features
We provide some extra features especially for troubleshooting, handling possible errors, retrying if the scanning fails.

## LogScraper
This class provides log functionalies for the scrapers.

## ConfigureScraper
This class define and handle the configuration knobs for the framework such as:
* `retry_attempts`: number of retry attempts
* `log_file`: path to the log file
* `screenshot_dir`: path for the screenshot directory used by the SeleniumScraper

The configuration file must be named **.scraper.ini** and located in the root directory of the project. An example would be:
```
[scraper]
num_retry_attempts = 2
log_file = log/scraper.log
screenshot_dir = log/screenshots/
```

## StateEnum
This is a enum class that defines five scraper states:
```
STATELESS = 0
INITIALIZED = 1
LOGINTO = 2
LOADED_PROFILE = 3
LOGOUT = 4
```
Those states are usefull for logging and specially while writing the test units.

## Models
This module is based on the **pydantic** library to provide two main models: `Credential` and `UserProfile`.
* `Credential`: this model class defines the user credential information used by the scrapers.
* `UserProfile`: this model class holds all valuable user information scanned from the profile page.

## Tests
We use the **pytest** library to implement unit tests for the scrapers, all the test cases should be placed inside the `tests` directory.

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
