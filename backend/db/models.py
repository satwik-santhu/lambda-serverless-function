from backend.db.database import cursor, conn
import os

def insert_function(name, language, file_path, timeout):
    cursor.execute("""
        INSERT INTO functions (name, language, file_path, timeout)
        VALUES (?, ?, ?, ?)
    """, (name, language, file_path, timeout))
    conn.commit()
    function_id = cursor.lastrowid  # Get the ID of the inserted function
    return function_id  # Return function_id

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

def log_execution(function_id, exec_time, mem_usage, cpu_percent, status):
    cursor.execute("""
        INSERT INTO executions (function_id, execution_time, memory_usage, cpu_percent, status)
        VALUES (?, ?, ?, ?, ?)
    """, (function_id, exec_time, mem_usage, cpu_percent, status))
    conn.commit()

def get_execution_logs(function_id):
    cursor.execute("""
        SELECT * FROM executions WHERE function_id = ? ORDER BY timestamp DESC
    """, (function_id,))
    return cursor.fetchall()

def get_function_id_by_path(file_path):
    cursor.execute("""
        SELECT id FROM functions WHERE file_path = ?
    """, (file_path,))
    row = cursor.fetchone()
    return row[0] if row else None
