/* Le 9 · petites interactions, sans dépendance */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  // --- Menu mobile ---
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // --- En-tête : filet au défilement ---
  var topbar = document.querySelector('.topbar');
  function onScroll() {
    if (topbar) topbar.classList.toggle('is-scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // --- Photos : tant que le fichier n'existe pas, on garde l'étiquette "à ajouter" ---
  document.querySelectorAll('.ph img').forEach(function (img) {
    var fig = img.closest('.ph');
    function ok() { fig.classList.add('has-img'); }
    function ko() { img.remove(); }
    if (img.complete) { img.naturalWidth > 0 ? ok() : ko(); }
    else { img.addEventListener('load', ok); img.addEventListener('error', ko); }
  });

  // --- Lien de navigation actif + apparition douce ---
  if ('IntersectionObserver' in window) {
    var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
    var sections = links.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id); });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { spy.observe(s); });

    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); reveal.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { reveal.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }

  // --- Année du pied de page ---
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());
})();
