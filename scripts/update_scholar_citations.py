#!/usr/bin/env python3
"""
Update only citation statistics (for daily updates)
"""

import re
from scholarly import scholarly
import sys

# Your Google Scholar ID
SCHOLAR_ID = 'ULBrgQcAAAAJ'

def get_citation_data():
    """Fetch only citation data from Google Scholar"""
    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author)
        
        citations = author.get('citedby', 0)
        h_index = author.get('hindex', 0)
        i10_index = author.get('i10index', 0)
        
        cites_per_year = author.get('cites_per_year', {})
        years = sorted(cites_per_year.keys())
        citation_counts = [cites_per_year[year] for year in years]
        
        return {
            'citations': citations,
            'h_index': h_index,
            'i10_index': i10_index,
            'years': years,
            'citation_counts': citation_counts
        }
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def update_index_html(data):
    """Update index.html with new stats"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
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

def update_citation_graph(data):
    """Update citation graph in scholar.js"""
    try:
        with open('scholar.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        import json
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
        
        with open('scholar.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Updated scholar.js citation graph")
        return True
    except Exception as e:
        print(f"Error updating scholar.js: {e}", file=sys.stderr)
        return False

def main():
    print("Fetching Google Scholar citation data...")
    data = get_citation_data()
    
    if not data:
        print("Failed to fetch data")
        sys.exit(1)
    
    print(f"Found: {data['citations']} citations, h-index: {data['h_index']}, i10-index: {data['i10_index']}")
    
    success = True
    success &= update_index_html(data)
    success &= update_citation_graph(data)
    
    if success:
        print("\n✓ Citation data updated successfully!")
        sys.exit(0)
    else:
        print("\n✗ Failed to update citation data")
        sys.exit(1)

if __name__ == '__main__':
    main()
