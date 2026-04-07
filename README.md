# VIT Campus Energy Dashboard

An interactive dashboard built from the provided energy utility assignment data.

## Files

- `app.py` — Streamlit dashboard app
- `data/energy_consumption.csv` — block consumption and load driver data
- `data/energy_initiatives.csv` — energy initiative savings estimates
- `data/energy_reconciliation.csv` — reported vs modeled reconciliation
- `requirements.txt` — Python dependencies

## Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Streamlit dashboard:
   ```bash
   python -m streamlit run app.py
   ```

## Shareable Dashboard

You can open `dashboard.html` directly in any browser. The file is fully standalone and can also be published on GitHub Pages, Netlify, or any static site host.

## GitHub Pages Deployment

This repository includes a GitHub Actions workflow that deploys the contents of `docs/` as a GitHub Pages site.

To deploy:

1. Initialize the repository locally:
   ```powershell
   git init
   git add .
   git commit -m "Initial dashboard deployment"
   ```
2. Create a repository on GitHub and add it as a remote, e.g.:
   ```powershell
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```
3. Enable GitHub Pages in the repository settings, if not automatic.

The static site will then be served from the `docs/` folder. Your published site URL will typically be:

- `https://<your-username>.github.io/<repo-name>/`

## Notes

- The dashboard uses the values and insights extracted from `REM_ASSIGNMENT 3(Raj Makwana) (1).docx`.
- It includes block-level consumption, driver breakdown, reconciliation and initiative savings.
