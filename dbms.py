import mysql.connector

import csv



conn = mysql.connector.connect(user='root', password='Kaddulive@0', host='127.0.0.1', database='plantData')
cursor = conn.cursor()


querry = 'insert into plants (sNo,plant_name,botname,part,disease,region,plant_desc) values ("%s","%s","%s","%s","%s","%s","%s");'

file = open('data.csv')

csvreader = list(csv.reader(file))
csvreader.pop(0)
k = 0

for i in csvreader:
    print(k)
    cursor.execute(querry,i)
    k+=1

conn.commit()
cursor.close()
conn.close()