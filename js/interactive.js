// Interactive functionality for the Global Internet Censorship Report
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Region selector functionality
    document.getElementById('region-select').addEventListener('change', function() {
        const region = this.value;
        const maps = document.querySelectorAll('#map-container img');
        
        maps.forEach(map => {
            map.classList.add('d-none');
        });
        
        document.getElementById(`${region}-map`).classList.remove('d-none');
    });

    // Shutdown filter functionality
    const electionCheckbox = document.getElementById('election-checkbox');
    const protestCheckbox = document.getElementById('protest-checkbox');
    
    function updateShutdownFilters() {
        // In a full implementation, this would dynamically filter the timeline
        // For now, we'll just log the state
        console.log('Filters:', {
            elections: electionCheckbox.checked,
            protests: protestCheckbox.checked
        });
        
        // Visual feedback to show the feature would work
        const timelineImg = document.querySelector('#shutdown-timeline');
        if (timelineImg) {
            if (!electionCheckbox.checked && !protestCheckbox.checked) {
                timelineImg.style.opacity = 0.3;
            } else if (!electionCheckbox.checked || !protestCheckbox.checked) {
                timelineImg.style.opacity = 0.7;
            } else {
                timelineImg.style.opacity = 1;
            }
        }
    }
    
    electionCheckbox.addEventListener('change', updateShutdownFilters);
    protestCheckbox.addEventListener('change', updateShutdownFilters);

    // Timeline zoom functionality
    document.querySelectorAll('#zoom-2023, #zoom-2024, #zoom-all').forEach(button => {
        button.addEventListener('click', function() {
            // Visual feedback for the zoom buttons
            document.querySelectorAll('#zoom-2023, #zoom-2024, #zoom-all').forEach(btn => {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-outline-secondary');
            });
            
            this.classList.remove('btn-outline-secondary');
            this.classList.add('btn-primary');
            
            // In a full implementation, this would adjust the timeline view
            console.log('Timeline zoom to:', this.id.replace('zoom-', ''));
        });
    });

    // Add smooth scrolling for citation links
    document.querySelectorAll('.citation').forEach(citation => {
        citation.addEventListener('click', function() {
            document.getElementById('references').scrollIntoView({ 
                behavior: 'smooth' 
            });
        });
    });

    // Add responsive behavior for mobile devices
    function adjustForMobile() {
        if (window.innerWidth < 768) {
            // Adjust visualization containers for better mobile viewing
            document.querySelectorAll('.viz-container').forEach(container => {
                container.style.overflowX = 'auto';
            });
            
            // Make sure tooltips don't overflow on mobile
            tooltipList.forEach(tooltip => {
                tooltip._config.placement = 'top';
            });
        }
    }
    
    // Run on load and resize
    adjustForMobile();
    window.addEventListener('resize', adjustForMobile);
});
