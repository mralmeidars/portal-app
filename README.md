# PortalApp

-------
<p align="center">
    <a href="#motivation">Motivation</a> &bull;
    <a href="#installation">Installation</a>
</p>
-------


## Motivation

This App was developed with the aim of improve my skills in Data Engineering, Front-End, Back-End using:
Python v3.7.3 (libs: Requests, Pymongo, Google, Tweepy, Multiprocessing, Web Scraping on Twitter and Google)
Django v2.2
MongoDB v4.0
Google Charts API (Graphs)
Bootstrap 3.4
Javascript

The intention is to apply improvements while I learning new ways to program in Python and another stacks.


## Installation

To execute this project, all you need to setup it properly is:

Using "Docker" and "docker-compose"
```
# REQUIREMENTS:
# docker and docker-compose installed
# clone the repository (portalapp)


# Inside of 'portalapp' directory there are Dockerfile and docker-compose.yml to setup the application
docker-compose up

# Access URL in your Browser
www.localhost:8000/home
```


Using "Virtualenv"
```
# REQUIREMENTS:
# have installed and running the MongoDB (v4.0 prefered) and Python (v3.7 prefered) on your LocalHost
# clone the repository (portalapp)


# Install Virtualenv
pip install virtualenv

# Inside of portalapp directory - Create the Virtual Enviroment
virtualenv -p 'python3' venv

# Inside of portalapp directory - Connect in the Virtual Environment
source venv/bin/activate

# Another requirements will be installed
pip install -r requirements

# Execute the commands to start
python manage.py migrate
python manage.py runserver

# Access URL in your Browser
www.localhost:8000/home
```
