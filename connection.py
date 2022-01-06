import pyodbc
import os
import shutil
import csv
import sys
import sqlite3
import math
import random
from time import time
from flask import Flask,render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

server = 'localhost:3306'
database = 'Project2'
username = 'root'
password = 'Sunny@mom1'
driver = '{ODBC Driver 17 for SQL Server}'
dbconnect = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

application = Flask(__name__)
bootstrap = Bootstrap(application)


@application.route('/')
def index():
	return render_template('index.html')



@application.route('/printData' , methods=['GET','POST'])
def printData():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT tbl_name FROM sqlite_master WHERE type = 'table';"
	cursor.execute(query)
	tableNames = cursor.fetchall()
	tableNames.pop(0)
	data = {}
	columnNames = {}
	for i in range (len (tableNames)):
		query = "PRAGMA table_info('" +str(tableNames[i][0])+ "');"
		cursor.execute(query)
		columnNames[i] = cursor.fetchall()
		query = "select * from '" +str(tableNames[i][0])+ "'"
		cursor.execute(query)
		data[i] = cursor.fetchall()
	return render_template('printData.html',name1= "USER_ACCOUNTs", tableNames = tableNames, columnNames = columnNames, data = data)


application.debug = True
application.run()
