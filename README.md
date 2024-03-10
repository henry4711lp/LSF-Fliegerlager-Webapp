[![Deploy to Portainer with Self-Hosted Runner](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/Docker-Build.yml/badge.svg)](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/Docker-Build.yml) ![Security Test](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/codeql-analysis.yml/badge.svg) ![Deployment](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/Docker-Build.yml/badge.svg) ![Sonarqube](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/sonarqube-scanner.yml/badge.svg) ![Tests](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/test_on_push.yml/badge.svg)
# LSF-Fliegerlager-Webapp

This app is to replace a handwritten list for "bought" drinks, dinners and accomodation days.  
The purpose of this webapp is to decrease the workload of the club youth management in the accounting process of the flying camp and to prevent the loss of the handwritten lists.

Latest version: **V0.1 Alpha**
Latest Main Branch running on: https://lsf-flilaapp.sellerbeckcloud.de/

## Authors

- [Jan Sellerbeck](https://www.github.com/henry4711lp)
- [Robin Busch](https://www.github.com/rbn-de)


## Data Privacy
- No storage of data of people who are not affected
- "testruns" against the "Vereinsflieger" API only via hardware from [Jan Sellerbeck](https://www.github.com/henry4711lp)
- No release of API key to anyone other than [Jan Sellerbeck](https://www.github.com/henry4711lp)
- No client side processing of the VF API or the DB
- No public network connection, separated network area, only accessible with VPN

## Roadmap

- [X]  Datenbank aufsetzen
- [X]  Vereinsflieger API implemented
- [X]  bill function implemented
- [X]  export function implemented
- [X]  Design created
- [X]  drink function implemented
- [ ]  Dinner function implemented
- [X]  Day function implemented
- [ ]  Open issues closed
------------------------------------
- [ ] **V0.1 Alpha release**
------------------------------------
- [ ] UI user tests
- [ ] Data Privacy inspection
------------------------------------
- [ ] **V0.1 Beta release**
------------------------------------

## Tech Stack

**Client:** Android Browser, HTML, CSS, JavaScript

**Server:** mySQL, phpMyAdmin, Python, Docker

**Python:** Flask, mysql, mysql-connector-python, PyYAML, requests, tabulate, setuptools, getConfig, Werkzeug,
            flask_httpauth, XlsxWriter, APScheduler

**CI/CD:** Github Actions, Sonarqube, Docker, Docker-Compose, Quodana, CodeQL, Ubuntu, Github Runner



## Run Locally
-  Clone the project
-  Install the requirements
-  Install XAMPP or another mysql server and add it to the config file
-  Start the mysql server
-  Start the phpmyadmin server
-  Create a user and add it to the config file
-  Create a database and add it to the config file
-  Import the tables from the sql file
-  Run the main.py

## Screenshots
![login_page.png](Screenshots%2Flogin_page.png)
![homepage.png](Screenshots%2Fhomepage.png)
![drinks.png](Screenshots%2Fdrinks.png)
![stays.png](Screenshots%2Fstays.png)
![summary.png](Screenshots%2Fsummary.png)

## Database Design
![database_design.png](Screenshots%2Fdatabase_design.png)


## FAQ

#### How was this readme created?

https://readme.so/de/editor

#### How can I contribute?

Text us!

