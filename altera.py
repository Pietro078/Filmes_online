import sqlite3

# Caminho do banco de dados
BANCO = "db.sqlite3"

# Conecta ao banco
conn = sqlite3.connect(BANCO)
cursor = conn.cursor()

# Atualiza o registro de ID 27
cursor.execute("""
    UPDATE filmes_projetc_magnetclinks
    SET link_1080p_dub = ?
    WHERE id = ?
""", ("Link_teste", 27))

# Salva a alteração
conn.commit()

# Verifica se alguma linha foi alterada
if cursor.rowcount > 0:
    print("Registro ID 27 atualizado com sucesso!")
else:
    print("Nenhum registro encontrado com ID 27.")

# Fecha a conexão
conn.close()