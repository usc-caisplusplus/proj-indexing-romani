import html
import os
import glob

directory = os.path.join(os.path.dirname(__file__), "FHM_transcript_XMLs")
xml_files = glob.glob(os.path.join(directory, "*.xml"))

for filepath in xml_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    unescaped = html.unescape(content)

    txt_path = os.path.splitext(filepath)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(unescaped)

print(f"Done. Created {len(xml_files)} .txt files in {directory}")
