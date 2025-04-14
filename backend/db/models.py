from backend.db.database import cursor, conn
import os

def insert_function(name, language, file_path, timeout):
    cursor.execute("""
        INSERT INTO functions (name, language, file_path, timeout)
        VALUES (?, ?, ?, ?)
    """, (name, language, file_path, timeout))
    conn.commit()

def get_all_functions():
    cursor.execute("SELECT * FROM functions")
    return cursor.fetchall()

def delete_function_by_id(function_id):
    cursor.execute("SELECT file_path FROM functions WHERE id = ?", (function_id,))
    row = cursor.fetchone()
    if row:
        file_path = row[0]
        if os.path.exists(file_path):
            os.remove(file_path)
    cursor.execute("DELETE FROM functions WHERE id = ?", (function_id,))
    conn.commit()

