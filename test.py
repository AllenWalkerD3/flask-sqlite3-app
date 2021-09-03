import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE tbl_user (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'allen', 'allen1234')

insert_query = "INSERT INTO tbl_user VALUES (?, ?, ?)"
cursor.execute(insert_query, user)


users = [
    (2, 'aren', 'woka1234'),
    (3, 'peter', '111212')
]
cursor.executemany(insert_query, users)

select_all_query = "SELECT * FROM tbl_user"

for row in cursor.execute(select_all_query):
    print(row)
connection.commit()
connection.close()