# Renomeacao de Arquivos Apache Hop

Data: 2026-04-04

## Workflows

| Nome antigo | Nome novo |
|---|---|
| `workflows/Job Mestre.hwf` | `workflows/job_mestre.hwf` |
| `workflows/Job_00_Setar_variaveis.hwf` | `workflows/job_00_setar_variaveis.hwf` |
| `workflows/Job_01_Importação_para_tabelas_temporarias.hwf` | `workflows/job_01_importacao_tabelas_temporarias.hwf` |
| `workflows/Job_02_Ajustes.hwf` | `workflows/job_02_ajustes.hwf` |
| `workflows/Job_03_Inserção_dos_produtos.hwf` | `workflows/job_03_insercao_produtos.hwf` |
| `workflows/Job_04_Inserção_dos_participantes.hwf` | `workflows/job_04_insercao_participantes.hwf` |
| `workflows/Job_05_Ajustes_pos_insercao.hwf` | `workflows/job_05_ajustes_pos_insercao.hwf` |
| `workflows/prepara_ambiente.hwf` | `workflows/job_prepara_ambiente.hwf` |
| `workflows/z_teste_wf.hwf` | `workflows/job_z_teste_wf.hwf` |

## Pipelines

| Nome antigo | Nome novo |
|---|---|
| `pipelines/00_Esvazia as tabelas.hpl` | `pipelines/pipe_00_esvazia_tabelas.hpl` |
| `pipelines/Ajuste_das_unidades.hpl` | `pipelines/pipe_ajuste_das_unidades.hpl` |
| `pipelines/Ajustes_18_pos_insercao.hpl` | `pipelines/pipe_18_ajustes_pos_insercao.hpl` |
| `pipelines/Ajustes_Complementares.hpl` | `pipelines/pipe_ajustes_complementares.hpl` |
| `pipelines/Conversao Estoque_Preco_base.hpl` | `pipelines/pipe_conversao_estoque_preco_base.hpl` |
| `pipelines/Conversao_plano_de_contas.hpl` | `pipelines/pipe_conversao_plano_de_contas.hpl` |
| `pipelines/Conversão Clientes_base.hpl` | `pipelines/pipe_conversao_clientes_base.hpl` |
| `pipelines/Conversão Fornecedores_base.hpl` | `pipelines/pipe_conversao_fornecedores_base.hpl` |
| `pipelines/Conversão Produtos_base.hpl` | `pipelines/pipe_conversao_produtos_base.hpl` |
| `pipelines/Insercao_01_Produtos.hpl` | `pipelines/pipe_01_insercao_produtos.hpl` |
| `pipelines/Insercao_02_GTIN.hpl` | `pipelines/pipe_02_insercao_gtin.hpl` |
| `pipelines/Insercao_03_TAX.hpl` | `pipelines/pipe_03_insercao_tax.hpl` |
| `pipelines/Insercao_04_Type.hpl` | `pipelines/pipe_04_insercao_type.hpl` |
| `pipelines/Insercao_05_Unidade_de_Venda.hpl` | `pipelines/pipe_05_insercao_unidade_venda.hpl` |
| `pipelines/Insercao_06_grupo_do_produto.hpl` | `pipelines/pipe_06_insercao_grupo_produto.hpl` |
| `pipelines/Insercao_07_subgrupo_do_produto.hpl` | `pipelines/pipe_07_insercao_subgrupo_produto.hpl` |
| `pipelines/Insercao_08_produtos_adicional.hpl` | `pipelines/pipe_08_insercao_produtos_adicional.hpl` |
| `pipelines/Insercao_09_produtos_precos.hpl` | `pipelines/pipe_09_insercao_produtos_precos.hpl` |
| `pipelines/balanco_maisclean.hpl` | `pipelines/pipe_balanco_maisclean.hpl` |
| `pipelines/conversao_clientes_base.hpl` | `pipelines/pipe_conversao_clientes_base_legacy.hpl` |
| `pipelines/conversao_estoque_preco_base.hpl` | `pipelines/pipe_conversao_estoque_preco_base_legacy.hpl` |
| `pipelines/conversao_fornecedores_base.hpl` | `pipelines/pipe_conversao_fornecedores_base_legacy.hpl` |
| `pipelines/conversao_produtos_base.hpl` | `pipelines/pipe_conversao_produtos_base_legacy.hpl` |
| `pipelines/insercao_10_fornecedores.hpl` | `pipelines/pipe_10_insercao_fornecedores.hpl` |
| `pipelines/insercao_11_fornecedores_adicional.hpl` | `pipelines/pipe_11_insercao_fornecedores_adicional.hpl` |
| `pipelines/insercao_12_vincula_produto_a_fornecedor.hpl` | `pipelines/pipe_12_vincula_produto_fornecedor.hpl` |
| `pipelines/insercao_13_fornecedores_endereços.hpl` | `pipelines/pipe_13_insercao_fornecedores_enderecos.hpl` |
| `pipelines/insercao_14_clientes.hpl` | `pipelines/pipe_14_insercao_clientes.hpl` |
| `pipelines/insercao_15_clientes_adicional.hpl` | `pipelines/pipe_15_insercao_clientes_adicional.hpl` |
| `pipelines/insercao_16_clientes_endereços.hpl` | `pipelines/pipe_16_insercao_clientes_enderecos.hpl` |
| `pipelines/insercao_17_relationship.hpl` | `pipelines/pipe_17_insercao_relationship.hpl` |
| `pipelines/povoa as tabelas iniciais.hpl` | `pipelines/pipe_povoa_tabelas_iniciais.hpl` |
| `pipelines/povoa as tabelas passo 1.hpl` | `pipelines/pipe_povoa_tabelas_passo_1.hpl` |
| `pipelines/recria_banco_base.hpl` | `pipelines/pipe_recria_banco_base.hpl` |

## Observacoes

- Os arquivos duplicados que ja existiam com nomes parcialmente normalizados receberam sufixo `_legacy` para evitar colisao.
- As referencias internas em workflows e pipelines foram atualizadas para os nomes canônicos atuais.
