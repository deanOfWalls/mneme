#!/bin/bash

OUTPUT_FILE="index.html"

echo "<html><body>" > "$OUTPUT_FILE"
for file in *.md; do
    title=$(head -n 1 "$file" | sed 's/# //')
    echo "<p><a href=\"$file\">$title</a></p>" >> "$OUTPUT_FILE"
done
echo "</body></html>" >> "$OUTPUT_FILE"
