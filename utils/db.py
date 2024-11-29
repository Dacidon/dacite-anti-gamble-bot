import sqlite3, traceback, os

path = "db/database.db"

def execute(query: str):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        data = cursor.fetchall()
        if bool(data): return data
        else: return None
    except Exception as ex:
        print(f"Error!\nException: {ex}\n" + \
        f"Traceback: {traceback.print_exc()}\n" + \
        f"Query : {query}")

def check_db():
    if not os.path.exists(path):
        sql_user = """CREATE TABLE "user" (
                        "tg_id"	INTEGER NOT NULL UNIQUE,
                        "gamble_total_count" INTEGER NOT NULL DEFAULT 1,
                        "gamble_daily_count" INTEGER NOT NULL DEFAULT 1,
                        "wins_count" INTEGER NOT NULL DEFAULT 0,
                        PRIMARY KEY("tg_id")
                    )"""
        execute(sql_user)

class User:
        
    def get_gamble_total_count(tg_id: int):
        data = execute(f"SELECT gamble_total_count FROM user WHERE tg_id = {tg_id}")
        if bool(data): return data[0][0]
        else: return None
        
    def get_gamble_daily_count(tg_id: int):
        data = execute(f"SELECT gamble_daily_count FROM user WHERE tg_id = {tg_id}")
        if bool(data): return data[0][0]
        else: return None
        
    def add_to_gamble_total_count(tg_id: int):
        execute(f"UPDATE user SET gamble_total_count = gamble_total_count + 1 WHERE tg_id = {tg_id}")
        
    def add_to_gamble_daily_count(tg_id: int):
        execute(f"UPDATE user SET gamble_daily_count = gamble_daily_count + 1 WHERE tg_id = {tg_id}")
        
    def reset_gamble_daily_count(tg_id: int):
        execute(f"UPDATE user SET gamble_daily_count = 0 WHERE tg_id = {tg_id}")
        
    def add_to_wins_count(tg_id: int):
        execute(f"UPDATE user SET wins_count = wins_count + 1 WHERE tg_id = {tg_id}")
        
    def find(tg_id: int):
        data = execute(f"SELECT * FROM user WHERE tg_id = {tg_id}")
        return bool(data)
    
    def add(tg_id: int):
        execute(f"INSERT INTO user (tg_id) VALUES ({tg_id})")
        
    def delete(tg_id: int):
        execute(f"DELETE FROM user WHERE tg_id = {tg_id}")
    
    
    
    