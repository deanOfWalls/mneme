from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

MEMORIES_DIR = "/var/www/mneme/memories"
GIT_REPO_DIR = "/var/www/mneme"

@app.route('/delete-memory', methods=['POST'])
def delete_memory():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    memory_path = os.path.join(MEMORIES_DIR, filename)

    if not os.path.exists(memory_path):
        return jsonify({"error": f"File {filename} not found"}), 404

    try:
        os.remove(memory_path)

        # Rebuild index.html
        subprocess.run(["/bin/bash", os.path.join(GIT_REPO_DIR, "generate-index.sh")], check=True)

        # Git pull to avoid conflicts
        subprocess.run(["git", "-C", GIT_REPO_DIR, "pull", "origin", "master"], check=True)

        # Git add, commit, and push
        subprocess.run(["git", "-C", GIT_REPO_DIR, "add", "memories", "index.html"], check=True)
        subprocess.run(["git", "-C", GIT_REPO_DIR, "commit", "-m", f"Delete memory {filename}"], check=True)
        subprocess.run(["git", "-C", GIT_REPO_DIR, "push", "origin", "master"], check=True)

        return jsonify({"message": f"Memory {filename} deleted successfully"}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Git operation failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
