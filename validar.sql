SELECT * FROM movimentacoes ORDER BY data_movimentacao, id;
SELECT COUNT(*) AS quantidade,
       COALESCE(SUM(CASE WHEN valor > 0 THEN valor ELSE 0 END), 0) AS entradas,
       COALESCE(SUM(CASE WHEN valor < 0 THEN valor ELSE 0 END), 0) AS saidas,
       COALESCE(SUM(valor), 0) AS saldo_calculado
FROM movimentacoes;
