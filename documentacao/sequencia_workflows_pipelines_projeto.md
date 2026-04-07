# Sequência de Workflows e Pipelines do Projeto

Data de geração: 2026-04-07

## 1. Fluxo principal do projeto

Workflow principal identificado: `workflows/job_mestre.hwf`

### Sequência de workflows

1. `job_00_setar_variaveis`
2. `job_01_importacao_tabelas_temporarias`
3. `job_02_ajustes`
4. `job_03_insercao_produtos`
5. `job_04_insercao_participantes`
6. `job_05_ajustes_pos_insercao`

### Sequência detalhada de execução

1. Workflow `job_00_setar_variaveis`
   Etapa inicial para definição das variáveis do projeto.

2. Workflow `job_01_importacao_tabelas_temporarias`
   Pipelines executados em sequência:
   - `pipe_1`: `pipe_conversao_fornecedores_base.hpl`
   - `pipe_2`: `pipe_conversao_clientes_base.hpl`
   - `pipe_3`: `pipe_conversao_produtos_base.hpl`
   - `pipe_4`: `pipe_conversao_plano_de_contas.hpl`

3. Workflow `job_02_ajustes`
   Pipelines executados em sequência:
   - `pipe_1`: `pipe_ajuste_das_unidades.hpl`

4. Workflow `job_03_insercao_produtos`
   Pipelines executados em sequência:
   - `pipe_1`: `pipe_01_insercao_produtos.hpl`
   - `pipe_2`: `pipe_02_insercao_gtin.hpl`
   - `pipe_3`: `pipe_03_insercao_tax.hpl`
   - `pipe_4`: `pipe_04_insercao_type.hpl`
   - `pipe_5`: `pipe_05_insercao_unidade_venda.hpl`
   - `pipe_6`: `pipe_06_insercao_grupo_produto.hpl`
   - `pipe_7`: `pipe_07_insercao_subgrupo_produto.hpl`
   - `pipe_8`: `pipe_08_insercao_produtos_adicional.hpl`
   - `pipe_9`: `pipe_09_insercao_produtos_precos.hpl`

5. Workflow `job_04_insercao_participantes`
   Pipelines executados em sequência:
   - `pipe_1`: `pipe_10_insercao_fornecedores.hpl`
   - `pipe_2`: `pipe_11_insercao_fornecedores_adicional.hpl`
   - `pipe_3`: `pipe_12_vincula_produto_fornecedor.hpl`
   - `pipe_4`: `pipe_13_insercao_fornecedores_enderecos.hpl`
   - `pipe_5`: `pipe_14_insercao_clientes.hpl`
   - `pipe_6`: `pipe_15_insercao_clientes_adicional.hpl`
   - `pipe_7`: `pipe_16_insercao_clientes_enderecos.hpl`
   - `pipe_8`: `pipe_17_insercao_relationship.hpl`

6. Workflow `job_05_ajustes_pos_insercao`
   Pipelines executados em sequência:
   - `pipe_1`: `pipe_18_ajustes_pos_insercao.hpl`

## 2. Workflow auxiliar de preparação de ambiente

Workflow identificado: `workflows/job_prepara_ambiente.hwf`

### Sequência

1. `pipe_1`: `pipe_recria_banco_base.hpl`
2. Execução de etapa shell para gerar o dump estrutural em `dumps/alcantara_1_estrutura_completa.sql`

Observação: existe também o workflow `workflows/job_z_teste_wf.hwf`, que usa `pipe_recria_banco_base.hpl` em um fluxo de teste.

## 3. Pipelines existentes no projeto sem vínculo direto com workflows identificados

Os arquivos abaixo existem na pasta `pipelines`, mas não foram encontrados como chamadas diretas dentro dos workflows versionados:

- `pipe_00_esvazia_tabelas.hpl`
- `pipe_ajustes_complementares.hpl`
- `pipe_balanco_maisclean.hpl`
- `pipe_conversao_clientes_base_legacy.hpl`
- `pipe_conversao_estoque_preco_base.hpl`
- `pipe_conversao_estoque_preco_base_legacy.hpl`
- `pipe_conversao_fornecedores_base_legacy.hpl`
- `pipe_conversao_produtos_base_legacy.hpl`
- `pipe_povoa_tabelas_iniciais.hpl`
- `pipe_povoa_tabelas_passo_1.hpl`

## 4. Resumo da ordem macro

1. `job_00_setar_variaveis`
2. `job_01_importacao_tabelas_temporarias`
3. `job_02_ajustes`
4. `job_03_insercao_produtos`
5. `job_04_insercao_participantes`
6. `job_05_ajustes_pos_insercao`

Esse é o encadeamento principal atualmente configurado no arquivo `workflows/job_mestre.hwf`.
