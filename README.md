# 📱 Instagram Terminal Chat

Chat on Instagram directly from your terminal — no browser needed!

---

## 📁 Files

| File | Purpose |
|------|---------|
| `login.py` | Saves your Instagram account session (`session.json`) |
| `start.py` | Runs the chat app in the terminal |
| `requirements.txt` | Contains all required libraries |

---

## 📥 Clone the Repository

```bash
git clone https://github.com/siddharthhc/TermiChat.git
cd InstaChatTermi
```

---

## ⚙️ Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate It

**Linux / macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🔐 First Time Login

Save your Instagram account session before running the app:

```bash
python3 login.py
```

> This creates a `session.json` file that stores your login — so you don't have to log in every time.

---

## 🚀 Start the App

```bash
python3 main.py
```

---

## 🔁 Running Again Next Time

If your virtual environment is deactivated, just do:

```bash
source venv/bin/activate   # Windows: venv\Scripts\activate
python3 main.py
```

> No need to run `login.py` again — your session is already saved.

---

## ⚠️ Note

- Do **not** share `session.json` with anyone — it contains your login session.
- If your login expires, run `python3 login.py` again to refresh it.
