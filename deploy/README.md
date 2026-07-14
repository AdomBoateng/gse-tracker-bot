# Deploying GSE Tracker on a free AWS EC2 instance (with HTTPS)

This hosts the **whole app on one small EC2 instance**:

```
Internet ──HTTPS──▶ nginx (:443)
                     ├── /            → built Vue SPA (frontend/dist)
                     └── /api/…       → gunicorn (127.0.0.1:8000) → FastAPI
                                          └── fetches dev.kwayisi.org directly
```

Because the backend runs on EC2 (an AWS IP, not Google Cloud), it can fetch the
GSE data API that blocked Render. nginx serves the frontend and proxies `/api`
same-origin, so there are no CORS issues. EC2 has a persistent disk, so the
SQLite history/news DB survives restarts.

> **Reality check:** `dev.kwayisi.org` blocks datacenter IPs. AWS *may* also be
> blocked. **Step 0 below tests this in one command** — do it before investing in
> the full setup. If it fails, EC2 won't help and we switch data sources.

---

## Prerequisites

- An **AWS account** (the EC2 `t2.micro`/`t3.micro` free tier covers 750 hrs/month
  for the first 12 months).
- A free **[DuckDNS](https://www.duckdns.org)** account (sign in with GitHub/Google).

## Step 0 — Confirm AWS can reach the data API (do this first)

Launch a throwaway instance (or your real one) and SSH in, then run:

```bash
curl -m 15 -s -o /dev/null -w "%{http_code} in %{time_total}s\n" https://dev.kwayisi.org/apis/gse/live
```

- `200 in 0.x s` → 🎉 AWS is not blocked. Continue.
- Hangs / `000` → AWS is blocked too. Stop here and tell me — we'll switch the
  backend to scrape `gse.com.gh` (which every cloud can reach) instead.

## Step 1 — DuckDNS subdomain

1. At [duckdns.org](https://www.duckdns.org), create a subdomain, e.g. `gse-tracker`
   → gives you `gse-tracker.duckdns.org`.
2. Leave it for now; you'll set its IP in Step 2 once the instance is up.

## Step 2 — Launch the EC2 instance

1. EC2 → **Launch instance**.
2. **AMI:** Ubuntu Server 24.04 LTS. **Type:** `t2.micro` (or `t3.micro`).
3. **Key pair:** create/download one (you'll SSH with it).
4. **Network / security group — open these inbound ports:**
   - SSH `22` (your IP)
   - HTTP `80` (anywhere)
   - HTTPS `443` (anywhere)
5. Launch. Copy the instance's **Public IPv4 address**.
6. Back at DuckDNS, set your subdomain's IP to that public IPv4 and **Update**.

## Step 3 — Provision the app

SSH in (replace with your key and IP):

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

Then:

```bash
sudo apt-get update -y && sudo apt-get install -y git
git clone https://github.com/AdomBoateng/gse-tracker-bot.git
cd gse-tracker-bot
bash deploy/setup.sh gse-tracker.duckdns.org you@example.com
```

`setup.sh` installs Node 22 / Python / nginx / certbot, builds the frontend,
runs the backend as a systemd service, wires up nginx, and gets the Let's
Encrypt cert. It re-runs the Step 0 reachability check and warns if the IP is
blocked.

## Step 4 — Verify

- Open **https://gse-tracker.duckdns.org** — the padlock should be valid and the
  companies table populated with live prices.
- Backend health: `curl http://127.0.0.1:8000/health` → `{"status":"healthy"}`
- Live data locally: `curl -s http://127.0.0.1:8000/api/v1/gse/live | head -c 200`

---

## Updating after you push new code

```bash
cd ~/gse-tracker-bot
git pull
# frontend
cd frontend && npm install && npm run build && cd ..
# backend deps (if requirements changed)
./backend/.venv/bin/pip install -r backend/requirements.txt
sudo systemctl restart gse-tracker-api
```

nginx serves the freshly built `frontend/dist` automatically; no nginx reload
needed unless you change `deploy/nginx.conf.template`.

## Operating notes

- **Logs:** `sudo journalctl -u gse-tracker-api -f`
- **Restart backend:** `sudo systemctl restart gse-tracker-api`
- **Cert renewal:** certbot installs a renewal timer automatically (certs last 90
  days). Check with `sudo certbot renew --dry-run`.
- **DuckDNS IP:** if you stop/start the instance, its public IP changes (unless
  you attach an Elastic IP). Update the IP at DuckDNS, or attach an Elastic IP to
  keep it stable.
- **Persistent data:** the SQLite DB (`backend/gse_tracker.db`) lives on the
  instance disk and persists across restarts, so composite history and cached
  news accumulate over time.
- **Cost:** free for 12 months within the `t2.micro` 750 hrs/month allowance;
  after that (or beyond the allowance) the instance is billable.
