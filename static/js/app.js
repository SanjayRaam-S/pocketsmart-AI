/**
 * PocketSmart AI - Global Application Helpers
 */

// Toast Notifications System
function showToast(message, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === 'success' ? '✓ ' : type === 'danger' ? '⚠️ ' : 'ℹ️ ';
  toast.innerHTML = `
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <span>${icon}</span>
      <span>${message}</span>
    </div>
    <button style="background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #94a3b8; margin-left: 0.75rem;" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Global Logout function
async function handleLogout() {
  try {
    const res = await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/login?logged_out=1';
  } catch (err) {
    console.error('Logout error:', err);
    window.location.href = '/login';
  }
}

// Mobile Navbar Toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }
});
