import os
from getpass import getpass
from pathlib import Path

PASTA = Path(__file__).resolve().parent

def importar(registros):
    import psycopg2

    # Valida antes de abrir a transação: não descarta nem trunca informações.
    for r in registros:
        if not r["fitid"]:
            raise ValueError("Transação sem FITID: importação cancelada para evitar duplicação indevida.")
        if len(r["descricao"]) > 255:
            raise ValueError("Descrição maior que 255 caracteres: ajuste a tabela antes de importar.")
    senha = os.environ.get("PGPASSWORD")
    if senha is None:
        senha = getpass("Senha do PostgreSQL (não aparece ao digitar): ")
    conexao = psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ.get("PGDATABASE", "projeto_ofx"),
        user=os.environ.get("PGUSER", "postgres"),
        password=senha,
        connect_timeout=10,
    )
    inseridos = 0
    try:
        # Commit ao concluir; rollback automático se qualquer operação falhar.
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute((PASTA / "schema.sql").read_text(encoding="utf-8"))
                for r in registros:
                    cursor.execute("""
                        INSERT INTO movimentacoes
                          (data_movimentacao, valor, descricao, banco, agencia, conta, fitid)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (banco, agencia, conta, fitid) DO NOTHING
                    """, (r["data"], r["valor"], r["descricao"], r["banco"],
                          r["agencia"], r["conta"], r["fitid"]))
                    inseridos += cursor.rowcount
    finally:
        conexao.close()
    return inseridos


