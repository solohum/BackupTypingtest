import mysql.connector

myconn = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword")

cursor = myconn.cursor()
cursor.execute("create database if not exists typing_test;")
cursor.execute("use database typing_test")
cursor.execute("create table if not exists records(username varchar(30), difficulty varchar(30), accuracy int, wpm int)")

