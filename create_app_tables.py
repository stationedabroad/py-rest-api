import sqlite3

connection = sqlite3.connect('appdata.db')
cursor = connection.cursor()

create_users_table = """
						create table if not exists users
						(id INTEGER PRIMARY KEY, -- auto-increment column (have to use integer instead of INT)
						 username text,
						 password text)
					 """	
cursor.execute(create_users_table)
connection.commit()
connection.close()