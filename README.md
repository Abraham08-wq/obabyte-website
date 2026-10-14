# Oba-Byte Enterprises — website

One-page site with a working contact form that emails you.

```
obabyte-website/
├── index.html        the whole site (frontend)
├── app.py            Python/Flask backend (serves the site + /api/contact)
├── requirements.txt  Python dependencies
├── .env.example      copy to .env and add your Gmail app password
└── contact.php       alternative backend for cPanel/shared hosting
```

---

## A. Run it locally (Python) — copy/paste

```bash
cd obabyte-website

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env               # then edit .env (see below)
python app.py
```

Open http://localhost:8000

### Set up the email (one time)
The form sends through your Gmail. Gmail needs an **App Password**, not your normal password:
1. Go to myaccount.google.com → **Security** → turn on **2-Step Verification**.
2. Then **Security → App passwords** → create one for **Mail**.
3. Put it in `.env`:
   ```
   SMTP_USER=obajeabrham24@gmail.com
   SMTP_PASS=the-16-character-app-password
   ```
4. Restart: `python app.py`.

Until you add the app password, the page still loads — the form just reports it isn't configured yet.

---

## B. Host it so it's online

### Option 1 — cPanel / shared hosting (PHP, simplest with the form)
1. In **File Manager**, open `public_html`.
2. Upload `index.html` and `contact.php` into it.
3. In `index.html`, find `fetch('/api/contact'` and change it to `fetch('contact.php'`.
4. Done — the form works through the server's `mail()`.

### Option 2 — VPS / cloud server (Python, production)
```bash
cd obabyte-website
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt gunicorn
# fill in .env, then run:
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```
Put Nginx in front and point your domain at the server.

### Option 3 — Free static host (no backend, email button only)
Netlify or GitHub Pages. The form needs a server, so on a static-only host
either use a form service (e.g. Formspree) or just keep the “email us” address.
```bash
# Netlify drag-and-drop: rename index.html and drop the folder at app.netlify.com
```

---

## Point your domain
After hosting, in your domain registrar set the DNS record your host gives you
(an A record to the server IP, or a CNAME to the host). Changes take up to a few hours.
