# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Grace Dividend Tracker is a personal investment dividend tracking web app for a Taiwan-based portfolio. It stores data in Google Sheets (tab: `devidends` — intentional typo preserved) and renders an editable grid of dividend-producing holdings grouped by financial institution.

## Running the App

**Recommended (static, no backend):** Serve `index.html` or `grace-dividend.html` from any HTTP server, e.g.:
```bash
npx serve .          # or python3 -m http.server 8080
```
Opening as `file://` may break Google API calls in some browsers.

**Node.js proxy backend:**
```bash
npm install
npm start            # runs server.js on http://localhost:5000
```

**Python proxy backend:**
```bash
pip install -r requirements.txt
python server.py     # http://localhost:5000
# Windows: run.bat
```

## Architecture: Two Modes, Three HTML Files

There are two distinct architectural modes, and understanding which HTML file uses which mode is critical:

### Mode 1 — Direct Google Sheets API (current/primary)
`grace-dividend.html` and root `index.html` are **identical** self-contained single-page apps. They talk directly to the Google Sheets API v4 from the browser:
- **Read-only** (unauthenticated): uses the hardcoded `API_KEY` with a public GET to the Sheets API
- **Read-write** (after "Sign in"): uses Google Identity Services OAuth2 (`accounts.google.com/gsi/client`) to get an `accessToken`, then PUTs data back to the sheet
- **Fallback**: if the API call fails, the `SEED` constant (a hardcoded snapshot of the data) is shown with a warning status

No server is needed for this mode. The Node.js and Python servers are not involved.

### Mode 2 — Backend proxy (legacy)
`templates/index.html` and `public/index.html` fetch from `/api/data` (a relative URL), which means they require either `server.js` or `server.py` to be running. Those servers scrape the Google Sheet's published HTML (`pubhtml` URL) using cheerio (Node) or BeautifulSoup (Python) and return raw table rows as JSON.

These backend files are an older approach; the direct API mode in `grace-dividend.html`/`index.html` is the authoritative current version.

## Data Model and Computation Logic

The spreadsheet columns are fixed: `Institution | Product | Funding | Monthly Average | ROI% | Frequency`

**Grouping:** Rows are visually grouped by Institution. A non-empty Institution cell starts a new group; subsequent rows with an empty Institution cell belong to the same group.

**Special product rows** (auto-computed, shown with pink background, readonly):
- `TWD` — currency-converted sum of the group's investment rows. The conversion rate is preserved from the existing TWD value: `rate = current_TWD_Funding / sum_of_source_Fundings`. When source rows change, TWD is updated as `round(srcFund * rate)`.
- `Available` — computed as `Deposit_Funding − previous_group's_TWD_Funding`. Only the last institution group is expected to have Deposit/Available rows.

**ROI%** (blue background, readonly): `Monthly Average × 12 / Funding × 100`, formatted as `"X.X%"`. Recalculated automatically whenever Funding or Monthly Average changes.

The recalculation chain on any cell edit: `onCellChange → recalcSummaryRows → recalcAllROIs`.

## Google API Configuration

Hardcoded in both `grace-dividend.html` and `index.html`:
- `CLIENT_ID` — Google OAuth2 client ID
- `API_KEY` — Google Sheets API key (read-only public access)
- `SPREADSHEET_ID` — the target spreadsheet
- `SHEET_NAME = 'devidends'` — the tab name (typo is intentional; the actual sheet tab is named this)
- `RANGE = 'devidends!A:F'`

If the spreadsheet or credentials need to change, update these constants in both HTML files.

## Seasonal Fruit Widget

An IIFE at the bottom of the `<script>` block renders a seasonally appropriate Taiwanese fruit SVG in the bottom-left corner using pure SVG path/shape construction (no external library). The month index (1–12) selects from a `fruits` object; January, February, and December all show strawberry.
