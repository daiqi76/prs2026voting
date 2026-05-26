# app.py
# Main Flask application for the PRS voting system.
# Handles voter flow (4 steps) and admin panel (password-protected).

import csv
import io
import os
import uuid

from flask import (Flask, redirect, render_template, request,
                   send_file, session, url_for, flash)
from openpyxl import Workbook

import database as db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "prs2026-secret-key-change-in-prod")

ADMIN_PASSWORD = "PRS2026!@#"

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def get_voter_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()


def ensure_cookie():
    """Assign a persistent device cookie if the visitor doesn't have one yet."""
    if "device_id" not in session:
        session["device_id"] = str(uuid.uuid4())
    return session["device_id"]


# ─────────────────────────────────────────────
# Voter routes
# ─────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    ensure_cookie()
    if not db.is_voting_active():
        return render_template("closed.html")

    if request.method == "POST":
        name = request.form.get("voter_name", "").strip()
        if not name:
            return render_template("index.html", error="Please enter your name.")
        session["voter_name"] = name
        # Clear any previous draft
        session.pop("oral_draft", None)
        session.pop("poster_draft", None)
        return redirect(url_for("vote_oral"))

    return render_template("index.html")


@app.route("/vote/oral", methods=["GET", "POST"])
def vote_oral():
    ensure_cookie()
    if not db.is_voting_active():
        return render_template("closed.html")
    if "voter_name" not in session:
        return redirect(url_for("index"))

    voter_name = session["voter_name"]
    voter_ip = get_voter_ip()
    voter_cookie = session["device_id"]

    # Check already finalised
    if db.has_voted("Oral", voter_name, voter_ip, voter_cookie):
        return render_template("already_voted.html", category="Oral")

    candidates = [c for c in db.get_candidates("Oral") if c["title"] or c["presenter"]]
    error = None

    if request.method == "POST":
        selected = request.form.getlist("candidates")
        comment = request.form.get("comment", "").strip()

        if len(selected) == 0:
            error = "Please select at least 1 candidate."
        elif len(selected) > 2:
            error = "You can select at most 2 candidates."
        elif len(set(selected)) != len(selected):
            error = "Please select different candidates."
        else:
            session["oral_draft"] = {"ids": selected, "comment": comment}
            return redirect(url_for("vote_poster"))

    draft = session.get("oral_draft", {})
    return render_template("vote_oral.html", candidates=candidates,
                           draft=draft, error=error)


@app.route("/vote/poster", methods=["GET", "POST"])
def vote_poster():
    ensure_cookie()
    if not db.is_voting_active():
        return render_template("closed.html")
    if "voter_name" not in session:
        return redirect(url_for("index"))
    if "oral_draft" not in session:
        return redirect(url_for("vote_oral"))

    voter_name = session["voter_name"]
    voter_ip = get_voter_ip()
    voter_cookie = session["device_id"]

    if db.has_voted("Poster", voter_name, voter_ip, voter_cookie):
        return render_template("already_voted.html", category="Poster")

    candidates = [c for c in db.get_candidates("Poster") if c["title"] or c["presenter"]]
    error = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "back":
            return redirect(url_for("vote_oral"))

        selected = request.form.getlist("candidates")
        comment = request.form.get("comment", "").strip()

        if len(selected) == 0:
            error = "Please select at least 1 candidate."
        elif len(selected) > 2:
            error = "You can select at most 2 candidates."
        elif len(set(selected)) != len(selected):
            error = "Please select different candidates."
        else:
            session["poster_draft"] = {"ids": selected, "comment": comment}
            return redirect(url_for("confirm"))

    draft = session.get("poster_draft", {})
    return render_template("vote_poster.html", candidates=candidates,
                           draft=draft, error=error)


@app.route("/vote/confirm", methods=["GET", "POST"])
def confirm():
    ensure_cookie()
    if not db.is_voting_active():
        return render_template("closed.html")
    if "voter_name" not in session:
        return redirect(url_for("index"))
    if "oral_draft" not in session or "poster_draft" not in session:
        return redirect(url_for("vote_oral"))

    voter_name = session["voter_name"]
    voter_ip = get_voter_ip()
    voter_cookie = session["device_id"]

    oral_draft = session["oral_draft"]
    poster_draft = session["poster_draft"]

    # Resolve candidate objects for display
    oral_candidates = [db.get_candidate_by_id(int(i)) for i in oral_draft["ids"]]
    poster_candidates = [db.get_candidate_by_id(int(i)) for i in poster_draft["ids"]]

    if request.method == "POST":
        action = request.form.get("action")
        if action == "back":
            return redirect(url_for("vote_poster"))

        # Final anti-fraud check before writing
        if db.has_voted("Oral", voter_name, voter_ip, voter_cookie) or \
           db.has_voted("Poster", voter_name, voter_ip, voter_cookie):
            return render_template("already_voted.html", category="both")

        db.save_votes(voter_name, voter_ip, voter_cookie,
                      "Oral", [int(i) for i in oral_draft["ids"]], oral_draft["comment"])
        db.save_votes(voter_name, voter_ip, voter_cookie,
                      "Poster", [int(i) for i in poster_draft["ids"]], poster_draft["comment"])

        session.pop("oral_draft", None)
        session.pop("poster_draft", None)
        return redirect(url_for("thank_you"))

    return render_template("confirm.html",
                           voter_name=voter_name,
                           oral_candidates=oral_candidates,
                           oral_comment=oral_draft["comment"],
                           poster_candidates=poster_candidates,
                           poster_comment=poster_draft["comment"])


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


# ─────────────────────────────────────────────
# Admin routes
# ─────────────────────────────────────────────

def admin_logged_in():
    return session.get("admin") is True


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if admin_logged_in():
        return redirect(url_for("admin_dashboard"))
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Incorrect password."
    return render_template("admin/login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    voting_active = db.is_voting_active()
    oral_board = db.get_leaderboard("Oral")
    poster_board = db.get_leaderboard("Poster")
    details = db.get_vote_details()
    return render_template("admin/dashboard.html",
                           voting_active=voting_active,
                           oral_board=oral_board,
                           poster_board=poster_board,
                           details=details)


@app.route("/admin/reset", methods=["POST"])
def admin_reset():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    db.reset_votes()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/toggle", methods=["POST"])
def admin_toggle():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    current = db.is_voting_active()
    db.set_setting("voting_active", "false" if current else "true")
    return redirect(url_for("admin_dashboard"))


# ── Candidate management ──

@app.route("/admin/candidates")
def admin_candidates():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    oral = db.get_candidates("Oral")
    poster = db.get_candidates("Poster")
    return render_template("admin/candidates.html", oral=oral, poster=poster)


@app.route("/admin/candidates/add", methods=["POST"])
def admin_add_candidate():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    category = request.form.get("category")
    title = request.form.get("title", "").strip() or None
    presenter = request.form.get("presenter", "").strip() or None
    order = int(request.form.get("display_order", 0))
    db.add_candidate(category, title, presenter, order)
    return redirect(url_for("admin_candidates"))


@app.route("/admin/candidates/edit/<int:cid>", methods=["POST"])
def admin_edit_candidate(cid):
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    title = request.form.get("title", "").strip() or None
    presenter = request.form.get("presenter", "").strip() or None
    order = int(request.form.get("display_order", 0))
    db.update_candidate(cid, title, presenter, order)
    return redirect(url_for("admin_candidates"))


@app.route("/admin/candidates/delete/<int:cid>", methods=["POST"])
def admin_delete_candidate(cid):
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    db.delete_candidate(cid)
    return redirect(url_for("admin_candidates"))


# ── Export ──

@app.route("/admin/export/csv")
def export_csv():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    details = db.get_vote_details()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Voter", "Title", "Presenter", "Category", "Comment", "Timestamp"])
    for r in details:
        writer.writerow([r["voter_name"], r["title"], r["presenter"],
                         r["category"], r["comment"], r["timestamp"]])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="prs_votes.csv"
    )


@app.route("/admin/export/excel")
def export_excel():
    if not admin_logged_in():
        return redirect(url_for("admin_login"))
    wb = Workbook()

    # Detail sheet
    ws1 = wb.active
    ws1.title = "Vote Details"
    ws1.append(["Voter", "Title", "Presenter", "Category", "Comment", "Timestamp"])
    for r in db.get_vote_details():
        ws1.append([r["voter_name"], r["title"], r["presenter"],
                    r["category"], r["comment"], r["timestamp"]])

    # Leaderboard sheets
    for cat in ("Oral", "Poster"):
        ws = wb.create_sheet(title=f"{cat} Leaderboard")
        ws.append(["Title", "Presenter", "Votes"])
        for r in db.get_leaderboard(cat):
            ws.append([r["title"], r["presenter"], r["vote_count"]])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(
        buf,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="prs_votes.xlsx"
    )


# ─────────────────────────────────────────────

if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=5001, debug=False)
