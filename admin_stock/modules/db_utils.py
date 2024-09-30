import sqlite3

DB_NAME = 'inventory.db'

def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        print(f"Conexão bem-sucedida com {DB_NAME}.")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER
    )
    ''')
    conn.commit()
    conn.close()
    print("Tabela 'items' criada ou já existe.")

def delete_item_from_db(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    print(f"Item com id {item_id} deletado do banco de dados.")

def get_items_from_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    rows = cursor.fetchall()
    conn.close()
    print(f"{len(rows)} itens carregados do banco de dados.")
    return [{'id': row[0], 'name': row[1], 'description': row[2], 'quantity': row[3]} for row in rows]
