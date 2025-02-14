#!/bin/bash

MEMORY_DIR="./memories"
OUTPUT_FILE="index.html"

echo "<!DOCTYPE html>" > "$OUTPUT_FILE"
echo "<html lang='en'>" >> "$OUTPUT_FILE"
echo "<head><meta charset='UTF-8'><title>Mneme Memories</title></head>" >> "$OUTPUT_FILE"
echo "<body>" >> "$OUTPUT_FILE"
echo "<h1>Mneme Memories</h1>" >> "$OUTPUT_FILE"
echo "<div id='memories-list'>" >> "$OUTPUT_FILE"

# Sort files in descending order based on timestamp in filename
for file in $(ls -1 "$MEMORY_DIR"/*.md | sort -r); do
    timestamp=$(basename "$file" .md | sed 's/_/ /g' | awk '{print $3":"$2":"$1}')
    content=$(cat "$file" | tr '\n' ' ') # Flatten file contents to a single line

    echo "<div class='memory-entry'>" >> "$OUTPUT_FILE"
    echo "  <button class='delete-btn' disabled>X</button>" >> "$OUTPUT_FILE"
    echo "  <span>time: $timestamp created : $content</span>" >> "$OUTPUT_FILE"
    echo "</div>" >> "$OUTPUT_FILE"
done

echo "</div>" >> "$OUTPUT_FILE"

echo "<style>
body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 20px; }
h1 { font-size: 24px; color: #333; }
.memory-entry { display: flex; align-items: center; margin-bottom: 10px; padding: 8px; background-color: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
.delete-btn { margin-right: 10px; background-color: #f44336; color: white; border: none; padding: 4px 8px; cursor: not-allowed; border-radius: 4px; }
span { font-size: 14px; color: #333; }
</style>" >> "$OUTPUT_FILE"

echo "</body></html>" >> "$OUTPUT_FILE"

