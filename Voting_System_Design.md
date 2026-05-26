
# PRS Voting System — Product Requirements Document (PRD)

## 1. Project Background
This system is designed for the **Pattern Recognition Symposium (PRS)** lab activity. The event consists of two parts: **Oral Presentation** and **Poster Session**. The system allows participants to vote via a web page, while the organizer manages the voting status and views results through an admin panel.

---

## 2. Core Business Rules

1. **Vote Quota**:
   - **Oral**: Each participant may cast **up to 2 votes** (not required to use both).
   - **Poster**: Each participant may cast **up to 2 votes** (not required to use both).

2. **Vote Constraints**:
   - Voting for oneself is allowed.
   - **No duplicate votes**: Within the same category (e.g., Oral), the 2 votes must go to **different** candidates.
   - **No re-submission**: Once a participant has submitted votes for a category, they cannot modify or resubmit.

3. **Anti-fraud / Identity Verification**:
   - Participants must enter their **name** (required).
   - The backend performs **dual-factor duplicate detection**: `name` + `device fingerprint (IP address + browser cookie)`.
   - If either the name or the device has already submitted for a given category, the submission is rejected.

4. **Comments**:
   - An optional **comment** field is provided per submission.
   - Comment content and voter identity are visible **only to the admin**, not to regular users.

5. **Voting Channels**:
   - Oral and Poster voting channels open and close **simultaneously**.
   - After voting closes, the user-facing page displays a **"Voting has ended"** message.

6. **Language**:
   - All UI text (user and admin pages) must be in **English**.

---

## 3. Voting Item Design

Each candidate entry (Oral or Poster) displays the following:

```
( )  [Title]
     Presenter: [Name]
```

- A **radio-style circle** (or checkbox) on the left for selection.
- **Title**: presentation or poster title (defaults to `N/A` until confirmed).
- **Presenter**: presenter's name (defaults to `N/A` until confirmed).

Items with `N/A` are hidden from the voting UI; only entries with at least a title or presenter filled in are shown to voters.

---

## 4. Functional Modules

### 4.1 User-Facing Voting Page

- **Step 1 — Identity**: Enter participant name (required). A session cookie is set to track the device.
- **Step 2 — Oral Vote**:
  - Display the list of Oral candidates (title + presenter).
  - Select up to 2 candidates (must be distinct).
  - Optional comment field.
  - Click **"Next"** to proceed to Step 3. Selections are saved temporarily but **not yet committed**.
- **Step 3 — Poster Vote**:
  - Same layout as Step 2, for the Poster category.
  - A **"Back"** button allows returning to Step 2 to revise Oral selections.
  - Once satisfied, click **"Submit Votes"** to show a confirmation summary (Oral + Poster choices).
- **Step 4 — Confirm & Finalize**:
  - Display a summary of all selections for review.
  - Click **"Confirm & Finish"** to permanently commit the votes. After this point, no modifications are allowed.
  - Show a final **"Thank you for voting!"** message.
- **Closed State**: If voting is not active, display **"Voting has ended. Thank you for your participation."** on all pages.

### 4.2 Admin Control Panel

**Access**: Protected by a login page. Password: configured server-side (default: `PRS2026!@#`).

#### 4.2.1 Voting Channel Management
- **Toggle button**: Open / Close voting (affects both Oral and Poster simultaneously).
- Status indicator: `Voting is OPEN` / `Voting is CLOSED`.

#### 4.2.2 Candidate List Management
- Separate management tables for **Oral** and **Poster** candidates.
- For each entry, admin can:
  - **Add** a new candidate (title + presenter).
  - **Edit** title or presenter of an existing entry.
  - **Delete** a candidate entry.
- Entries with empty title and presenter show as `N/A` and are hidden from the voter UI.

#### 4.2.3 Results Dashboard
- **Leaderboard**: Real-time ranking of candidates by total votes received, shown separately for Oral and Poster.
- **Vote Detail Log**: Table view — `Voter` | `Candidate` | `Category` | `Comment` | `Timestamp`.

#### 4.2.4 Data Export
- Export full results (leaderboard + detail log) as **CSV** or **Excel (.xlsx)**.

---

## 5. Technical Stack (Python)

| Component | Choice | Reason |
| :--- | :--- | :--- |
| Framework | **Flask** | Flexible routing; supports session/cookie management for anti-fraud |
| Database | **SQLite** | Lightweight, no setup required, single-file |
| Frontend | Jinja2 templates + plain CSS/JS | Simple, no build toolchain needed |
| Deployment | LAN server (accessible via IP address) | Internal lab use only |

> Streamlit is not recommended here because cookie-based session management and multi-step form flow are difficult to implement reliably in Streamlit.

---

## 6. Database Schema

### Table: `candidates`
| Column | Type | Description |
| :--- | :--- | :--- |
| id | Integer | Primary key |
| category | String | `Oral` or `Poster` |
| title | String | Presentation/poster title (nullable) |
| presenter | String | Presenter name (nullable) |
| display_order | Integer | Display order in the voting list |

### Table: `votes`
| Column | Type | Description |
| :--- | :--- | :--- |
| id | Integer | Primary key |
| voter_name | String | Participant's name |
| voter_ip | String | IP address of the voter's device |
| voter_cookie | String | Browser cookie fingerprint |
| candidate_id | Integer | Foreign key → `candidates.id` |
| category | String | `Oral` or `Poster` |
| comment | Text | Optional comment (nullable) |
| timestamp | DateTime | Submission time |

### Table: `settings`
| Column | Type | Description |
| :--- | :--- | :--- |
| key | String | Setting key (e.g., `voting_active`) |
| value | String | Setting value (e.g., `true` / `false`) |

---

## 7. Anti-Fraud Logic

A submission for a given `category` is **rejected** if **any** of the following is true:
1. A vote record already exists with the same `voter_name` + `category`.
2. A vote record already exists with the same `voter_ip` + `category`.
3. A vote record already exists with the same `voter_cookie` + `category`.

This prevents both name-sharing abuse and device-reuse abuse independently.
