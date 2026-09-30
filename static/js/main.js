// GovPilot Main JavaScript
document.addEventListener('DOMContentLoaded', () => {
  // Mobile Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.app-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // Notification Dropdown Toggle & Auto-read
  const notifBtn = document.getElementById('notif-btn');
  const notifDropdown = document.getElementById('notif-dropdown');
  if (notifBtn && notifDropdown) {
    notifBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      notifDropdown.classList.toggle('active');
    });
    document.addEventListener('click', (e) => {
      if (!notifDropdown.contains(e.target) && e.target !== notifBtn) {
        notifDropdown.classList.remove('active');
      }
    });
  }

  // Tab switcher for Pilot Passport
  const tabButtons = document.querySelectorAll('[data-tab-target]');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab-target');
      
      // Update buttons
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Update contents
      const contents = document.querySelectorAll('.passport-tab-content');
      contents.forEach(c => {
        if (c.id === targetId) {
          c.style.display = 'block';
        } else {
          c.style.display = 'none';
        }
      });
    });
  });

  // Auto-dismiss alert messages after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
});

// Function to mark all notifications as read
function markAllNotificationsRead() {
  fetch('/notifications/read-all', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => res.json()).then(data => {
    if (data.success) {
      const badge = document.querySelector('.badge-count');
      if (badge) badge.style.display = 'none';
      const items = document.querySelectorAll('.notif-item');
      items.forEach(i => i.classList.remove('unread'));
    }
  });
}
