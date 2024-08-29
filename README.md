[![Deploy to Portainer with Self-Hosted Runner](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/Docker-Build.yml/badge.svg)](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/Docker-Build.yml) ![Deployment](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/Docker-Build.yml/badge.svg) ![Sonarqube](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/sonarqube-scanner.yml/badge.svg) ![Tests](https://github.com/henry4711lp/LSF-Fliegerlager-Webapp/actions/workflows/test_on_push.yml/badge.svg)
# LSF-Fliegerlager-Webapp

This app is to replace a handwritten list for "bought" drinks, dinners and accomodation days.  
The purpose of this webapp is to decrease the workload of the club youth management in the accounting process of the flying camp and to prevent the loss of the handwritten lists.

Latest version: **V0.1 Alpha**
Latest Main Branch running on: https://lsf-flilaapp.sellerbeckcloud.de/

## Authors

- [Jan Sellerbeck](https://www.github.com/henry4711lp)
- [Robin Busch](https://www.github.com/rbn-de)
- ### HELP WANTED ***REDESIGN FRONTEND***


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
- [X]  Dinner function implemented
- [X]  Day function implemented
- [ ]  Open issues closed
------------------------------------
- [ ] **V0.1 Alpha release**
------------------------------------
- [ ] UI user tests
- [ ] Data Privacy inspection
- [ ] Bugfixes
- [ ] Code review
- [ ] Documentation
- [ ] Open issues closed
- [ ] Relief stress on API calls --> new DB design pulling data from VF API and storing
------------------------------------
- [ ] **V0.1 Beta release**
------------------------------------

## Tech Stack

**Client:** Android Browser, HTML5, CSS3, JavaScript (ES6)

**Server:** MySQL, phpMyAdmin, Python 3.9, Docker

**Python Libraries:** Flask, mysql-connector-python, PyYAML, requests, tabulate, setuptools, getConfig, Werkzeug, flask_httpauth, XlsxWriter, APScheduler

**CI/CD:** Github Actions, Sonarqube, Docker, Docker-Compose, Quodana, CodeQL, Ubuntu 20.04, Github Runner, Portainer


## Run Locally for Development
-  Clone the project
-  Install the requirements
-  Install XAMPP or another mysql server and add it to the config file
-  Start the mysql server
-  Start the phpmyadmin server
-  Create a user and add it to the config file
-  Create a database and add it to the config file
-  Import the tables from the sql file
-  Run the main.py

## Run for Production
-  deploy a mysql server
-  run the sample database creation script
-  pull and run the docker image with these commands:
```bash
  docker pull henry4711lp/lsf-fliegerlager-webapp:latest
  docker run -d -p 5000:5000 -v ${YOUR_CONFIG_PATH}:/config/config.yaml --restart unless-stopped henry4711lp/lsf-fliegerlager-webapp:latest
```

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
##### HELP WANTED ***REDESIGN FRONTEND***

