from flask import Flask, request, jsonify

app = Flask(__name__)

# Storage (DSA HashMap)
snippets = {}
tag_index = {}

@app.route("/health", methods=["GET"])
def health():
    return "OK - Deployed", 200


@app.route("/snippet", methods=["POST"])
def add_snippet():
    data = request.json

    snippet_id = data["id"]
    snippets[snippet_id] = data

    for tag in data["tags"]:
        if tag not in tag_index:
            tag_index[tag] = []
        tag_index[tag].append(snippet_id)

    return jsonify({"message": "Snippet added"})


@app.route("/snippet/<int:snippet_id>", methods=["GET"])
def view_snippet(snippet_id):
    if snippet_id not in snippets:
        return jsonify({"error": "Not found"}), 404
    return jsonify(snippets[snippet_id])


@app.route("/tag/<string:tag>", methods=["GET"])
def search_by_tag(tag):
    if tag not in tag_index:
        return jsonify({"message": "No snippets"}), 404

    result = [snippets[i] for i in tag_index[tag]]
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
