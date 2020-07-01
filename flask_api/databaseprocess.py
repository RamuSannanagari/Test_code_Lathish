import pandas as pd
import os
import sqlite3
import pyodbc # connect to SQL server 
import mysql.connector # connect to mysql
import psycopg2 # connect to postgrasql
import cx_Oracle # connect to Oracle 

from utility.logger import log

from.save_connection import Connections

class Databaseprocess():
    
    def __init__(self, db_details):
        self.db_details = db_details
        self.operation = db_details["operation"]

        if "database" in db_details:
            self.database = db_details["database"]
        if "Host" in db_details:
            self.host = db_details["host"]
        if "username" in db_details:
            self.username = db_details["username"]
        if "password" in db_details:
            self.password = db_details["password"]
        if "port" in db_details:
            self.port = db_details["port"]
        if "Drivers" in db_details:
            self.Drivers = db_details["Drivers"]

        if "connectiin_name" in db_details:
            self.connection_name = db_details["connectiin_name"]

    def authenticats(self):
        if self.database == 'sqlite':
            connection = sqlite3.connect(self.host)
            status = "successful"
            if not connection:
                status = "failed"
            return status
#Mysql connection
        elif self.database == 'mysql':
            connection = mysql.connector.connect(self.host)
            status = "successful"
            if not connection:
                status = "failed"
            return status
# postgrasql connection
        elif self.database == 'postgrassql':
            connection = psycopg2.connect(self.host)
            status = "successful"
            if not connection:
                status = "failed"
            return status
# SQL server connection
        elif self.database == 'SQL server':
            connection = pyodbc.connect(self.host)
            status = "successful"
            if not connection:
                status = "failed"
            return status
# Oracle connection
        elif self.database == 'oracle':
            connection = cx_Oracle.connect(self.host)
            status ="successful"
            if not connection:
                status="failed"
            return status
        

    def save_db_details(self):
        db_obj = Connections()
        try:
            db_obj.insert(self.connection_name, self.database,
                          self.host, self.username, self.password, self.port)
            status = "successful"
        except Exception as e:
            status = "failed"
            log.exception("%s DB connection error " % e)
        return status

    def get_connection_details(self, connection_name=None):
        db_obj = Connections()
        if not connection_name:
            data = db_obj.showConnections()
        else:
            data = db_obj.showConnectionData(connection_name)
        return data

    def get_db_object_metadata(self):
        pass

    def get_db_object_data(self):
        pass

    def process_db_details(self):
        if self.operation == "test":
            if self.authenticate() == "successful":
                msg = "DB Test cannaction successful"
            else:
                msg = "DB Test connection not sucscessful,please check your credentials"
        elif self.operation == "save":
            if self.save_db_details() == "successful":
                msg = "DB connection saved seccessful"
            else:
                msg = "DB connection save failed,please check credentials"
        elif self.operation == "get_Connectians":
            if "comnection_name" in self.db_details:
                msg = self.get_connection_details(self.connection_name)
            else:
                msg = self.get_connection_details()
        elif self.operation == "metadata":
            msg = None
        elif self.operation == "data":
            msg = None
        return msg
