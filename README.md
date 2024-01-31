# pull-binance-data
This is a project to pull and update historical cryptocurrency data from binance.<br /> 
It consists of a dockerized airflow application and an sql database.<br />
<br />
It pulls data from 45 different cryptocurrencies.<br />
There is a cron job that updates the data every five minutes and the prices are reported at five-minute intervals. 

# Prerequisities
* You need to have docker installed
* Python 3.9 or above

# Usage
* Create a file named `.env`, copy inside the content of the `env_template` file, and fill in the necessary variables
* install the python libraries found in `requirements.txt`
* Spin up the containers by running `make start`

