#!/usr/bin/env python3
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "dados_origem"
DOC_DIR = PROJECT_ROOT / "documentacao"
DELIVERY_DIR = DOC_DIR / "entrega_equipe_preenchimento"
MANUAL_FILE = DOC_DIR / "Manual_Operacional_Preenchimento_Planilhas_Carga_Vivon.docx"

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def col_letter(index: int) -> str:
    result = ""
    while index > 0:
        index, rem = divmod(index - 1, 26)
        result = chr(65 + rem) + result
    return result


def extract_headers_and_sheet(source: Path):
    with zipfile.ZipFile(source) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(f"{{{NS_MAIN}}}si"):
                texts = []
                for t in si.iter(f"{{{NS_MAIN}}}t"):
                    texts.append(t.text or "")
                shared.append("".join(texts))

        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relmap = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels
            if rel.tag.endswith("Relationship")
        }

        first_sheet = wb.find(f"{{{NS_MAIN}}}sheets")[0]
        sheet_name = first_sheet.attrib["name"]
        rid = first_sheet.attrib[f"{{{NS_REL}}}id"]
        sheet_path = "xl/" + relmap[rid].lstrip("/")
        sheet_root = ET.fromstring(z.read(sheet_path))
        sheet_data = sheet_root.find(f"{{{NS_MAIN}}}sheetData")
        row1 = sheet_data.find(f"{{{NS_MAIN}}}row") if sheet_data is not None else None
        headers = []
        if row1 is not None:
            for cell in row1.findall(f"{{{NS_MAIN}}}c"):
                t = cell.attrib.get("t")
                v = cell.find(f"{{{NS_MAIN}}}v")
                isel = cell.find(f"{{{NS_MAIN}}}is")
                text = ""
                if t == "s" and v is not None and v.text is not None:
                    text = shared[int(v.text)]
                elif t == "inlineStr" and isel is not None:
                    text = "".join(node.text or "" for node in isel.iter(f"{{{NS_MAIN}}}t"))
                elif v is not None and v.text is not None:
                    text = v.text
                headers.append(text)
        return sheet_name, headers


def build_content_types():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""


def build_root_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


def build_workbook(sheet_name: str):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="{NS_REL}">
  <sheets>
    <sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""


def build_workbook_rels():
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="{NS_REL}/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="{NS_REL}/styles" Target="styles.xml"/>
</Relationships>"""


def build_styles():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1">
    <font>
      <sz val="11"/>
      <name val="Calibri"/>
      <family val="2"/>
    </font>
  </fonts>
  <fills count="2">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
  </fills>
  <borders count="1">
    <border><left/><right/><top/><bottom/><diagonal/></border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
  </cellXfs>
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>
</styleSheet>"""


def build_sheet(headers):
    last_col = col_letter(len(headers)) if headers else "A"
    cells = []
    for idx, header in enumerate(headers, start=1):
        ref = f"{col_letter(idx)}1"
        cells.append(
            f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(header)}</t></is></c>'
        )
    row = f'<row r="1">{"".join(cells)}</row>'
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="{NS_MAIN}">
  <dimension ref="A1:{last_col}1"/>
  <sheetViews>
    <sheetView workbookViewId="0"/>
  </sheetViews>
  <sheetFormatPr defaultRowHeight="15"/>
  <sheetData>
    {row}
  </sheetData>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
</worksheet>"""


def build_core():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Modelo de planilha para preenchimento</dc:title>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
</cp:coreProperties>"""


def build_app(sheet_name: str):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Excel</Application>
  <HeadingPairs>
    <vt:vector size="2" baseType="variant">
      <vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>
      <vt:variant><vt:i4>1</vt:i4></vt:variant>
    </vt:vector>
  </HeadingPairs>
  <TitlesOfParts>
    <vt:vector size="1" baseType="lpstr">
      <vt:lpstr>{escape(sheet_name)}</vt:lpstr>
    </vt:vector>
  </TitlesOfParts>
</Properties>"""


def create_blank_workbook(target: Path, sheet_name: str, headers):
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", build_content_types())
        z.writestr("_rels/.rels", build_root_rels())
        z.writestr("docProps/core.xml", build_core())
        z.writestr("docProps/app.xml", build_app(sheet_name))
        z.writestr("xl/workbook.xml", build_workbook(sheet_name))
        z.writestr("xl/_rels/workbook.xml.rels", build_workbook_rels())
        z.writestr("xl/styles.xml", build_styles())
        z.writestr("xl/worksheets/sheet1.xml", build_sheet(headers))


def main() -> None:
    DELIVERY_DIR.mkdir(parents=True, exist_ok=True)

    for source in sorted(SOURCE_DIR.glob("*.xlsx")):
        sheet_name, headers = extract_headers_and_sheet(source)
        create_blank_workbook(DELIVERY_DIR / source.name, sheet_name, headers)

    shutil.copy2(MANUAL_FILE, DELIVERY_DIR / MANUAL_FILE.name)
    print(DELIVERY_DIR)


if __name__ == "__main__":
    main()
