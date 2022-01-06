import os
import shutil
import csv
import sys
import sqlite3 as sq
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


webpage = Flask(__name__)
bootstrap = Bootstrap(webpage)

# Configurations
webpage.config['SECRET_KEY'] = 'blah blah blah blah'

class NameForm(FlaskForm):
	name = StringField('Name', default="Bruce Springsteen")
	submit = SubmitField('Submit')

# ROUTES!
@webpage.route('/')
def index():
	return render_template('index.html')



@webpage.route('/printData' , methods=['GET','POST'])
def printData():
	connection = sq.connect('database.db')
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



@webpage.route('/insert_User_Accounts')
def insert_User_Accounts():
	return render_template('insert_User_Accounts.html')

@webpage.route('/user_accountsData' , methods=['GET','POST'])
def user_accountsData():
	name = (request.form['name'])
	email = (request.form['email'])
	role=(request.form['role'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into USER_ACCOUNTs (Name, Email,UserRole) values ('" +str(name)+ "','" +str(email)+ "','" +str(role)+ "')"
	if (cursor.execute(query)):
		message = "Data uploaded successfully."
	connection.commit()
	return render_template('insert_User_Accounts.html', message = message)



@webpage.route('/insert_User_Roles')
def insert_User_Roles():
	return render_template('insert_User_Roles.html')

@webpage.route('/user_rolesData' , methods=['GET','POST'])
def user_rolesData():
	roleName = (request.form['roleName'])
	description = (request.form['description'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into USER_ROLEs (RoleName, Description) values ('" +str(roleName)+ "','" +str(description)+ "')"
	if (cursor.execute(query)):
		message = "Data uploaded successfully."
	connection.commit()
	return render_template('insert_User_Roles.html', message = message)



@webpage.route('/insert_Tables')
def insert_Tables():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	return render_template('insert_Tables.html', user_accounts = user_accounts)

@webpage.route('/tablesData' , methods=['GET','POST'])
def tablesData():
	tableName = (request.form['tableName'])
	comments = (request.form['comments'])
	userId = (request.form['userId'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into TABLEs (TableName, Comments, UserID) values ('" +str(tableName)+ "','" +str(comments)+ "'," +str(userId)+ ")"
	if (cursor.execute(query)):
		message = "Data added successfully."
	connection.commit()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	return render_template('insert_Tables.html', user_accounts = user_accounts, message = message)



@webpage.route('/insert_Account_Privileges')
def insert_Account_Privileges():
	return render_template('insert_Account_Privileges.html')

@webpage.route('/account_privilegesData' , methods=['GET','POST'])
def account_privilegesData():
	privilegeName = (request.form['privilegeName'])
	comments = (request.form['comments'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into ACCOUNT_PRIVILEGEs (PrivilegeName, Comments) values ('" +str(privilegeName)+ "','" +str(comments)+ "')"
	if (cursor.execute(query)):
		message = "Data uploaded successfully."
	connection.commit()
	return render_template('insert_Account_Privileges.html', message = message)



@webpage.route('/insert_Relation_Privileges')
def insert_Relation_Privileges():
	return render_template('insert_Relation_Privileges.html')

@webpage.route('/relation_privilegesData' , methods=['GET','POST'])
def relation_privilegesData():
	privilegeName = (request.form['privilegeName'])
	comments = (request.form['comments'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into RELATION_PRIVILEGEs (PrivilegeName, Comments) values ('" +str(privilegeName)+ "','" +str(comments)+ "')"
	if (cursor.execute(query)):
		message = "Data uploaded successfully."
	connection.commit()
	return render_template('insert_Relation_Privileges.html', message = message)



@webpage.route('/Relate_user_accountAndUser_role')
def Relate_user_accountAndUser_role():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	return render_template('Relate_user_accountAndUser_role.html', user_accounts = user_accounts, user_roles = user_roles)

@webpage.route('/user_accountAndUser_roleData' , methods=['GET','POST'])
def user_accountAndUser_roleData():
	userId = (request.form['userId'])
	userRole = (request.form['userRole'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "UPDATE USER_ACCOUNTs SET UserRole = " +(userRole)+ " where IdNo == " +(userId)+ ""
	if (cursor.execute(query)):
		message = "Data added successfully."
	connection.commit()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	return render_template('Relate_user_accountAndUser_role.html',user_accounts = user_accounts, user_roles = user_roles, message = message)



@webpage.route('/Relate_account_privilegeAndUser_role')
def Relate_account_privilegeAndUser_role():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT PrivilegeId FROM ACCOUNT_PRIVILEGEs;"
	cursor.execute(query)
	account_privileges = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	return render_template('Relate_account_privilegeAndUser_role.html', account_privileges = account_privileges, user_roles = user_roles)

@webpage.route('/account_privilegeAndUser_roleData' , methods=['GET','POST'])
def account_privilegeAndUser_roleData():
	accountPrivilege = (request.form['accountPrivilege'])
	userRole = (request.form['userRole'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into SPECIFIED_PRIVILEGEs (PrivilegeId, UserRole) values (" +(accountPrivilege)+ "," +(userRole)+ ")"
	if (cursor.execute(query)):
		message = "Data added successfully."
	connection.commit()
	query = " SELECT PrivilegeId FROM ACCOUNT_PRIVILEGEs;"
	cursor.execute(query)
	account_privileges = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	return render_template('Relate_account_privilegeAndUser_role.html', account_privileges = account_privileges, user_roles = user_roles, message = message)



@webpage.route('/Relate_relation_privilegeAndUser_roleAndTable')
def Relate_relation_privilegeAndUser_roleAndTable():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT PrivilegeId FROM RELATION_PRIVILEGEs;"
	cursor.execute(query)
	relation_privileges = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	query = " SELECT TableId FROM TABLEs;"
	cursor.execute(query)
	tables = cursor.fetchall()
	return render_template('Relate_relation_privilegeAndUser_roleAndTable.html', relation_privileges = relation_privileges, user_roles = user_roles, tables = tables)

@webpage.route('/relation_privilegeAndUser_roleAndTableData' , methods=['GET','POST'])
def relation_privilegeAndUser_roleAndTableData():
	relationPrivilege = (request.form['relationPrivilege'])
	userRole = (request.form['userRole'])
	table = (request.form['table'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "insert into TRACKs values ("+(table)+"," +(userRole)+ ", " +(relationPrivilege)+ ")"
	if (cursor.execute(query)):
		message = "Data uploaded successfully."
	connection.commit()
	query = " SELECT PrivilegeId FROM RELATION_PRIVILEGEs;"
	cursor.execute(query)
	relation_privileges = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	query = " SELECT TableId FROM TABLEs;"
	cursor.execute(query)
	tables = cursor.fetchall()
	return render_template('Relate_relation_privilegeAndUser_roleAndTable.html', relation_privileges = relation_privileges, user_roles = user_roles, tables = tables, message = message)

@webpage.route('/user_accountAndPrivilegeRetrive')
def user_accountAndPrivilegeRetrive():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)	
	user_accounts = cursor.fetchall()
	return render_template('user_accountAndPrivilegeRetrive.html', user_accounts = user_accounts)

@webpage.route('/user_accountAndPrivilegeData' , methods=['GET','POST'])
def user_accountAndPrivilegeData():
	userAccount = (request.form['userAccount'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "select ACCOUNT_PRIVILEGEs.PrivilegeId, ACCOUNT_PRIVILEGEs.PrivilegeName, ACCOUNT_PRIVILEGEs.Comments from ACCOUNT_PRIVILEGEs JOIN SPECIFIED_PRIVILEGEs JOIN USER_ACCOUNTs ON ACCOUNT_PRIVILEGEs.PrivilegeId = SPECIFIED_PRIVILEGEs.PrivilegeId and SPECIFIED_PRIVILEGEs.UserRole = USER_ACCOUNTs.UserRole where USER_ACCOUNTs.IdNo = " +(userAccount)+ " group by ACCOUNT_PRIVILEGEs.PrivilegeId"
	cursor.execute(query)
	accountPrivilegeData = cursor.fetchall()
	query = "select RELATION_PRIVILEGEs.PrivilegeId, RELATION_PRIVILEGEs.PrivilegeName, RELATION_PRIVILEGEs.Comments from RELATION_PRIVILEGEs JOIN TRACKs JOIN USER_ACCOUNTs ON RELATION_PRIVILEGEs.PrivilegeId = TRACKs.Privilege and TRACKs.UserRole = USER_ACCOUNTs.UserRole where USER_ACCOUNTs.IdNo = " +(userAccount)+ " group by RELATION_PRIVILEGEs.PrivilegeId"
	cursor.execute(query)
	relationPrivilegeData = cursor.fetchall()
	query = "PRAGMA table_info(ACCOUNT_PRIVILEGEs);"
	cursor.execute(query)
	columnNames = cursor.fetchall()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	return render_template('user_accountAndPrivilegeRetrive.html', user_accounts = user_accounts, accountPrivilegeData = accountPrivilegeData, relationPrivilegeData = relationPrivilegeData, columnNames = columnNames)


@webpage.route('/user_roleAndPrivilegeRetrive')
def user_roleAndPrivilegeRetrive():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	return render_template('user_roleAndPrivilegeRetrive.html', user_roles = user_roles)

@webpage.route('/user_roleAndPrivilegeData' , methods=['GET','POST'])
def user_roleAndPrivilegeData():
	userRole = (request.form['userRole'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "select ACCOUNT_PRIVILEGEs.PrivilegeId, ACCOUNT_PRIVILEGEs.PrivilegeName, ACCOUNT_PRIVILEGEs.Comments from ACCOUNT_PRIVILEGEs JOIN SPECIFIED_PRIVILEGEs ON ACCOUNT_PRIVILEGEs.PrivilegeId = SPECIFIED_PRIVILEGEs.PrivilegeId where SPECIFIED_PRIVILEGEs.UserRole = " +(userRole)+ " group by ACCOUNT_PRIVILEGEs.PrivilegeId"
	cursor.execute(query)
	accountPrivilegeData = cursor.fetchall()
	query = "select RELATION_PRIVILEGEs.PrivilegeId, RELATION_PRIVILEGEs.PrivilegeName, RELATION_PRIVILEGEs.Comments from RELATION_PRIVILEGEs JOIN TRACKs ON RELATION_PRIVILEGEs.PrivilegeId = TRACKs.Privilege where TRACKs.UserRole = " +(userRole)+ " group by RELATION_PRIVILEGEs.PrivilegeId"
	cursor.execute(query)
	relationPrivilegeData = cursor.fetchall()
	query = "PRAGMA table_info(ACCOUNT_PRIVILEGEs);"
	cursor.execute(query)
	columnNames = cursor.fetchall()
	query = " SELECT RoleId FROM USER_ROLEs;"
	cursor.execute(query)
	user_roles = cursor.fetchall()
	return render_template('user_roleAndPrivilegeRetrive.html', user_roles = user_roles, accountPrivilegeData = accountPrivilegeData, relationPrivilegeData = relationPrivilegeData, columnNames = columnNames)


@webpage.route('/privilegeToUser_accountRetrive')
def privilegeToUser_accountRetrive():
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	privileges = []
	query = " SELECT PrivilegeId FROM ACCOUNT_PRIVILEGEs;"
	cursor.execute(query)
	privileges = cursor.fetchall()
	query = " SELECT PrivilegeId FROM RELATION_PRIVILEGEs;"
	cursor.execute(query)
	temp = cursor.fetchall()
	for i in temp:
		privileges.append(i)
	return render_template('privilegeToUser_accountRetrive.html', user_accounts = user_accounts, privileges = privileges)

@webpage.route('/privilegeToUser_accountData' , methods=['GET','POST'])
def privilegeToUser_accountData():
	privilege = (request.form['privilege'])
	userAccount = (request.form['userAccount'])
	connection = sq.connect('database.db')
	cursor = connection.cursor()
	query = "select exists (select ACCOUNT_PRIVILEGEs.PrivilegeId, ACCOUNT_PRIVILEGEs.PrivilegeName, ACCOUNT_PRIVILEGEs.Comments from ACCOUNT_PRIVILEGEs JOIN SPECIFIED_PRIVILEGEs JOIN USER_ACCOUNTs ON ACCOUNT_PRIVILEGEs.PrivilegeId = SPECIFIED_PRIVILEGEs.PrivilegeId and SPECIFIED_PRIVILEGEs.UserRole = USER_ACCOUNTs.UserRole where USER_ACCOUNTs.IdNo = " +(userAccount)+ " and SPECIFIED_PRIVILEGEs.PrivilegeId = " +(privilege)+ " group by ACCOUNT_PRIVILEGEs.PrivilegeId)"
	cursor.execute(query)
	exists = cursor.fetchall()
	if (exists[0][0] == 1):
		message = "Yes, Privilege Id " +(privilege)+ " is granted to User Account " +(userAccount)+ "."
	else:
		query = "select exists (select RELATION_PRIVILEGEs.PrivilegeId, RELATION_PRIVILEGEs.PrivilegeName, RELATION_PRIVILEGEs.Comments from RELATION_PRIVILEGEs JOIN TRACKs JOIN USER_ACCOUNTs ON RELATION_PRIVILEGEs.PrivilegeId = TRACKs.Privilege and TRACKs.UserRole = USER_ACCOUNTs.UserRole where USER_ACCOUNTs.IdNo = " +(userAccount)+ " and TRACKs.Privilege = " +(privilege)+ " group by RELATION_PRIVILEGEs.PrivilegeId)"
		cursor.execute(query)
		exists = cursor.fetchall()
		if (exists[0][0] == 1):
			message = "Yes, Privilege Id " +(privilege)+ " is GRANTED to User Account " +(userAccount)+ "."
		else:
			message = "No, Privilege Id " +(privilege)+ " is NOT GRANTED to User Account " +(userAccount)+ "."
	query = " SELECT IdNo FROM USER_ACCOUNTs;"
	cursor.execute(query)
	user_accounts = cursor.fetchall()
	privileges = []
	query = " SELECT PrivilegeId FROM ACCOUNT_PRIVILEGEs;"
	cursor.execute(query)
	privileges = cursor.fetchall()
	query = " SELECT PrivilegeId FROM RELATION_PRIVILEGEs;"
	cursor.execute(query)
	temp = cursor.fetchall()
	for i in temp:
		privileges.append(i)
	return render_template('privilegeToUser_accountRetrive.html', user_accounts = user_accounts, privileges = privileges, message = message)



port = int(os.getenv('PORT', '3000'))
webpage.debug = True
webpage.run() 
