const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('#menu-principal');

if (menuToggle && navMenu) {
  menuToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const targetId = link.getAttribute('href');
    if (!targetId || targetId === '#') return;

    const target = document.querySelector(targetId);

    if (target) {
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

const sections = document.querySelectorAll('main section[id], header[id]');
const navLinks = document.querySelectorAll('.nav-links a');

const updateActiveLink = () => {
  if (!sections.length) return;

  let currentId = 'inicio';
  sections.forEach((section) => {
    if (window.scrollY >= section.offsetTop - 140) currentId = section.id;
  });

  navLinks.forEach((link) => {
    const href = link.getAttribute('href') || '';
    link.classList.toggle('active', href === `#${currentId}` || href.endsWith(`#${currentId}`));
  });
};

window.addEventListener('scroll', updateActiveLink, { passive: true });
updateActiveLink();
