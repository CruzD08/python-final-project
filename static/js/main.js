/* ============================================================
   Blue Bloom Travel — main.js
   Two things this file does:
   1. Mobile navbar toggle (hamburger button ☰)
   2. Fade-in animation when elements scroll into view
   ============================================================ */


/* ── 1. Mobile Navbar Toggle ─────────────────────────────── */
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', function () {
    navLinks.classList.toggle('open');
  });

  // Close the menu if user clicks anywhere outside of it
  document.addEventListener('click', function (e) {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
    }
  });
}


/* ── 2. Scroll Fade-In Animation ─────────────────────────── */

const fadeEls = document.querySelectorAll('.fade-up');

if (fadeEls.length > 0) {
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // stop watching once visible
      }
    });
  }, { threshold: 0.12 });

  fadeEls.forEach(function (el) {
    observer.observe(el);
  });
}


/* ── 3. Flash Message Close Button ──────────────────────────*/
/*
   Clicking the × button on a flash message removes it from the page.
*/
document.querySelectorAll('.flash-close').forEach(function (btn) {
  btn.addEventListener('click', function () {
    btn.closest('.flash').remove();
  });
});




/* ── Hero Carousel ───────────────────────────────────────── */
const slides = document.querySelectorAll('.slide');
const dots   = document.querySelectorAll('.dot');
let current  = 0;

function goToSlide(n) {
  // remove active class from current slide and dot
  slides[current].classList.remove('active');
  dots[current].classList.remove('active');
  // change to the new one
  current = n;
  slides[current].classList.add('active');
  dots[current].classList.add('active');
}


if (slides.length > 0) {
  setInterval(function () {
    let next = (current + 1) % slides.length;
    goToSlide(next);
  }, 4000);
}
