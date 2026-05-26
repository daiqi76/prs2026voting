# Ngrok Setup Guide

Follow these steps **once** before the event. After setup, `start.sh` handles everything automatically.

---

## Step 1 — Install Homebrew (skip if already installed)

Open **Terminal** and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify it works:

```bash
brew --version
```

---

## Step 2 — Install ngrok

```bash
brew install ngrok
```

Verify:

```bash
ngrok --version
```

---

## Step 3 — Create a free ngrok account

1. Go to **https://ngrok.com** and click **Sign Up** (free account is enough).
2. After signing in, go to **https://dashboard.ngrok.com/get-started/your-authtoken**.
3. Copy your **Authtoken** (a long string like `2abc...XYZ`).

---

## Step 4 — Connect ngrok to your account

In Terminal, paste your token (replace `<YOUR_TOKEN>` with the one you copied):

```bash
ngrok config add-authtoken <YOUR_TOKEN>
```

You should see: `Authtoken saved to configuration file`

---

## Step 5 — Claim your free static domain

Free accounts get **one fixed public URL** that never changes.

1. Go to **https://dashboard.ngrok.com/domains**
2. Click **Create Domain** — ngrok assigns you a domain like `fox-happy-owl.ngrok-free.app`
3. Copy that domain name.

Update `start.sh` to use your static domain.  
Open `start.sh` and change this line:

```bash
ngrok http 5001
```

to:

```bash
ngrok http --domain=fox-happy-owl.ngrok-free.app 5001
```

(replace `fox-happy-owl.ngrok-free.app` with your actual domain)

---

## Step 6 — Test the full setup

Run:

```bash
bash start.sh
```

You should see output like:

```
Starting Flask server on port 5001...
Starting ngrok tunnel...
Your public voting URL will appear below:
-------------------------------------------
Forwarding    https://fox-happy-owl.ngrok-free.app -> http://localhost:5001
```

Open that URL in a browser — the voting page should appear.

**Share with voters:**
```
https://fox-happy-owl.ngrok-free.app
```

**Admin panel:**
```
https://fox-happy-owl.ngrok-free.app/admin
```

---

## Day-of Checklist

- [ ] Mac plugged in to power
- [ ] System Settings → Energy → **Prevent Mac from sleeping** ✓
- [ ] Connected to WiFi (or ethernet for stability)
- [ ] Run `bash start.sh` in Terminal
- [ ] Verify the public URL loads in a browser
- [ ] Log in to `/admin` and **Open Voting**
- [ ] Share the public URL with all participants

---

## Stopping the server

Press `Ctrl + C` in the Terminal window where `start.sh` is running.  
Both Flask and ngrok will shut down.
