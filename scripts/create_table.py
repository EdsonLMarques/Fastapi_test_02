import sqlite3
# Conexão com o banco de dados
conn = sqlite3.connect('../app/db/database.db')
c = conn.cursor()

# Criação da tabela de clientes
c.execute('''CREATE TABLE IF NOT EXISTS clientes
             (cpf TEXT PRIMARY KEY,
              nome_completo TEXT,
              telefone TEXT,
              fgts REAL)''')

# Criação da tabela de dados de contato
c.execute('''CREATE TABLE IF NOT EXISTS dados_contato
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              cpf TEXT,
              telefone TEXT,
              data_contato TEXT,
              interesse BOOLEAN,
              FOREIGN KEY (cpf) REFERENCES clientes(cpf))''')

# Commit das alterações e fechamento da conexão
conn.commit()
conn.close()
