# PRS 2026 Voting System

A web-based voting system for the Pattern Recognition Symposium (PRS), supporting
Oral Presentation and Poster Session voting. The system is anonymous, prevents
duplicate voting, and provides an admin panel for managing candidates, controlling
the voting window, and exporting results.

---

## 🌐 Live Site

The system is deployed on **PythonAnywhere** and is online 24/7 — no local
computer needs to stay running.

| Role | URL |
|---|---|
| **Voters** | https://prs.pythonanywhere.com |
| **Admin** | https://prs.pythonanywhere.com/admin |

> **Admin password:** ask the organiser

---

## Features

### Voter flow (4 steps, anonymous)
1. Enter your name (used only for fraud prevention, never shown in results)
2. **Oral** vote — choose up to 2 presentations
3. **Poster** vote — choose up to 2 posters (you can go back and edit Oral)
4. Confirm & finish — votes are locked after final submission

### Anti-fraud
Each submission is checked against `name` + `IP address` + `browser cookie`.
If any of these has already voted in a category, the submission is rejected.

### Admin panel

| Feature | Description |
|---|---|
| Open / Close Voting | Enable or disable voting for all participants |
| Manage Candidates | Add, edit, or delete Oral / Poster candidates |
| Leaderboard | Real-time vote rankings |
| Vote Detail Log | Anonymous log of every vote (title, category, comment, time) |
| Export CSV / Excel | Download all results |
| Reset All Votes | Delete all votes (candidates are kept) |

---

## Deployment

The recommended hosting is **PythonAnywhere** (free, always online).
See **[PYTHONANYWHERE_SETUP.md](PYTHONANYWHERE_SETUP.md)** for the full
step-by-step guide.

### Updating the live site after pushing changes

Open a Bash console on PythonAnywhere and run:

```bash
cd prs2026voting
git pull
```

Then go to the **Web** tab and click **Reload**.

---

## Day-of Checklist (organiser)

- [ ] Open `/admin` and log in
- [ ] Under **Manage Candidates**, add all Oral and Poster entries
- [ ] Click **Open Voting**
- [ ] Share the voter URL with all participants
- [ ] After the event, click **Close Voting**
- [ ] Export results via **Export CSV** or **Export Excel**

---

## Local Development / Testing (optional)

To run the app locally on a Mac for testing:

```bash
git clone https://github.com/daiqi76/prs2026voting.git
cd prs2026voting
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5001 in a browser.

> An alternative local setup using **ngrok** for a temporary public URL is
> documented in **[NGROK_SETUP.md](NGROK_SETUP.md)**, but PythonAnywhere is the
> recommended production hosting.

---

## Project Structure

```
prs2026voting/
├── app.py                      # Flask application (routes, voting logic, admin)
├── database.py                 # SQLite helpers (candidates, votes, settings)
├── wsgi_pythonanywhere.py      # WSGI entry point template for PythonAnywhere
├── requirements.txt            # Python dependencies
├── start.sh                    # Local launcher (Flask + ngrok)
├── templates/                  # Jinja2 HTML templates
├── static/css/style.css        # Styles
├── PYTHONANYWHERE_SETUP.md     # Cloud deployment guide (recommended)
└── NGROK_SETUP.md              # Local public-URL guide (alternative)
```

---

## Tech Stack

- **Backend:** Flask + SQLite
- **Frontend:** Jinja2 templates + plain CSS
- **Hosting:** PythonAnywhere (free tier, 24/7)
