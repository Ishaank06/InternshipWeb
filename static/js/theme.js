/**
 * Academia-Industry Collaboration Portal (SkillLink)
 * Theme JavaScript & Interactive UX Helpers
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbarScroll();
  initPasswordToggles();
  initAlertAutoDismiss();
  initAnimatedCounters();
  initSubmitButtonLoading();
});

/**
 * Navbar elevation and frosted glass effect on scroll
 */
function initNavbarScroll() {
  const navbarContainer = document.querySelector('.navbar-floating-container') || document.querySelector('.navbar-premium');
  if (!navbarContainer) return;

  const handleScroll = () => {
    if (window.scrollY > 15) {
      navbarContainer.classList.add('scrolled');
    } else {
      navbarContainer.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // Trigger initial check
}

/**
 * Password Visibility Toggle
 */
function initPasswordToggles() {
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach((input) => {
    // Check if toggle already exists
    const parent = input.parentElement;
    if (parent && !parent.querySelector('.password-toggle-btn')) {
      // Add relative wrapper class if needed
      parent.classList.add('password-field-wrapper');
      
      const toggleBtn = document.createElement('button');
      toggleBtn.type = 'button';
      toggleBtn.className = 'password-toggle-btn';
      toggleBtn.setAttribute('aria-label', 'Toggle password visibility');
      toggleBtn.innerHTML = '<i class="bi bi-eye"></i>';

      toggleBtn.addEventListener('click', () => {
        if (input.type === 'password') {
          input.type = 'text';
          toggleBtn.innerHTML = '<i class="bi bi-eye-slash"></i>';
        } else {
          input.type = 'password';
          toggleBtn.innerHTML = '<i class="bi bi-eye"></i>';
        }
      });

      parent.appendChild(toggleBtn);
    }
  });
}

/**
 * Auto-dismiss alerts after 5 seconds with smooth fade
 */
function initAlertAutoDismiss() {
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-6px)';
      setTimeout(() => alert.remove(), 400);
    }, 5500);
  });
}

/**
 * Animated Number Counter for Dashboard Metrics
 */
function initAnimatedCounters() {
  // Check if reduced motion is preferred
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const counters = document.querySelectorAll('.stat-number[data-count]');
  counters.forEach((counter) => {
    const target = parseFloat(counter.getAttribute('data-count'));
    const isPercentage = counter.getAttribute('data-is-pct') === 'true';
    if (isNaN(target)) return;

    let start = 0;
    const duration = 1200; // ms
    const startTime = performance.now();

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const currentVal = Math.floor(easeProgress * target);

      counter.textContent = currentVal + (isPercentage ? '%' : '');

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = (isPercentage ? target + '%' : target);
      }
    }

    requestAnimationFrame(updateCounter);
  });
}

/**
 * Add subtle loading state on forms upon submission
 */
function initSubmitButtonLoading() {
  const forms = document.querySelectorAll('form:not(.no-spin)');
  forms.forEach((form) => {
    form.addEventListener('submit', () => {
      const submitBtn = form.querySelector('button[type="submit"]:not(.no-spin)');
      if (submitBtn && !submitBtn.disabled) {
        // Prevent double click
        setTimeout(() => {
          submitBtn.disabled = true;
          const originalHtml = submitBtn.innerHTML;
          submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Processing...`;
        }, 50);
      }
    });
  });
}
