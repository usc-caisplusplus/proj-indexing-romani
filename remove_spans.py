import re
import os
import glob

directory = os.path.join(os.path.dirname(__file__), "FHM_transcript_XMLs")
xml_files = glob.glob(os.path.join(directory, "*.xml"))

span_tag_pattern = re.compile(r"<span[^>]*>|</span>")

processed = 0
for filepath in xml_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = span_tag_pattern.sub("", content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        processed += 1

print(f"Done. Modified {processed} of {len(xml_files)} files.")
