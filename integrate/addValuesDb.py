import psycopg2

#Establishes connection to database.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

"""
medicineNames = ["ROSUVASTATIN", "Tamsulosin HCL 0.4 MG cap sunp", "Cyclobenzaprine 5 MG", "docusate sodium 100 MG capsule", "Ibuprofen Tablet 800 MG"]

idCount = 1
sql_stmt = insert into medicineNames values(%s,%s)
for i in range(0,len(medicineNames)):
    data = (idCount,medicineNames[i])
    cur.execute(sql_stmt,data)
    idCount += 1
    conn.commit()
"""
medicineNames = []
cur.execute("select name from medicinenames")
data = cur.fetchall()

for i in range(0,len(data)):
    medicineNames.append(data[i][0])
print(medicineNames)

cur.close()
conn.close()
