import cv2
import os 
import numpy as np
import pytesseract
from pytesseract import Output
import psycopg2
from fuzzywuzzy import process,fuzz
from dateutil import parser
import re

def getlastmedicineId(cur):
    cur.execute("select count(*) from medicine1")
    count = int(cur.fetchone()[0])
    if count > 0:
        cur.execute("select id from medicine1 order by id desc limit 1")
        id = int(cur.fetchone()[0])
    else:
        id = 0
    return id 

def saveToDb(pillInfo):
    conn = psycopg2.connect(
    host="localhost",
    database="EVA",
    user="postgres",
    password="postgres"
    )
    cur = conn.cursor()
    lastMedicineId = getlastmedicineId(cur)
    lastMedicineId += 1
    #store the data in DB.
    sql_stmt = """insert into medicine1(id,medname,datefilled,quantity,refillsleft,imagepath,folderpath,refilldate) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    data = (lastMedicineId,pillInfo['medicineName'], pillInfo['dateFilled'], pillInfo['quantity'], pillInfo['refillsLeft'], pillInfo['frontImagePath'], pillInfo['folderPath'],pillInfo['refillDate'])
    cur.execute(sql_stmt,data)
    print("------------------------------------------------")
    print("Saved to DB.")
    conn.commit()
    cur.close()
    conn.close()


