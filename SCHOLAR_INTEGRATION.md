# Google Scholar Integration Guide

## How to Keep Your Publications Updated

Due to Google Scholar's CORS restrictions, there are three ways to keep your publications updated:

### Option 1: Manual Updates (Current - Most Reliable)

Edit `scholar.js` and update the `publications` array with your papers:

```javascript
const publications = [
    {
        title: "Your Paper Title",
        authors: "Author 1, Author 2, P. Suñer-Castillo",
        venue: "Journal Name",
        year: "2024",
        link: "https://doi.org/your-doi-or-scholar-link"
    },
    // Add more publications
];
```

### Option 2: Use a Third-Party Service

Services like **Zotero**, **Scholarcy**, or **Publons** can provide embeddable publication lists:

1. Export your Google Scholar publications
2. Import to Zotero or similar
3. Generate an embed code
4. Add to your website

### Option 3: GitHub Actions (Automated - Advanced)

Create a GitHub Action that periodically scrapes your Google Scholar profile and updates the publications:

1. Use `serpapi` or `scholarly` Python library
2. Set up GitHub Action to run weekly
3. Automatically commit updates to `scholar.js`

## Quick Start

To add your first publication:

1. Open `scholar.js`
2. Find the `publications` array
3. Add your publication details
4. Commit and push

Your website will automatically display the publications!

## Getting Publication Links from Google Scholar

1. Visit your [Google Scholar profile](https://scholar.google.es/citations?user=ULBrgQcAAAAJ&hl=es)
2. Click on each publication
3. Copy the link or DOI
4. Add to the publications array in `scholar.js`
