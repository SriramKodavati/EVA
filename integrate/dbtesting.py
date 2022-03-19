import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="EVA",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

#cur.execute("CREATE TABLE medicines (id SERIAL,name VARCHAR);")

cur.execute("select id from medicine1 order by id desc limit 1")

#print(cur.fetchone()[0]) 

id = int(cur.fetchone()[0]) 
id = id + 1
print(id)
conn.commit()

cur.close()

conn.close()
