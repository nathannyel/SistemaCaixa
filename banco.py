import sqlite3

# Conectar ao banco de dados
def conectar():
    conn = sqlite3.connect("caixa.db")
    cursor = conn.cursor()
    return conn, cursor

# Criar tabela se não existir
def criar_tabela():
    conn, cursor = conectar()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            valor REAL,
            descricao TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

# Adicionar movimentação
def adicionar_movimentacao(tipo, valor, descricao, data):
    conn, cursor = conectar()
    cursor.execute("""
        INSERT INTO movimentacoes (tipo, valor, descricao, data)
        VALUES (?, ?, ?, ?)
    """, (tipo, valor, descricao, data))
    conn.commit()
    conn.close()

# Listar movimentações
def listar_movimentacoes():
    conn, cursor = conectar()
    cursor.execute("SELECT * FROM movimentacoes ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados
