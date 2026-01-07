# Google Scholar Auto-Update

This setup automatically fetches and updates your Google Scholar data daily.

## How It Works

1. **GitHub Action** runs daily at 2 AM UTC (`.github/workflows/update-scholar.yml`)
2. **Python script** fetches your Google Scholar data (`scripts/update_scholar_data.py`)
3. **Auto-commits** changes to `index.html` and `scholar.js`

## What Gets Updated Automatically

- ✅ Total Citations
- ✅ h-index
- ✅ i10-index  
- ✅ Citation graph (citations per year)
- ✅ Publication list (top 10 papers)

## Manual Trigger

You can also manually trigger the update:

1. Go to: https://github.com/sunyercastillo/pol.github.io/actions
2. Click "Update Google Scholar Data"
3. Click "Run workflow"

## Testing Locally

To test the script locally before pushing:

```bash
cd /Users/polsuka/Documents/GitHub/pol.github.io
pip install scholarly beautifulsoup4 requests
python3 scripts/update_scholar_data.py
```

## Configuration

Your Google Scholar ID is set to: `ULBrgQcAAAAJ`

To change it, edit `scripts/update_scholar_data.py` line 9.

## Notes

- The action runs automatically every day
- Changes are committed with message: "Auto-update Google Scholar data [skip ci]"
- The `[skip ci]` prevents infinite loops
- First run may take a few minutes as it scrapes Google Scholar
