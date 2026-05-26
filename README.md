# PRS 2026 Voting System

A web-based voting system for the Pattern Recognition Symposium (PRS), supporting Oral Presentation and Poster Session voting with a public URL powered by ngrok.

---

## Requirements

- macOS
- Python 3 (pre-installed on most Macs — check with `python3 --version`)
- Homebrew
- ngrok

---

## First-Time Setup (do this once)

### 1. Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, follow the "Next steps" printed in the terminal to add Homebrew to your PATH, then verify:

```bash
brew --version
```

### 2. Install ngrok

```bash
brew install ngrok
```

### 3. Connect ngrok to the account

Ask the organiser for the ngrok **Authtoken**, then run:

```bash
ngrok config add-authtoken <authtoken>
```

### 4. Clone the project

```bash
git clone https://github.com/daiqi76/prs2026voting.git
cd prs2026voting
```

---

## Starting the Server

```bash
bash start.sh
```

The terminal will show:

```
Starting Flask server on port 5001...
Starting ngrok tunnel...
Forwarding  https://email-dazzler-squint.ngrok-free.dev -> http://localhost:5001
```

Share these URLs with participants:

| Role | URL |
|---|---|
| Voters | `https://email-dazzler-squint.ngrok-free.dev` |
| Admin | `https://email-dazzler-squint.ngrok-free.dev/admin` |

> **Admin password:** ask the organiser

---

## Day-of Checklist

- [ ] Mac plugged in to power
- [ ] System Settings → Energy → Prevent Mac from sleeping
- [ ] Run `bash start.sh` in Terminal
- [ ] Log in to `/admin` and click **Open Voting**
- [ ] Share the public URL with all participants
- [ ] After the event, click **Close Voting** in the admin panel
- [ ] Export results via **Export CSV** or **Export Excel**

---

## Stopping the Server

Press `Ctrl + C` in the Terminal window where `start.sh` is running.

---

## Admin Panel Features

| Feature | Description |
|---|---|
| Open / Close Voting | Enable or disable voting for all participants |
| Manage Candidates | Add, edit, or delete Oral / Poster candidates |
| Leaderboard | Real-time vote rankings |
| Vote Detail Log | Full log of every vote with voter name and comment |
| Export CSV / Excel | Download all results |
| Reset All Votes | Delete all votes (candidates are kept) |
