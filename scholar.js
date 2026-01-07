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
        title: "REE ultra-rich karst bauxite deposits in the Pedernales Peninsula, Dominican Republic: Mineralogy of REE phosphates and carbonates",
        authors: "Cristina Villanova-de-Benavent and Joaquín A Proenza and Lisard Torró and Thomas Aiglsperger and Cristina Domènech and Diego Domínguez-Carretero and Xavier Llovet and Pol Suñer and Jesús Rodríguez",
        venue: "Ore Geology Reviews",
        year: "2023",
        link: "https://doi.org/10.1016/j.oregeorev.2023.105422"
    },
];

// Citation data by year (update with your actual data from Google Scholar)
const citationData = {
    years: [2023, 2024, 2025],
    citations: [2, 2, 13]
};

// Function to create citation graph
function createCitationGraph() {
    const canvas = document.getElementById('citationChart');
    
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: citationData.years,
            datasets: [{
                label: 'Citations',
                data: citationData.citations,
                backgroundColor: 'rgba(52, 152, 219, 0.6)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 2,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + ' citations';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

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
    document.addEventListener('DOMContentLoaded', () => {
        loadPublications();
        createCitationGraph();
    });
} else {
    loadPublications();
    createCitationGraph();
}
