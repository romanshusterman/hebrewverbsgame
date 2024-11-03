from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "very_secret_key"  # Change to a real secret key in production

verbs = {
    "לאהוב": {"english": "to love", "russian": "любить", "binyan": "פָּעַל"},
    "לאחר": {"english": "to delay", "russian": "задерживать", "binyan": "פִּעֵל"},
    "לאכול": {"english": "to eat", "russian": "есть", "binyan": "פָּעַל"},
    "לבוא": {"english": "to come", "russian": "приходить", "binyan": "פָּעַל"},
    "לבחור": {"english": "to choose", "russian": "выбирать", "binyan": "פָּעַל"}
}

binyanim = ["פָּעַל", "פִּעֵל", "הִפְעִיל", "הִתְפַּעֵל", "פֻּעַל", "הֻפְעַל", "נִפְעַל"]

@app.route("/", methods=["GET", "POST"])
def index():
    session["verb_index"] = 0
    return render_template("index.html", verb=list(verbs.keys())[session["verb_index"]])

@app.route("/process_response", methods=["POST"])
def process_response():
    response = request.form.get("response")
    if response == "yes":
        session["verb_index"] = (session["verb_index"] + 1) % len(verbs)
    elif response == "no":
        return redirect(url_for("translate"))
    return redirect(url_for("index"))

@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        return redirect(url_for("binyan"))
    current_verb = list(verbs.keys())[session["verb_index"]]
    translations = verbs[current_verb]
    return render_template("translate.html", verb=current_verb, translations=translations)

@app.route("/binyan", methods=["GET", "POST"])
def binyan():
    verb = list(verbs.keys())[session["verb_index"]]
    correct_binyan = verbs[verb]["binyan"]
    if request.method == "POST":
        user_binyan = request.form.get("binyan")
        if user_binyan == correct_binyan:
            return redirect(url_for("conjugate"))
        else:
            return render_template("binyan.html", message="Wrong. Try another binyan.", binyanim=binyanim, verb=verb)
    return render_template("binyan.html", binyanim=binyanim, verb=verb)

@app.route("/conjugate", methods=["GET", "POST"])
def conjugate():
    verb = list(verbs.keys())[session["verb_index"]]
    if request.method == "POST":
        # Here you should validate user input against the correct forms
        return redirect(url_for("index"))
    return render_template("conjugate.html", verb=verb)

if __name__ == "__main__":
    app.run(debug=True)
