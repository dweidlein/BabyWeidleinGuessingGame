from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Fly will set PORT, default to 8080 for local
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
