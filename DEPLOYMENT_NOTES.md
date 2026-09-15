# What changed, and what to do before going live

## 1. Files changed
- `app.py` — secret key, admin login, and employee passwords now come from
  env vars / hashed storage instead of hardcoded plaintext.
- `google_drive_manager.py` — reads credential/token paths from env vars and
  fails with a clear error on a server instead of trying to open a browser.
- `Procfile` — tells Render (or any Heroku-style host) to run with gunicorn.
- `requirements.txt` — added `gunicorn`, plus the packages your imports need
  (double check this against your real local `pip freeze` — I inferred it
  from your imports, not from an existing requirements file).

## 2. Environment variables to set on Render
In your Render service's "Environment" tab, add:

| Key | Value |
|---|---|
| `FLASK_SECRET_KEY` | any long random string (e.g. generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `ADMIN_USER` | your chosen admin username (don't leave as `admin`) |
| `ADMIN_PASSWORD` | a strong password |
| `GOOGLE_CREDENTIALS_FILE` | `/etc/secrets/credentials.json` (see below) |
| `GOOGLE_TOKEN_FILE` | `/etc/secrets/token.pickle` (see below) |
| `RENDER` | Render sets this automatically — no action needed, it's what triggers the "don't try to open a browser" check |

## 3. Google Drive auth — do this once, locally
The OAuth "sign in with Google" flow needs a real browser, which a server
doesn't have. So:
1. Run the app locally once, as you already do, so it generates a fresh
   `token.pickle` via the browser consent screen.
2. On Render, use **Settings → Secret Files** to upload your `credentials.json`
   and `token.pickle` directly (do NOT commit them to Git). Set the file
   paths to match `GOOGLE_CREDENTIALS_FILE` / `GOOGLE_TOKEN_FILE` above.
3. Google refresh tokens can expire if unused for 6+ months, or if the
   OAuth consent screen is still in "Testing" mode in Google Cloud Console
   (those tokens expire in 7 days) — if uploads start failing, republish
   the consent screen as "In production" in Google Cloud Console, then
   regenerate token.pickle locally and re-upload it.

## 4. Database persistence — the bigger decision
`hrms.db`, `candidates.db`, and the `uploads/` folder are all local files.
Render's free tier wipes local disk on every restart/redeploy, so:
- **Quick fix:** add a Render **persistent disk** (paid, starts ~$1/mo) and
  mount it at `BASE_DIR`, so `hrms.db` and `uploads/` survive restarts.
  No code changes needed — this is the least-effort option.
- **More robust:** migrate off SQLite to Render's managed Postgres. This is
  a bigger job since the code uses raw `sqlite3` + positional `?` params
  throughout (15+ tables) — happy to help with this next if you want it,
  but it's a separate, larger piece of work from what's done here.

## 5. Still worth doing before real employee data goes in
- The employee PII fields (PAN, Aadhar, bank account, salary) are stored as
  plain columns with no encryption at rest. SQLite files themselves aren't
  encrypted — if you go the persistent-disk route, this data sits on disk
  as-is. Worth knowing given what this app stores.
- Existing plaintext passwords in your current `hrms.db` will auto-upgrade
  to hashed ones the next time each employee logs in successfully — no
  migration script needed.
