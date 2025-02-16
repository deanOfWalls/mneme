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
    filename=$(basename "$file")
    timestamp_hms=$(echo "$filename" | awk -F_ '{print $2}' | tr '-' ':')
    timestamp_date=$(echo "$filename" | awk -F_ '{print $1}' | sed 's/-/\//g')
    content=$(tail -n +3 "$file" | tr '\n' ' ' | sed 's/"/&quot;/g')

    # Only render non-empty content
    if [ -n "$content" ]; then
        echo "<div class='memory-entry' id='entry-$filename'>" >> "$OUTPUT_FILE"
        echo "  <button class='delete-btn' onclick='deleteMemory(\"$filename\")'>[ - ]</button>" >> "$OUTPUT_FILE"
        echo "  <span>$timestamp_hms $timestamp_date | \"$content\"</span>" >> "$OUTPUT_FILE"
        echo "</div>" >> "$OUTPUT_FILE"
    fi
done

echo "</div>" >> "$OUTPUT_FILE"

# Add deleteMemory JS function at the bottom
cat << 'EOF' >> "$OUTPUT_FILE"
<script>
  async function deleteMemory(filename) {
    if (!confirm(`Delete memory ${filename}?`)) return;

    try {
      const response = await fetch('http://192.168.1.166:5000/delete-memory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename }),
      });

      const result = await response.json();
      if (response.ok) {
        document.getElementById(`entry-${filename}`).remove();
        alert(`Deleted: ${filename}`);
      } else {
        alert(`Failed to delete: ${result.error}`);
      }
    } catch (error) {
      alert(`Request failed: ${error.message}`);
    }
  }
</script>
EOF

echo "</body></html>" >> "$OUTPUT_FILE"
