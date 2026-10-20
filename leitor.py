from decimal import Decimal
from ofxparse import OfxParser

def moeda(valor):
    return f"R$ {valor:,.2f}".translate(str.maketrans({",": ".", ".": ","}))


def ler_ofx(caminho):
    with open(caminho, "rb") as arquivo:
        ofx = OfxParser.parse(arquivo, fail_fast=True)
    registros = []
    for conta in ofx.accounts:
        for t in conta.statement.transactions:
            registros.append({
                "banco": str(conta.routing_number or ""),
                "agencia": str(conta.branch_id or ""),
                "conta": str(conta.account_id or ""),
                "fitid": str(t.id or "").strip(),
                "data": t.date.date(),
                "valor": t.amount,
                "descricao": t.memo or t.payee or "Sem descrição",
            })
    return registros


def totais(registros):
    entradas = sum((r["valor"] for r in registros if r["valor"] > 0), Decimal("0.00"))
    saidas = sum((r["valor"] for r in registros if r["valor"] < 0), Decimal("0.00"))
    return entradas, saidas, entradas + saidas


