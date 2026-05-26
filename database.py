# database.py
# Handles SQLite database initialization and all query helpers for the PRS voting system.

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "votes.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT,
            presenter TEXT,
            display_order INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_name TEXT NOT NULL,
            voter_ip TEXT NOT NULL,
            voter_cookie TEXT NOT NULL,
            candidate_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Default settings
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('voting_active', 'false')")

    conn.commit()
    conn.close()


# ---------- Settings ----------

def get_setting(key):
    conn = get_db()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else None


def set_setting(key, value):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def is_voting_active():
    return get_setting("voting_active") == "true"


# ---------- Candidates ----------

def get_candidates(category):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM candidates WHERE category = ? ORDER BY display_order, id",
        (category,)
    ).fetchall()
    conn.close()
    return rows


def get_all_candidates():
    conn = get_db()
    rows = conn.execute("SELECT * FROM candidates ORDER BY category, display_order, id").fetchall()
    conn.close()
    return rows


def add_candidate(category, title, presenter, display_order=0):
    conn = get_db()
    conn.execute(
        "INSERT INTO candidates (category, title, presenter, display_order) VALUES (?, ?, ?, ?)",
        (category, title, presenter, display_order)
    )
    conn.commit()
    conn.close()


def update_candidate(candidate_id, title, presenter, display_order):
    conn = get_db()
    conn.execute(
        "UPDATE candidates SET title = ?, presenter = ?, display_order = ? WHERE id = ?",
        (title, presenter, display_order, candidate_id)
    )
    conn.commit()
    conn.close()


def delete_candidate(candidate_id):
    conn = get_db()
    conn.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    conn.commit()
    conn.close()


def get_candidate_by_id(candidate_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,)).fetchone()
    conn.close()
    return row


# ---------- Anti-fraud check ----------

def has_voted(category, voter_name, voter_ip, voter_cookie):
    """Return True if any of name / IP / cookie has already voted in this category."""
    conn = get_db()
    row = conn.execute(
        """SELECT id FROM votes WHERE category = ?
           AND (voter_name = ? OR voter_ip = ? OR voter_cookie = ?)
           LIMIT 1""",
        (category, voter_name, voter_ip, voter_cookie)
    ).fetchone()
    conn.close()
    return row is not None


# ---------- Votes ----------

def save_votes(voter_name, voter_ip, voter_cookie, category, candidate_ids, comment):
    conn = get_db()
    for cid in candidate_ids:
        conn.execute(
            """INSERT INTO votes (voter_name, voter_ip, voter_cookie, candidate_id, category, comment)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (voter_name, voter_ip, voter_cookie, cid, category, comment)
        )
    conn.commit()
    conn.close()


def get_leaderboard(category):
    conn = get_db()
    rows = conn.execute(
        """SELECT c.title, c.presenter, COUNT(v.id) as vote_count
           FROM candidates c
           LEFT JOIN votes v ON v.candidate_id = c.id AND v.category = ?
           WHERE c.category = ?
           GROUP BY c.id
           ORDER BY vote_count DESC""",
        (category, category)
    ).fetchall()
    conn.close()
    return rows


def reset_votes():
    conn = get_db()
    conn.execute("DELETE FROM votes")
    conn.commit()
    conn.close()


def get_vote_details():
    conn = get_db()
    rows = conn.execute(
        """SELECT v.voter_name, c.title, c.presenter, v.category, v.comment, v.timestamp
           FROM votes v
           JOIN candidates c ON c.id = v.candidate_id
           ORDER BY v.timestamp DESC"""
    ).fetchall()
    conn.close()
    return rows
