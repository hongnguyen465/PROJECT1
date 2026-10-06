import os
import xml.etree.ElementTree as ET

tree = ET.parse('docs/striker_activity_diagrams.drawio')
root = tree.getroot()

os.makedirs('docs/drawio_xml', exist_ok=True)

for i, diag in enumerate(root.findall('diagram')):
    model = diag.find('mxGraphModel')
    xml_str = ET.tostring(model, encoding='unicode')
    
    clean_name = f"So_do_{i+1}.xml"
    with open(f"docs/drawio_xml/{clean_name}", "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"Exported: {clean_name}")
