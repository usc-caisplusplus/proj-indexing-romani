import os
import glob
import re

directory = os.path.join(os.path.dirname(__file__), "FHM_transcript_XMLs")
txt_files = glob.glob(os.path.join(directory, "*.txt"))

# Pattern to strip the XML declaration line and the wrapping tags
front_pattern = re.compile(r"^<\?xml[^?]*\?>\n?<transcription><p>", re.DOTALL)
end_pattern = re.compile(r"</p><p></p></transcription>\s*$", re.DOTALL)

modified = 0
for filepath in txt_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = front_pattern.sub("", content)
    new_content = end_pattern.sub("", new_content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        modified += 1

print(f"Done. Modified {modified} of {len(txt_files)} .txt files.")
