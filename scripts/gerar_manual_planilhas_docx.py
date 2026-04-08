#!/usr/bin/env python3
import datetime as dt
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = PROJECT_ROOT / "documentacao" / "Guia de Preenchimento das Planilhas de Carga de Dados para o Vivon.docx"
OUTPUT = PROJECT_ROOT / "documentacao" / "Manual_Operacional_Preenchimento_Planilhas_Carga_Vivon.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"


def run(text, *, bold=False, size=None):
    props = []
    if bold:
        props.append("<w:b/>")
    if size is not None:
        props.append(f'<w:sz w:val="{size}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    xml_text = escape(text).replace("\n", "</w:t><w:br/><w:t xml:space=\"preserve\">")
    return f'<w:r>{rpr}<w:t xml:space="preserve">{xml_text}</w:t></w:r>'


def para(*runs, align=None, spacing_before=None, spacing_after=120, keep_next=False):
    ppr = []
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    spacing_attrs = []
    if spacing_before is not None:
        spacing_attrs.append(f'w:before="{spacing_before}"')
    if spacing_after is not None:
        spacing_attrs.append(f'w:after="{spacing_after}"')
    if spacing_attrs:
        ppr.append(f"<w:spacing {' '.join(spacing_attrs)}/>")
    if keep_next:
        ppr.append("<w:keepNext/>")
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr_xml}{''.join(runs)}</w:p>"


def title(text):
    return para(run(text, bold=True, size=30), align="center", spacing_before=120, spacing_after=180, keep_next=True)


def subtitle(text):
    return para(run(text, size=22), align="center", spacing_after=260)


def heading(text):
    return para(run(text, bold=True, size=24), spacing_before=220, spacing_after=120, keep_next=True)


def body(text):
    return para(run(text, size=21), spacing_after=100)


def bullet(text):
    return para(run(f"• {text}", size=21), spacing_after=60)


def field(name, status, rule):
    return para(
        run(f"{name} ", bold=True, size=21),
        run(f"({status}) ", bold=True, size=21),
        run(rule, size=21),
        spacing_after=60,
    )


def build_document_xml():
    today = dt.date.today().strftime("%d/%m/%Y")
    parts = []

    parts.append(title("Manual Operacional de Preenchimento das Planilhas de Carga"))
    parts.append(subtitle("Projeto Vivon • Versão para equipe de preparação de dados"))
    parts.append(body(f"Data de emissão: {today}"))

    parts.append(heading("1. Objetivo"))
    parts.append(body("Este manual orienta a criação, a nomenclatura das colunas e o preenchimento das planilhas usadas na carga de dados do projeto Vivon. O foco é reduzir rejeições, evitar perda de informação e padronizar a preparação dos arquivos antes da importação."))

    parts.append(heading("2. Arquivos contemplados"))
    parts.append(bullet("clientes.xlsx • Aba: def_campos_clientes"))
    parts.append(bullet("fornecedores.xlsx • Aba: def_campos_fornecedor"))
    parts.append(bullet("produtos.xlsx • Aba: def_campos_produtos"))
    parts.append(bullet("plano_de_contas.xlsx • Aba: Planilha1"))

    parts.append(heading("3. Regras obrigatórias para qualquer planilha"))
    parts.append(bullet("Sempre utilize o arquivo-modelo entregue pelo projeto. Não crie uma planilha nova do zero se o layout já existir."))
    parts.append(bullet("Não altere o nome do arquivo, o nome da aba, a ordem das colunas nem o texto do cabeçalho da linha 1. Os arquivos devem seguir exatamente o layout definido no projeto."))
    parts.append(bullet("Preencha os dados a partir da linha 2. A linha 1 é exclusiva para os nomes das colunas."))
    parts.append(bullet("Não insira colunas extras, não remova colunas e não deixe colunas obrigatórias sem preenchimento."))
    parts.append(bullet("Não use fórmulas, células mescladas, comentários, filtros salvos, subtotais, linhas de separação ou cores como sinalização de regra. A carga considera apenas o valor final de cada célula."))
    parts.append(bullet("Cada linha deve representar um único registro completo. Não distribua informações do mesmo cadastro em linhas diferentes."))
    parts.append(bullet("Evite linhas totalmente em branco no meio da base."))
    parts.append(bullet("Campos com códigos longos devem ser mantidos como texto no Excel para impedir notação científica ou perda de zeros à esquerda. Isso é especialmente importante para cpf_cnpj, rg_inscricao_estadual, insc_estadual, codigo_de_barras e referencia."))
    parts.append(bullet("Quando um campo exigir somente números, informe apenas dígitos, sem pontos, barras, traços, parênteses, espaços ou prefixos."))
    parts.append(bullet("Para valores monetários e quantidades decimais, use preenchimento numérico simples, preferencialmente no padrão brasileiro, como 1234,56. Não use símbolo de moeda."))
    parts.append(bullet("Antes de entregar o arquivo, valide duplicidades de códigos, campos obrigatórios vazios e relacionamentos entre planilhas."))

    parts.append(heading("4. Ordem recomendada de preparação"))
    parts.append(bullet("1. Preencher e validar fornecedores.xlsx."))
    parts.append(bullet("2. Preencher e validar clientes.xlsx."))
    parts.append(bullet("3. Preencher e validar produtos.xlsx, usando os códigos já existentes em fornecedores.xlsx."))
    parts.append(bullet("4. Preencher e validar plano_de_contas.xlsx, quando fizer parte do escopo da carga."))

    parts.append(heading("5. Orientações por planilha"))

    parts.append(heading("5.1 clientes.xlsx"))
    parts.append(body("Finalidade: cadastrar clientes e seus dados principais para importação."))
    parts.append(body("Campos do layout: codigo_do_cliente, nome_do_cliente, cpf_cnpj, rg_inscricao_estadual, endereco, num_endereco, bairro, cep, cidade, uf, cod_ibge_cidade, ponto_de_referência, telefone, celular, data_nascimento, limite_credito, email, conjuge, conjuge_cpf, nome_pai, nome_mae, observacoes."))
    parts.append(field("codigo_do_cliente", "obrigatório", "Identificador único do cliente na origem. Não repetir valores. Preferir preenchimento apenas com dígitos, sem espaços ou texto decorativo."))
    parts.append(field("nome_do_cliente", "obrigatório", "Informar nome completo ou razão social. Evitar abreviações desnecessárias."))
    parts.append(field("cpf_cnpj", "obrigatório", "Informar somente números, com 11 dígitos para CPF ou 14 para CNPJ."))
    parts.append(field("rg_inscricao_estadual", "opcional", "Informar somente quando existir. Se preenchido, usar valor real e evitar textos curtos demais."))
    parts.append(field("endereco, num_endereco, bairro, cidade, uf", "obrigatórios", "Preencher endereço completo. A UF deve ter exatamente 2 letras. Se não houver número, informar SN."))
    parts.append(field("cep", "obrigatório", "Informar 8 dígitos, sem máscara."))
    parts.append(field("cod_ibge_cidade", "recomendado", "Informar 7 dígitos."))
    parts.append(field("telefone e celular", "opcionais", "Informar somente números, incluindo DDD."))
    parts.append(field("data_nascimento", "opcional", "Manter um padrão único em toda a planilha. Recomenda-se DD/MM/AAAA."))
    parts.append(field("limite_credito", "opcional", "Informar valor numérico sem símbolo monetário. Exemplo: 1500,00."))
    parts.append(field("email", "opcional", "Informar e-mail válido e completo."))
    parts.append(field("conjuge, conjuge_cpf, nome_pai, nome_mae, observacoes", "opcionais", "Usar apenas quando houver informação confiável."))

    parts.append(heading("5.2 fornecedores.xlsx"))
    parts.append(body("Finalidade: cadastrar fornecedores usados na carga e no vínculo principal dos produtos."))
    parts.append(body("Campos do layout: codigo_do_fornecedor, cpf_cnpj, insc_estadual, fornecedor, nome_fantasia, endereco, numero_endereco, bairro, cep, codigo_ibge_cidade, cidade, uf, fone1, email."))
    parts.append(field("codigo_do_fornecedor", "obrigatório", "Identificador único do fornecedor na origem. Este código é usado por produtos.xlsx no campo codigo_fornecedor_principal."))
    parts.append(field("cpf_cnpj", "obrigatório", "Informar somente números, com 11 dígitos para CPF ou 14 para CNPJ."))
    parts.append(field("insc_estadual", "opcional", "Informar somente números ou texto realmente aplicável, evitando valores incompletos."))
    parts.append(field("fornecedor", "obrigatório", "Razão social completa."))
    parts.append(field("nome_fantasia", "opcional", "Preencher quando existir."))
    parts.append(field("endereco, numero_endereco, bairro, cidade, uf", "obrigatórios", "Preencher endereço completo. UF deve ter 2 letras. Se não houver número, informar SN."))
    parts.append(field("cep", "obrigatório", "Informar 8 dígitos, sem máscara."))
    parts.append(field("codigo_ibge_cidade", "recomendado", "Informar 7 dígitos."))
    parts.append(field("fone1", "opcional", "Informar somente números com DDD."))
    parts.append(field("email", "opcional", "Informar e-mail válido e completo."))
    parts.append(body("Regra crítica: nenhum produto deve apontar para um codigo_fornecedor_principal inexistente em fornecedores.xlsx."))

    parts.append(heading("5.3 produtos.xlsx"))
    parts.append(body("Finalidade: cadastrar produtos para inserção, formação de preço e vínculo com fornecedor principal."))
    parts.append(body("Campos do layout: codigo_do_produto, codigo_de_barras, descricao, referencia, ncm, cest, preco_venda, peso_bruto, estoque, estoque_minimo, preco_custo, descricao_grupo, subgrupo, margem, unidade_de_venda, tax_table_01_ff_ii_nn, codigo_fornecedor_principal, razao_fornecedor_principal, nome_da_marca, tipo_do_produto, preco_compra, ipi, frete, st, Credito_icms, multiplo_de_venda."))
    parts.append(field("codigo_do_produto", "obrigatório", "Identificador único do produto. Não pode repetir em mais de uma linha da planilha."))
    parts.append(field("codigo_de_barras", "recomendado", "Informar somente números. O ideal é informar o GTIN real do produto sempre que existir."))
    parts.append(field("descricao", "obrigatório", "Descrição comercial completa do item."))
    parts.append(field("referencia", "opcional", "Código de referência do fabricante. Manter como texto para evitar perda de zeros ou notação científica."))
    parts.append(field("ncm", "obrigatório", "Informar somente números. Recomenda-se 8 dígitos conforme cadastro fiscal da empresa."))
    parts.append(field("cest", "condicional", "Informar somente números quando aplicável."))
    parts.append(field("preco_venda, preco_custo, preco_compra, ipi, frete, st, Credito_icms", "numéricos", "Informar valores sem símbolo de moeda. Se não houver valor para campos complementares, preferir zero em vez de texto."))
    parts.append(field("peso_bruto, estoque, estoque_minimo, margem, multiplo_de_venda", "numéricos", "Usar apenas números. Estoque e preços devem refletir a base de origem."))
    parts.append(field("descricao_grupo", "obrigatório", "Grupo principal do produto."))
    parts.append(field("subgrupo", "opcional", "Detalhamento do grupo, quando existir."))
    parts.append(field("unidade_de_venda", "obrigatório", "Sigla de unidade compatível com o cadastro do sistema, como UN, CX, KG ou PC."))
    parts.append(field("tax_table_01_ff_ii_nn", "obrigatório", "Preencher com a regra tributária usada pelo projeto, como 01, FF, II ou NN. Esse campo influencia CST, CFOP e CSOSN gerados na importação."))
    parts.append(field("codigo_fornecedor_principal", "obrigatório", "O valor deve existir exatamente em fornecedores.xlsx na coluna codigo_do_fornecedor."))
    parts.append(field("razao_fornecedor_principal", "recomendado", "Preencher com a razão social correspondente ao fornecedor principal para facilitar conferência humana."))
    parts.append(field("nome_da_marca", "opcional", "Marca comercial do produto."))
    parts.append(field("tipo_do_produto", "obrigatório", "Preencher conforme a regra operacional definida para a carga. Nos exemplos atuais da base, o valor usado é S."))

    parts.append(heading("5.4 plano_de_contas.xlsx"))
    parts.append(body("Finalidade: importar o plano de contas quando essa etapa fizer parte da carga do cliente."))
    parts.append(body("Campos do layout: codigo, classificacao, tipo, descricao."))
    parts.append(field("codigo", "obrigatório", "Código interno da linha do plano de contas."))
    parts.append(field("classificacao", "obrigatório", "Classificação hierárquica da conta. Manter o padrão da contabilidade de origem."))
    parts.append(field("tipo", "obrigatório", "Usar o valor previsto no layout de origem, como S para sintética e A para analítica, quando aplicável."))
    parts.append(field("descricao", "obrigatório", "Descrição da conta contábil."))

    parts.append(heading("6. Checklist antes da entrega"))
    parts.append(bullet("O nome do arquivo e da aba está exatamente igual ao modelo."))
    parts.append(bullet("A linha 1 contém os cabeçalhos originais, sem renomeação e sem troca de ordem."))
    parts.append(bullet("Não existem colunas extras nem fórmulas."))
    parts.append(bullet("Os códigos principais não estão duplicados."))
    parts.append(bullet("CEP, CPF, CNPJ, IBGE, NCM, CEST, telefones e códigos de barras estão sem máscara."))
    parts.append(bullet("Todos os produtos apontam para um fornecedor existente."))
    parts.append(bullet("Campos tributários e de unidade foram revisados pela área responsável."))
    parts.append(bullet("Os valores numéricos foram revisados e não contêm texto indevido."))

    parts.append(heading("7. Observação final"))
    parts.append(body("Quando houver dúvida sobre o significado de uma coluna ou sobre a regra de negócio de um campo tributário, a equipe deve validar antes da entrega da planilha. Corrigir o layout na origem é sempre mais seguro do que tratar erros depois da carga."))

    section = (
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:cols w:space="708"/>'
        '<w:docGrid w:linePitch="360"/>'
        "</w:sectPr>"
    )

    body_xml = "".join(parts) + section
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W_NS}">'
        f"<w:body>{body_xml}</w:body>"
        "</w:document>"
    )


def build_core_xml():
    now = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    title = "Manual Operacional de Preenchimento das Planilhas de Carga - Vivon"
    subject = "Orientações de preenchimento das planilhas de carga do projeto Vivon"
    description = "Documento atualizado para a equipe responsável pela preparação das planilhas de carga."
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<cp:coreProperties xmlns:cp="{CP_NS}" xmlns:dc="{DC_NS}" xmlns:dcterms="{DCTERMS_NS}" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="{XSI_NS}">'
        f"<dc:title>{escape(title)}</dc:title>"
        f"<dc:subject>{escape(subject)}</dc:subject>"
        f"<dc:creator>OpenAI Codex</dc:creator>"
        f"<cp:keywords>Vivon, planilhas, carga de dados</cp:keywords>"
        f"<dc:description>{escape(description)}</dc:description>"
        "<cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "</cp:coreProperties>"
    )


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document_xml = build_document_xml()
    core_xml = build_core_xml()

    with zipfile.ZipFile(TEMPLATE, "r") as src, zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                data = document_xml.encode("utf-8")
            elif item.filename == "docProps/core.xml":
                data = core_xml.encode("utf-8")
            dst.writestr(item, data)

    print(OUTPUT)


if __name__ == "__main__":
    main()
