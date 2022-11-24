import sqlite3

Connection = sqlite3.connect('Messages.db', check_same_thread=False)
cursor = Connection.cursor()
def create():
    query = """CREATE TABLE IF NOT EXISTS messages(
    Name TEXT NOT NULL,
    recv_message TEXT NOT NULL);"""
    cursor.execute(query)

def add(name_message):
    name_message = str(name_message)
    name = name_message.split(":")[0]
    message = name_message[(len(name)+1):]
    # print(f"{name}")
    # print(f"{message}")
    if name != "" and message != "":
        try:
            cursor.execute(f"""INSERT INTO messages (Name,recv_message)VALUES 
            ('{name}', '{message}')""")
            Connection.commit()
        except Exception as e:
            print(e)

def get():
    cursor.execute("SELECT * FROM messages;")
    res = cursor.fetchall()
    Connection.commit()
    return res

create()
# add("Shuvadip Ghosh: hello")
# get()
