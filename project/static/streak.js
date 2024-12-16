// Toggle visibility of the Last 4 Weeks section
function toggleWeeklyData() {
    const last4Weeks = document.getElementById('last-4-weeks');
    const isHidden = last4Weeks.style.display === "none";
    last4Weeks.style.display = isHidden ? "block" : "none";
}

// Toggle between light and dark modes with a smooth transition
function toggleMode() {
    const body = document.body;
    const isDark = body.classList.contains('dark-mode');
    
    body.classList.toggle('dark-mode', !isDark);
    body.classList.toggle('light-mode', isDark);
    
    // Update toggle button status
    document.getElementById('toggleButton').checked = !isDark;
    
    // Save theme preference
    localStorage.setItem('mode', isDark ? 'light' : 'dark');
}

// Set initial theme based on localStorage
document.addEventListener('DOMContentLoaded', function () {
    const savedMode = localStorage.getItem('mode') || 'light';
    document.body.classList.add(savedMode + '-mode');
    document.getElementById('toggleButton').checked = savedMode === 'dark';
});



