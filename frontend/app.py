from flask import Flask, render_template, redirect, request, flash, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "dev-secret"
API_URL = "http://127.0.0.1:8001"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        team_name = request.form.get("team_name", "").strip()
        leader_name = request.form.get("leader_name", "").strip()
        contact = request.form.get("contact", "").strip()
        member_names = request.form.getlist("member_names")

        payload = {
            "team_name": team_name,
            "leader_name": leader_name,
            "contact": contact,
            "member_names": member_names
        }
        try:
            res = requests.post(f"{API_URL}/register", json=payload)
            res.raise_for_status()
            data = res.json()
            session["team_id"] = data.get("team_id")
            session["team_name"] = team_name
            flash(data.get("message", "Team registered successfully"), "success")
            return redirect(url_for("select"))

        except requests.HTTPError as e:
            try:
                error_detail = res.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            flash(error_detail, "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")

        return render_template("register.html")

    return render_template("register.html")

@app.route("/select", methods=["GET", "POST"])
def select():
    team_id = session.get("team_id")
    if not team_id:
        flash("Please register first", "danger")
        return redirect(url_for("register"))
    try:
        problems = requests.get(f"{API_URL}/problems").json()
    except Exception as e:
        problems = []
        flash(f"Error loading problems: {e}", "danger")
    if request.method == "POST":
        problem_title = request.form.get("problem_title")
        if not problem_title:
            flash("Select a problem", "danger")
            return redirect(url_for("select"))

        try:
            payload = {"team_id": team_id, "problem_statement": problem_title}
            res = requests.post(f"{API_URL}/select_problem", json=payload)
            res.raise_for_status()
            flash(res.json().get("message"), "success")
            return redirect(url_for("thanks"))

        except requests.HTTPError as e:
            try:
                flash(res.json().get("detail", str(e)), "danger")
            except Exception:
                flash(str(e), "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("select.html", problems=problems)

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
