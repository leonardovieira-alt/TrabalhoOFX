CREATE TABLE IF NOT EXISTS movimentacoes (
    id SERIAL PRIMARY KEY,
    data_movimentacao DATE,
    valor NUMERIC(15,2),
    descricao VARCHAR(255)
);
-- Também permite usar a tabela básica criada na aula.
ALTER TABLE movimentacoes ADD COLUMN IF NOT EXISTS banco TEXT;
ALTER TABLE movimentacoes ADD COLUMN IF NOT EXISTS agencia TEXT;
ALTER TABLE movimentacoes ADD COLUMN IF NOT EXISTS conta TEXT;
ALTER TABLE movimentacoes ADD COLUMN IF NOT EXISTS fitid TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS movimentacoes_origem_fitid_uq
    ON movimentacoes (banco, agencia, conta, fitid);
