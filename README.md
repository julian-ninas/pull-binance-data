# pull-binance-data
This is a project to pull and update historical cryptocurrency data from binance. 
It consists of a dockerized airflow application and an sql database.

# Prerequisities
* You need to have docker installed
* Python 3.9 or above

# Usage
* Create a file named `.env`, copy inside the content of the `env_template` file, and fill in the necessary variables
* install the python libraries found in `requirements.txt`
* Spin up the containers by running `make start`

