document.addEventListener('DOMContentLoaded', () => {
    // Dark mode toggle
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    document.documentElement.setAttribute('data-theme', currentTheme);
    if(themeToggle) {
        themeToggle.innerHTML = currentTheme === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-stars-fill"></i>';
        
        themeToggle.addEventListener('click', () => {
            const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            themeToggle.innerHTML = theme === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-stars-fill"></i>';
            
            // Dispatch event for Chart.js to update colors if needed
            window.dispatchEvent(new Event('themeChanged'));
        });
    }

    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    if(sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
    }
    
    // Notifications read
    const markReadBtn = document.getElementById('mark-read-btn');
    if(markReadBtn) {
        markReadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fetch('/api/notifications/read', {
                method: 'POST',
            }).then(response => response.json())
              .then(data => {
                  if(data.success) {
                      document.getElementById('notification-badge').style.display = 'none';
                      location.reload();
                  }
              });
        });
    }
    
    // Global Search (Simple redirect based on select)
    const searchInput = document.getElementById('global-search');
    if(searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') {
                e.preventDefault();
                // Simple implementation: redirect to my-tasks with query filter if needed
                // Currently backend doesn't fully support text search in a single endpoint
                // We'll redirect to My Tasks as a placeholder
                window.location.href = '/my-tasks?search=' + encodeURIComponent(searchInput.value);
            }
        });
    }
});
