from flask import Flask, jsonify, render_template, request

COMMENTS_FILE = "comments.txt"

app = Flask(__name__)
app._static_folder = 'static'


def write_comment(user, comment):
    with open(COMMENTS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{user}: {comment}\n")


@app.route("/get_comments", methods=["GET"])
def get_comments():
    with open("comments.txt", "r", encoding="utf-8") as file:
        comments = file.readlines()
    return jsonify(comments)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/work_report')
def work_report():
    return render_template("titul.html")

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    user = data.get('nick')
    comment = data.get('comment')
    
    if not user or not comment:
        return jsonify({"error": "Ник и комментарий не могут быть пустыми!"}), 400

    write_comment(user, comment)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)