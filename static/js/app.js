document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const searchText = document.querySelector('.search-text');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const modelBtns = document.querySelectorAll('.model-btn');
    const metricsSection = document.getElementById('metrics-section');
    const toggleMetricsBtn = document.getElementById('toggle-metrics');
    const metricsGrid = document.getElementById('metrics-grid');
    const searchResults = document.getElementById('search-results');
    
    // State
    let activeModel = 'vector';
    let showMetrics = true;
    
    // Event Listeners
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Model selection
    modelBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active model
            modelBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeModel = btn.dataset.model;
            
            // If we already have results, refresh the search with new model
            if (!searchResults.innerHTML.trim() == '') {
                performSearch();
            }
        });
    });
    
    // Toggle metrics display
    toggleMetricsBtn.addEventListener('click', () => {
        const metricsContent = metricsGrid;
        
        if (showMetrics) {
            metricsContent.style.display = 'none';
            toggleMetricsBtn.textContent = 'Show';
        } else {
            metricsContent.style.display = 'grid';
            toggleMetricsBtn.textContent = 'Hide';
        }
        
        showMetrics = !showMetrics;
    });
    
    // Search function
    async function performSearch() {
        const query = searchInput.value.trim();
        
        if (!query) {
            return;
        }
        
        // Show loading state
        setLoading(true);
        
        try {
            // Build API URL
            const apiUrl = `/api/search?query=${encodeURIComponent(query)}&model=${activeModel}`;
            
            // Fetch results
            const response = await fetch(apiUrl);
            
            if (!response.ok) {
                throw new Error('Search request failed');
            }
            
            const data = await response.json();
            
            // Display results
            displayResults(data);
            
        } catch (error) {
            console.error('Search error:', error);
            searchResults.innerHTML = `
                <div class="result-item">
                    <p>Sorry, an error occurred while searching. Please try again.</p>
                </div>
            `;
        } finally {
            setLoading(false);
        }
    }
    
    // Toggle loading state
    function setLoading(isLoading) {
        if (isLoading) {
            searchText.classList.add('hidden');
            loadingSpinner.classList.remove('hidden');
            searchBtn.disabled = true;
        } else {
            searchText.classList.remove('hidden');
            loadingSpinner.classList.add('hidden');
            searchBtn.disabled = false;
        }
    }
    
    // Display search results
    function displayResults(data) {
        // Display metrics
        displayMetrics(data);
        
        // Create query keywords section if available
        let queryKeywordsHtml = '';
        if (data.query_keywords && data.query_keywords.length > 0) {
            queryKeywordsHtml = `
                <div class="query-keywords">
                    <p class="query-keywords-title">Extracted Query Keywords:</p>
                    <div class="query-keywords-tags">
                        ${data.query_keywords.map(keyword => `
                            <span class="entity-tag query-keyword-tag">${keyword}</span>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // Display result items
        const resultsHtml = `
            ${queryKeywordsHtml}
            ${data.results.map(result => `
                <div class="result-item">
                    <h3 class="result-title">${result.title}</h3>
                    <p class="result-snippet">${result.snippet}</p>
                    <div class="result-footer">
                        <div class="result-entities">
                            ${result.entities.map(entity => `
                                <span class="entity-tag">${entity}</span>
                            `).join('')}
                        </div>
                        <div class="result-score">
                            <i data-feather="file-text"></i>
                            <span>Score: ${result.score.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        `;
        
        searchResults.innerHTML = resultsHtml;
        
        // Re-initialize Feather icons for dynamic content
        feather.replace();
    }
    
    // Display metrics cards
    function displayMetrics(data) {
        const { time_taken, metrics } = data;
        
        const metricsHtml = `
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="clock"></i>
                    <span>Time</span>
                </div>
                <div class="metric-value">${time_taken.toFixed(3)}s</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="award"></i>
                    <span>Precision</span>
                </div>
                <div class="metric-value">${metrics.precision.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="award"></i>
                    <span>Recall</span>
                </div>
                <div class="metric-value">${metrics.recall.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="award"></i>
                    <span>F1 Score</span>
                </div>
                <div class="metric-value">${metrics.f1_score.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="bar-chart-2"></i>
                    <span>MRR</span>
                </div>
                <div class="metric-value">${metrics.mean_reciprocal_rank.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="bar-chart-2"></i>
                    <span>NDCG</span>
                </div>
                <div class="metric-value">${metrics.ndcg.toFixed(2)}</div>
            </div>
        `;
        
        metricsGrid.innerHTML = metricsHtml;
        metricsSection.classList.remove('hidden');
        
        // Re-initialize Feather icons for dynamic content
        feather.replace();
    }
});
    // Toggle loading state
    function setLoading(isLoading) {
        if (isLoading) {
            searchText.classList.add('hidden');
            loadingSpinner.classList.remove('hidden');
            searchBtn.disabled = true;
        } else {
            searchText.classList.remove('hidden');
            loadingSpinner.classList.add('hidden');
            searchBtn.disabled = false;
        }
    }
    
    // Display search results
    function displayResults(data) {
        // Display metrics
        displayMetrics(data);
        
        // Display result items
        const resultsHtml = data.results.map(result => `
            <div class="result-item">
                <h3 class="result-title">${result.title}</h3>
                <p class="result-snippet">${result.snippet}</p>
                <div class="result-footer">
                    <div class="result-entities">
                        ${result.entities.map(entity => `
                            <span class="entity-tag">${entity}</span>
                        `).join('')}
                    </div>
                    <div class="result-score">
                        <i data-feather="file-text"></i>
                        <span>Score: ${result.score.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `).join('');
        
        searchResults.innerHTML = resultsHtml;
        
        // Re-initialize Feather icons for dynamic content
        feather.replace();
    }
    
    // Display metrics cards
    function displayMetrics(data) {
        const { time_taken, metrics } = data;
        
        const metricsHtml = `
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="clock"></i>
                    <span>Time</span>
                </div>
                <div class="metric-value">${time_taken.toFixed(3)}s</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="award"></i>
                    <span>Precision</span>
                </div>
                <div class="metric-value">${metrics.precision.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="award"></i>
                    <span>Recall</span>
                </div>
                <div class="metric-value">${metrics.recall.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="award"></i>
                    <span>F1 Score</span>
                </div>
                <div class="metric-value">${metrics.f1_score.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="bar-chart-2"></i>
                    <span>MRR</span>
                </div>
                <div class="metric-value">${metrics.mean_reciprocal_rank.toFixed(2)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">
                    <i data-feather="bar-chart-2"></i>
                    <span>NDCG</span>
                </div>
                <div class="metric-value">${metrics.ndcg.toFixed(2)}</div>
            </div>
        `;
        
        metricsGrid.innerHTML = metricsHtml;
        metricsSection.classList.remove('hidden');
        
        // Re-initialize Feather icons for dynamic content
        feather.replace();
    }

