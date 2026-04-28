#!/usr/bin/env python3
import os
import re
from pathlib import Path
from collections import defaultdict

# Define paths
input_dir = Path("/Users/zhangyuhui/Downloads/CAIS Project/FHM_transcript")
output_dir = Path("/Users/zhangyuhui/Downloads/CAIS Project/FHM_transcript_combined")

# Create output directory if it doesn't exist
output_dir.mkdir(exist_ok=True)

# Dictionary to group files by base ID
transcripts = defaultdict(list)

# Pattern to extract base ID and segment number
# Matches: 54022.1_EN.txt -> base_id=54022, segment=1
pattern = re.compile(r'^(\d+)\.(\d+)_EN\.txt$')

# Scan input directory
print(f"Scanning {input_dir}...")
for file_path in sorted(input_dir.glob("*.txt")):
    filename = file_path.name
    match = pattern.match(filename)
    if match:
        base_id = match.group(1)
        segment_num = int(match.group(2))
        transcripts[base_id].append((segment_num, file_path))
    else:
        print(f"Warning: File {filename} doesn't match expected pattern")

print(f"Found {len(transcripts)} unique transcript IDs")

# Combine segments for each transcript
combined_count = 0
for base_id in sorted(transcripts.keys(), key=int):
    segments = sorted(transcripts[base_id], key=lambda x: x[0])
    
    # Read and combine all segments
    combined_content = []
    for segment_num, file_path in segments:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            combined_content.append(content)
    
    # Write combined file
    output_file = output_dir / f"{base_id}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(combined_content))
    
    combined_count += 1
    num_segments = len(segments)
    if num_segments > 1:
        print(f"Combined {base_id}: {num_segments} segments -> {output_file.name}")

print(f"\nTotal files created: {combined_count}")
print(f"Output directory: {output_dir}")
