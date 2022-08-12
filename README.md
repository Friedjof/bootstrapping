# causal-impact

## Description
this project has a command line interface to run causal impact analysis on a set of data.
first you need to install the dependencies:
```bash
pip install -r requirements.txt
```
with this command you can start the project command line interface:
```bash
python setup.py
```
to setup the project for the first time you need to run the following command in the project command line interface:
```text
project setup
```
this will create the database directory, the project configuration file and other files needed for the project.

## Project structure
In the data directory you can find the configuration file and the database directory.
```text
data/
    config/
        config.ini
        config.ini.template
        query.sql
        query.sql.template
    database/
        db.sqlite
        db.sqlite.bak
```