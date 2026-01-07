// Google Scholar Configuration
const SCHOLAR_USER_ID = 'ULBrgQcAAAAJ';
const SCHOLAR_BASE_URL = 'https://scholar.google.es/citations';

// Function to create publication HTML
function createPublicationHTML(title, authors, venue, year, link) {
    return `
        <div class="publication-item">
            <h3>${title}</h3>
            <p class="authors">${authors}</p>
            <p class="journal">${venue} (${year})</p>
            <a href="${link}" target="_blank" class="publication-link">View Publication</a>
        </div>
    `;
}

// Note: Due to CORS restrictions, we cannot directly fetch from Google Scholar
// The best solution is to use one of these approaches:

// Option 1: Manual publication list (recommended for reliability)
const publications = [
    {
        title: "Your Publication Title",
        authors: "Author 1, Author 2, P. Suñer-Castillo",
        venue: "Journal Name",
        year: "2024",
        link: "https://doi.org/your-doi"
    },
    // Add more publications here
];

// Option 2: Use Google Scholar embed (if available)
function loadPublications() {
    const publicationsList = document.getElementById('publications-list');
    
    if (!publicationsList) return;
    
    // Check if we have manual publications
    if (publications.length > 0) {
        publicationsList.innerHTML = '';
        publications.forEach(pub => {
            publicationsList.innerHTML += createPublicationHTML(
                pub.title,
                pub.authors,
                pub.venue,
                pub.year,
                pub.link
            );
        });
    } else {
        // Fallback: Show message to visit Google Scholar
        publicationsList.innerHTML = `
            <div class="publication-item">
                <h3>View My Publications</h3>
                <p class="authors">For the most up-to-date list of publications</p>
                <a href="${SCHOLAR_BASE_URL}?user=${SCHOLAR_USER_ID}&hl=es" target="_blank" class="publication-link">
                    Visit my Google Scholar Profile
                </a>
            </div>
        `;
    }
}

// Load publications when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadPublications);
} else {
    loadPublications();
}
