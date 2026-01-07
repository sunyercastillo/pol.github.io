#!/usr/bin/env python3
"""
Automatically fetch Google Scholar data and update website files
"""

import json
import re
from scholarly import scholarly
import sys

# Your Google Scholar ID
SCHOLAR_ID = 'ULBrgQcAAAAJ'

def get_scholar_data():
    """Fetch data from Google Scholar"""
    try:
        # Search for author by ID
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author)
        
        # Extract citation data
        citations = author.get('citedby', 0)
        h_index = author.get('hindex', 0)
        i10_index = author.get('i10index', 0)
        
        # Extract yearly citations
        cites_per_year = author.get('cites_per_year', {})
        years = sorted(cites_per_year.keys())
        citation_counts = [cites_per_year[year] for year in years]
        
        # Get publications
        publications = []
        for pub in author.get('publications', [])[:10]:  # Get top 10
            pub_filled = scholarly.fill(pub)
            publications.append({
                'title': pub_filled.get('bib', {}).get('title', 'Untitled'),
                'authors': pub_filled.get('bib', {}).get('author', ''),
                'venue': pub_filled.get('bib', {}).get('venue', pub_filled.get('bib', {}).get('journal', 'Unknown')),
                'year': pub_filled.get('bib', {}).get('pub_year', ''),
                'link': pub_filled.get('pub_url', pub_filled.get('eprint_url', '#'))
            })
        
        return {
            'citations': citations,
            'h_index': h_index,
            'i10_index': i10_index,
            'years': years,
            'citation_counts': citation_counts,
            'publications': publications
        }
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def update_index_html(data):
    """Update index.html with new stats"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update citation stats
        content = re.sub(
            r'(<div class="stat-item">\s*<div class="stat-number">)\d+(</div>\s*<div class="stat-label">Citations</div>)',
            f'\\g<1>{data["citations"]}\\g<2>',
            content
        )
        content = re.sub(
            r'(<div class="stat-item">\s*<div class="stat-number">)\d+(</div>\s*<div class="stat-label">h-index</div>)',
            f'\\g<1>{data["h_index"]}\\g<2>',
            content
        )
        content = re.sub(
            r'(<div class="stat-item">\s*<div class="stat-number">)\d+(</div>\s*<div class="stat-label">i10-index</div>)',
            f'\\g<1>{data["i10_index"]}\\g<2>',
            content
        )
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Updated index.html")
        return True
    except Exception as e:
        print(f"Error updating index.html: {e}", file=sys.stderr)
        return False

def update_scholar_js(data):
    """Update scholar.js with new publications and citation data"""
    try:
        with open('scholar.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update citation data
        citation_data_str = f'''const citationData = {{
    years: {json.dumps(data['years'])},
    citations: {json.dumps(data['citation_counts'])}
}};'''
        
        content = re.sub(
            r'const citationData = \{[^}]+\};',
            citation_data_str,
            content,
            flags=re.DOTALL
        )
        
        # Update publications array
        pubs_array = "const publications = [\n"
        for pub in data['publications']:
            # Escape quotes in strings
            title = pub['title'].replace('"', '\\"').replace("'", "\\'")
            authors = pub['authors'].replace('"', '\\"').replace("'", "\\'")
            venue = pub['venue'].replace('"', '\\"').replace("'", "\\'")
            
            pubs_array += f'''    {{
        title: "{title}",
        authors: "{authors}",
        venue: "{venue}",
        year: "{pub['year']}",
        link: "{pub['link']}"
    }},\n'''
        
        pubs_array += "];"
        
        content = re.sub(
            r'const publications = \[[^\]]*\];',
            pubs_array,
            content,
            flags=re.DOTALL
        )
        
        with open('scholar.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Updated scholar.js")
        return True
    except Exception as e:
        print(f"Error updating scholar.js: {e}", file=sys.stderr)
        return False

def main():
    print("Fetching Google Scholar data...")
    data = get_scholar_data()
    
    if not data:
        print("Failed to fetch data")
        sys.exit(1)
    
    print(f"Found: {data['citations']} citations, h-index: {data['h_index']}, i10-index: {data['i10_index']}")
    print(f"Publications: {len(data['publications'])}")
    
    success = True
    success &= update_index_html(data)
    success &= update_scholar_js(data)
    
    if success:
        print("\n✓ All files updated successfully!")
        sys.exit(0)
    else:
        print("\n✗ Some files failed to update")
        sys.exit(1)

if __name__ == '__main__':
    main()
