from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwtbdSamZHit2-wiwDz9L4bMcb8kFporSJEe-6FsVLegZCcK2SXJEx2K8gGgS9c_OLtDw/exec"


@app.get("/")
def home():
    return render_template("index.html")

@app.post("/submit")
def submit():
    try:
        data = request.get_json(force=True) or {}

        payload = {
            "name": (data.get("name") or "").strip(),
            "birthDate": (data.get("birthDate") or "").strip(),
            "birthTime": (data.get("birthTime") or "").strip(),
            "weight": (data.get("weight") or "").strip(),
            "babyLength": (data.get("babyLength") or "").strip(),

        }

        # basic guardrails
        if not payload["name"]:
            return jsonify(success=False, error="Missing name"), 400

        r = requests.post(
            APPS_SCRIPT_URL,
            data=payload,
            timeout=10
        )

        # Apps Script sometimes returns plain text; handle both
        try:
            out = r.json()
        except Exception:
            out = {"raw": r.text}

        if r.status_code != 200:
            return jsonify(success=False, error=f"Apps Script HTTP {r.status_code}", details=out), 502

        if isinstance(out, dict) and out.get("success") is False:
            return jsonify(success=False, error=out.get("error", "Apps Script error")), 502

        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
