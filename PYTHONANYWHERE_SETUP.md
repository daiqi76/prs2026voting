# Deploying on PythonAnywhere (24/7 online, no local Mac needed)

This guide walks you through hosting the PRS voting system on **PythonAnywhere**,
a free cloud platform. Once deployed, the website stays online 24/7 — you no
longer need to keep a Mac running with ngrok.

> The current live deployment uses the username **`prs`**, so the site is at
> `https://prs.pythonanywhere.com`. If you deploy your own copy, replace `prs`
> with your own PythonAnywhere username throughout this guide.

> **Free tier notes:** completely free, no credit card. The site stays online,
> but free accounts must click a "Run until 3 months from today" button on the
> Web tab once every 3 months to keep it active (you get an email reminder).

---

## Step 1 — Create a free account

1. Go to **https://www.pythonanywhere.com/registration/register/beginner/**
2. Sign up for a free **Beginner** account.
3. Remember your **username** — your site will live at
   `https://prs.pythonanywhere.com`

---

## Step 2 — Clone the project

1. From the dashboard, open a **Bash console**:
   click **Consoles** → **Bash**.
2. In the console, run:

   ```bash
   git clone https://github.com/daiqi76/prs2026voting.git
   ```

---

## Step 3 — Create a virtual environment and install dependencies

In the same Bash console, run:

```bash
cd prs2026voting
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Wait until installation finishes. Note the Python version by running
`python3 --version` (e.g. `3.10`) — you'll need it in the next step.

---

## Step 4 — Create the web app

1. Go to the **Web** tab (top menu).
2. Click **Add a new web app** → **Next**.
3. Choose **Manual configuration** (NOT "Flask").
4. Select the **same Python version** as in Step 3 → **Next**.
5. The web app is created. Now you need to configure it (Steps 5–7).

---

## Step 5 — Point the web app to the virtualenv

On the **Web** tab, scroll to the **Virtualenv** section and enter:

```
/home/prs/prs2026voting/venv
```

(if you deploy your own copy, replace `prs` with your username)

---

## Step 6 — Configure the WSGI file

1. On the **Web** tab, find the **Code** section and click the link next to
   **WSGI configuration file** (looks like
   `/var/www/prs_pythonanywhere_com_wsgi.py`).
2. **Delete everything** in that file.
3. Paste the following (pure Python only — do **NOT** include the ``` ``` ```
   backtick lines, only the 7 lines between them):

   ```python
   import sys

   project_home = "/home/prs/prs2026voting"
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   from app import app as application
   ```

4. Click **Save** (top right).

> ⚠️ **Common mistake:** if you copy the Markdown code block including the
> ` ```python ` and ` ``` ` lines, the site will fail with an "Unhandled
> Exception". The first line of the WSGI file must be exactly `import sys`.

---

## Step 7 — Set source & working directory (optional but recommended)

On the **Web** tab, **Code** section:

- **Source code:** `/home/prs/prs2026voting`
- **Working directory:** `/home/prs/prs2026voting`

---

## Step 8 — Go live

1. Scroll to the top of the **Web** tab.
2. Click the big green **Reload** button.
3. Open your site:

   | Role | URL |
   |---|---|
   | Voters | `https://prs.pythonanywhere.com` |
   | Admin | `https://prs.pythonanywhere.com/admin` |

   **Admin password:** `PRS2026!@#`

The site is now online 24/7. 🎉

---

## Updating the code later

When you push new changes to GitHub, update the live site by opening a Bash
console and running:

```bash
cd prs2026voting
git pull
```

Then go to the **Web** tab and click **Reload**.

---

## Backing up / exporting votes

- Use the admin panel's **Export CSV / Excel** buttons to download results.
- The SQLite database file (`votes.db`) lives at
  `/home/prs/prs2026voting/votes.db` and persists across restarts.
