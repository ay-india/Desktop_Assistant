import sqlite3

def get_connection():
    # Connects to a local database file (creates it automatically if it doesn't exist)
    conn = sqlite3.connect("jarvis_memory.db")
    # Creates the table on the very first run
    conn.execute("CREATE TABLE IF NOT EXISTS memory_bank (id INTEGER PRIMARY KEY, fact TEXT)")
    conn.commit()
    return conn

def save_fact(fact):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Safely injects the text into the database
        cursor.execute("INSERT INTO memory_bank (fact) VALUES (?)", (fact,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def search_memory(query):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Uses SQL 'LIKE' to find any fact that contains your keyword
        cursor.execute("SELECT fact FROM memory_bank WHERE fact LIKE ?", ('%' + query + '%',))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            # If it finds multiple facts, it joins them together
            return "I remember: " + ", and also ".join([row[0] for row in results])
        else:
            return None
    except Exception:
        return None