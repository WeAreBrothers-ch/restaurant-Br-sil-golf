/* =============================================================================
   Le 9 — interactions du site. Aucune dépendance.
   Tout est facultatif : sans JavaScript, la page reste lisible et navigable.
   ============================================================================= */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- menu ---*/
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    var setMenu = function (open) {
      nav.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Menu');
      document.body.style.overflow = open && window.innerWidth <= 1080 ? 'hidden' : '';
    };
    burger.addEventListener('click', function () {
      setMenu(burger.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1080) setMenu(false); });
  }

  /* ------------------------------------------------- filet de l'en-tête ---*/
  var head = document.querySelector('.head');
  var onScroll = function () { if (head) head.classList.toggle('is-stuck', window.scrollY > 6); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------------------------------------------------- les photos ---
     Tant qu'un fichier n'existe pas, le cadre garde son étiquette : on voit
     quel nom déposer et où. Dès qu'il existe, l'image prend toute la place. */
  var hideEmpty = document.body.getAttribute('data-slots') === 'hide';
  Array.prototype.forEach.call(document.querySelectorAll('.ph'), function (fig) {
    var img = fig.querySelector('img');
    if (!img) return;
    var ok = function () { fig.classList.add('ready'); };
    var ko = function () {
      img.remove();
      // Emplacement facultatif, ou site passé en production : on retire le cadre.
      if (fig.hasAttribute('data-optional') || hideEmpty) fig.classList.add('gone');
    };
    if (img.complete) { img.naturalWidth > 0 ? ok() : ko(); }
    else { img.addEventListener('load', ok); img.addEventListener('error', ko); }
  });

  /* ----------------------------------- apparitions et sommaire actif ---*/
  if (document.documentElement.hasAttribute('data-js')) {
    var vu = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        // Un bloc déjà dépassé vers le haut est révélé sans attendre : il ne
        // doit pas rester caché si l'on arrive au milieu de la page.
        if (!e.isIntersecting && e.boundingClientRect.top > 0) return;
        e.target.setAttribute('data-vu', '1');
        vu.unobserve(e.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
    Array.prototype.forEach.call(document.querySelectorAll('[data-reveal]'), function (el) { vu.observe(el); });
  }

  if ('IntersectionObserver' in window) {
    var toc = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
    if (toc.length) {
      var seen = {};
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { seen[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
        var best = null, top = 0;
        Object.keys(seen).forEach(function (id) { if (seen[id] > top) { top = seen[id]; best = id; } });
        if (best) toc.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + best); });
      }, { rootMargin: '-15% 0px -55% 0px', threshold: [0, .25, .5, 1] });
      toc.forEach(function (a) {
        var sct = document.querySelector(a.getAttribute('href'));
        if (sct) spy.observe(sct);
      });
    }
  }

  /* ------------------------------------------------------------- année ---*/
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
