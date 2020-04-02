import sqlite3

DB_NAME = 'appdata.db'

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

create_users_table = """
						create table if not exists users
						(id INTEGER PRIMARY KEY, -- auto-increment column (have to use integer instead of INT)
						 username text,
						 password text)
					 """	

create_items_table = """
						create table if not exists items
						(name text primary key,
						 price real)
					 """
tables = [
	create_users_table,
	create_items_table,
]

for table in tables:
	cursor.execute(table)

# dummy entries
# cursor.execute("insert into items values ('item1', 400.50)")	

connection.commit()
connection.close()