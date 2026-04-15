/* PSU Complaints System - Main JavaScript */

document.addEventListener('DOMContentLoaded', () => {


// ===== NAVBAR MENU TOGGLE =====
const menuBtn = document.querySelector(".mobile-menu-btn");
const mobileMenu = document.getElementById("mobileMenu");

if (menuBtn && mobileMenu) {
  menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    mobileMenu.classList.toggle("active");
  });

  document.addEventListener("click", (e) => {
    if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
      mobileMenu.classList.remove("active");
    }
  });
}

// ===== SIDEBAR TOGGLE (SEPARATE BUTTON) =====
const sidebarBtn = document.querySelector(".mobile-sidebar-btn");
const sidebar = document.querySelector(".sidebar");

if (sidebarBtn && sidebar) {
  sidebarBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });
}

  // ===== User Dropdown =====
  const userAvatar = document.querySelector('.user-avatar');
  const userDropdown = document.querySelector('.user-dropdown');

  if (userAvatar && userDropdown) {
    userAvatar.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('show');
    });
    document.addEventListener('click', () => userDropdown.classList.remove('show'));
  }

  // ===== Star Rating =====
  const ratingContainer = document.querySelector('.star-rating');
  const ratingInput = document.getElementById('rating-value');

  if (ratingContainer && ratingInput) {
    const stars = ratingContainer.querySelectorAll('.star-btn');
    let currentRating = parseInt(ratingInput.value) || 0;

    function updateStars(rating) {
      stars.forEach((btn, idx) => {
        const icon = btn.querySelector('.star-icon');
        if (icon) {
          icon.classList.toggle('filled', idx < rating);
        }
      });
    }

    stars.forEach((btn, idx) => {
      btn.addEventListener('mouseenter', () => updateStars(idx + 1));
      btn.addEventListener('mouseleave', () => updateStars(currentRating));
      btn.addEventListener('click', () => {
        currentRating = idx + 1;
        ratingInput.value = currentRating;
        updateStars(currentRating);
      });
    });

    updateStars(currentRating);
  }

  // ===== File Upload =====
  const uploadArea = document.querySelector('.file-upload-area');
  const fileInput = document.getElementById('file-input');
  const fileList = document.querySelector('.file-list');

  if (uploadArea && fileInput) {
    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));

    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.classList.remove('dragover');
      handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', () => handleFiles(fileInput.files));

    function formatSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / 1048576).toFixed(1) + ' MB';
    }

    function handleFiles(files) {
      if (!fileList) return;
      Array.from(files).forEach(file => {
        if (file.size > 5 * 1024 * 1024) {
          showToast('File "' + file.name + '" exceeds 5MB limit.', 'error');
          return;
        }
        const item = document.createElement('div');
        item.className = 'file-item';
        item.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          <span class="file-item-name">${file.name}</span>
          <span class="file-item-size text-xs text-muted">${formatSize(file.size)}</span>
          <button type="button" class="file-remove" aria-label="Remove file">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        `;
        item.querySelector('.file-remove').addEventListener('click', () => item.remove());
        fileList.appendChild(item);
      });
    }
  }

  // ===== Modals =====
  document.querySelectorAll('[data-modal]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modalId = btn.dataset.modal;
      const modal = document.getElementById(modalId);
      if (modal) modal.classList.add('show');
    });
  });

  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.classList.remove('show');
    });
  });

  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.modal-overlay').classList.remove('show');
    });
  });

  // ===== Auto-dismiss alerts =====
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      alert.style.transition = 'all 0.3s';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // ===== Toast notification =====
  function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = `
        position:fixed;bottom:1.5rem;right:1.5rem;z-index:1000;
        display:flex;flex-direction:column;gap:0.5rem;max-width:320px;
      `;
      document.body.appendChild(container);
    }

    const colors = {
      success: 'var(--green-600)',
      error: '#e53e3e',
      warning: 'var(--gold-600)',
      info: '#2c5282'
    };

    const toast = document.createElement('div');
    toast.style.cssText = `
      background:white;border:1px solid var(--border);border-left:3px solid ${colors[type] || colors.info};
      border-radius:var(--radius);padding:0.875rem 1.125rem;box-shadow:var(--shadow-md);
      font-size:0.875rem;color:var(--text-primary);animation:slideUp 0.2s ease;
      display:flex;align-items:center;gap:0.5rem;
    `;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 4000);
  }

  window.showToast = showToast;

  // ===== Form validation =====
  document.querySelectorAll('form[data-validate]').forEach(form => {
    form.addEventListener('submit', (e) => {
      let valid = true;
      form.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
          valid = false;
          field.style.borderColor = '#e53e3e';
          field.addEventListener('input', () => field.style.borderColor = '', { once: true });
        }
      });
      if (!valid) {
        e.preventDefault();
        showToast('Please fill in all required fields.', 'error');
      }
    });
  });

  // ===== Progress bar animation =====
  document.querySelectorAll('.progress-fill').forEach(bar => {
    const target = bar.dataset.width || bar.style.width;
    bar.style.width = '0';
    setTimeout(() => { bar.style.width = target; }, 100);
  });

  // ===== Active nav link =====
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav a, .sidebar-nav a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ===== Confirm dialogs =====
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', (e) => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  // ===== Role-based form toggle =====
  const roleSelect = document.querySelector('[name="role"]');
  const matricGroup = document.getElementById('matric-group');
  const staffIdGroup = document.getElementById('staffid-group');

  if (roleSelect) {
    function toggleRoleFields() {
      const role = roleSelect.value;
      if (matricGroup) matricGroup.style.display = role === 'student' ? 'block' : 'none';
      if (staffIdGroup) staffIdGroup.style.display = role === 'staff' ? 'block' : 'none';
    }
    roleSelect.addEventListener('change', toggleRoleFields);
    toggleRoleFields();
  }

  // ===== Notification mark as read =====
  document.querySelectorAll('.notif-item[data-notif-id]').forEach(item => {
    if (!item.dataset.read) {
      item.addEventListener('click', () => {
        const id = item.dataset.notifId;
        fetch(`/notifications/${id}/read/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        item.dataset.read = 'true';
        item.classList.remove('notif-unread');
      });
    }
  });

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  // ===== Character counter for textareas =====
  document.querySelectorAll('textarea[maxlength]').forEach(ta => {
    const max = parseInt(ta.getAttribute('maxlength'));
    const counter = document.createElement('div');
    counter.className = 'text-xs text-muted mt-1 text-right';
    ta.parentNode.insertBefore(counter, ta.nextSibling);
    function update() { counter.textContent = `${ta.value.length}/${max}`; }
    ta.addEventListener('input', update);
    update();
  });

});
