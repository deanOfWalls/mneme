#!/bin/bash

MEMORY_DIR="./memories"
OUTPUT_FILE="index.html"

echo "<!DOCTYPE html>" > "$OUTPUT_FILE"
echo "<html lang='en'>" >> "$OUTPUT_FILE"
echo "<head><meta charset='UTF-8'><title>Mneme Memories</title><link rel='stylesheet' type='text/css' href='style.css'></head>" >> "$OUTPUT_FILE"
echo "<body>" >> "$OUTPUT_FILE"
echo "<h1>Mneme Memories</h1>" >> "$OUTPUT_FILE"
echo "<div id='memories-list'>" >> "$OUTPUT_FILE"

# Sort files in descending order based on timestamp in filename
for file in $(ls -1 "$MEMORY_DIR"/*.md | sort -r); do
    filename=$(basename "$file" .md)
    timestamp_hms=$(echo "$filename" | awk -F_ '{print $2}' | tr '-' ':')
    timestamp_date=$(echo "$filename" | awk -F_ '{print $1}' | sed 's/-/\//g')
    content=$(tail -n +3 "$file" | tr '\n' ' ' | sed 's/"/&quot;/g')

    # Only render non-empty content
    if [ -n "$content" ]; then
        echo "<div class='memory-entry'>" >> "$OUTPUT_FILE"
        echo "  <button class='delete-btn' disabled>X</button>" >> "$OUTPUT_FILE"
        echo "  <span>$timestamp_hms $timestamp_date | \"$content\"</span>" >> "$OUTPUT_FILE"
        echo "</div>" >> "$OUTPUT_FILE"
    fi
done

echo "</div>" >> "$OUTPUT_FILE"
echo "</body></html>" >> "$OUTPUT_FILE"
