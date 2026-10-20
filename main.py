"""Extrato Fácil: leitura OFX, relatório CSV e importação PostgreSQL."""
import argparse
import csv
from pathlib import Path
from leitor import ler_ofx, totais, moeda
from banco import importar


def exibir(registros):
    print('\nEXTRATO FÁCIL')
    for numero, item in enumerate(registros, start=1):
        tipo = 'Entrada' if item['valor'] > 0 else 'Saída' if item['valor'] < 0 else 'Neutra'
        print(f"\n{numero:02d}. {item['data']:%d/%m/%Y} | {tipo} | {moeda(item['valor'])}")
        print(item['descricao'])
    entradas, saidas, saldo = totais(registros)
    print(f'\nQuantidade total: {len(registros)}')
    print(f'Total de entradas: {moeda(entradas)}')
    print(f'Total de saídas: {moeda(abs(saidas))}')
    print(f'Saldo calculado: {moeda(saldo)}')
    print('Saldo calculado somente com as movimentações do arquivo.')


def exportar(registros, destino):
    # Modo x impede substituir um relatório que já existe.
    with destino.open('x', encoding='utf-8-sig', newline='') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow(['Data', 'Valor', 'Descrição'])
        for item in registros:
            descricao = item['descricao']
            # Evita interpretar descrições como fórmulas em planilhas.
            if descricao.lstrip().startswith(('=', '+', '-', '@')):
                descricao = "'" + descricao
            writer.writerow([item['data'].strftime('%d/%m/%Y'),
                             f"{item['valor']:.2f}".replace('.', ','), descricao])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arquivo', nargs='?', type=Path,
                        default=Path(__file__).resolve().parent / 'extrato.ofx')
    parser.add_argument('--csv', type=Path, metavar='DESTINO', help='Salvar as movimentações em CSV')
    parser.add_argument('--importar', action='store_true', help='Gravar no PostgreSQL')
    args = parser.parse_args()
    try:
        registros = ler_ofx(args.arquivo)
        exibir(registros)
        if args.csv:
            exportar(registros, args.csv)
            print(f'CSV salvo em: {args.csv.resolve()}')
        if args.importar:
            novos = importar(registros)
            print(f'Inseridos: {novos}; já existentes: {len(registros) - novos}.')
    except FileExistsError:
        parser.exit(1, 'O CSV já existe. Escolha outro nome para preservar o relatório anterior.\n')
    except Exception as erro:
        parser.exit(1, f'Falha ({type(erro).__name__}): {erro}\n')


if __name__ == '__main__':
    main()
