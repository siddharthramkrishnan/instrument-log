# Engineering Instrument Usage Log

One QR code per instrument → opens a pre-filled mobile log form → saves to Google Sheets.

---

## Setup (one-time, ~15 minutes)

### Step 1 — Set up Google Sheets + Apps Script

1. Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet.
   Name it: **Instrument Usage Log**

2. Go to **Extensions → Apps Script**

3. Delete the default code, paste everything from `apps_script.gs`

4. Click **Save** (💾), then click **Deploy → New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone** (so phones can submit without login)
   - Click **Deploy** → copy the Web App URL (looks like `https://script.google.com/macros/s/ABC.../exec`)

5. Run the `testSetup()` function once from the editor to verify the sheet gets created.

---

### Step 2 — Add your Apps Script URL to all pages

In your terminal, run this from inside the `instrument-log/` folder:

```bash
# Replace YOUR_APPS_SCRIPT_URL with the URL from Step 1
find log/ -name "*.html" -exec sed -i "s|REPLACE_WITH_APPS_SCRIPT_URL|YOUR_APPS_SCRIPT_URL|g" {} \;
```

Or on macOS (BSD sed):
```bash
find log/ -name "*.html" -exec sed -i '' "s|REPLACE_WITH_APPS_SCRIPT_URL|YOUR_APPS_SCRIPT_URL|g" {} \;
```

---

### Step 3 — Deploy to GitHub Pages

1. Go to [github.com](https://github.com) → **New repository**
   - Name: `instrument-log` (or anything you like)
   - Set to **Public**
   - Click **Create repository**

2. Push the files:
```bash
cd instrument-log/
git init
git add .
git commit -m "Initial deploy"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/instrument-log.git
git push -u origin main
```

3. In the repo on GitHub: **Settings → Pages → Source: main branch → Save**

4. Your site will be live at:
   `https://YOUR-USERNAME.github.io/instrument-log`

---

### Step 4 — Generate & Print QR Codes

1. Open `generate_qr_sheet.html` in your browser (just double-click it)
2. Enter your GitHub Pages URL: `https://YOUR-USERNAME.github.io/instrument-log`
3. Click **Generate QR Codes**
4. Click **Print / Save PDF**
5. Cut and laminate — stick one on each instrument!

---

## File Structure

```
instrument-log/
├── index.html              ← instrument list (home page)
├── log/
│   ├── eng_mfg_001.html    ← MFG instruments (77 files)
│   ├── eng_mfg_002.html
│   ├── ...
│   ├── eng_d_d_001.html    ← D&D instruments (61 files)
│   └── ...
├── apps_script.gs          ← paste into Google Apps Script
├── generate_qr_sheet.html  ← printable QR code sheet generator
└── README.md               ← this file
```

## QR URL format

Each QR code links to:
`https://YOUR-USERNAME.github.io/instrument-log/log/eng_mfg_001.html`

The page opens with the instrument pre-filled. The person enters only:
- Their **name** (required)
- **Purpose** (tap chips)
- **Date/time** (auto-filled to now)
- Condition + Remarks (optional)

Entries appear instantly in Google Sheets.
