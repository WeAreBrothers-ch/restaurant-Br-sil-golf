/* =============================================================================
   Le 9 — interactions du site. Aucune dépendance.
   Tout est facultatif : sans JavaScript, la page reste lisible et navigable.
   ============================================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

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

  /* ------------------------------------------------ visionneuse (galerie) ---*/
  var viewer = document.getElementById('viewer');
  if (viewer) {
    var vImg = viewer.querySelector('[data-img]');
    var vCap = viewer.querySelector('[data-caption]');
    var list = [];
    var idx = 0;
    var opener = null;

    var show = function (i) {
      if (!list.length) return;
      idx = (i + list.length) % list.length;
      var fig = list[idx];
      var img = fig.querySelector('img');
      vImg.src = img.currentSrc || img.src;
      vImg.alt = img.alt || '';
      var cap = fig.getAttribute('data-caption') || '';
      vCap.textContent = cap;
      vCap.hidden = !cap;
    };
    var open = function (fig) {
      list = Array.prototype.filter.call(
        document.querySelectorAll('.mosaic .ph'),
        function (f) { return f.classList.contains('ready'); });
      var i = list.indexOf(fig);
      if (i < 0) return;
      opener = document.activeElement;
      viewer.hidden = false;
      viewer.classList.add('show');
      document.body.style.overflow = 'hidden';
      show(i);
      viewer.querySelector('[data-close]').focus();
    };
    var close = function () {
      viewer.classList.remove('show');
      viewer.hidden = true;
      vImg.removeAttribute('src');
      document.body.style.overflow = '';
      if (opener && opener.focus) opener.focus();
    };

    document.addEventListener('click', function (e) {
      var fig = e.target.closest('.mosaic .ph.ready');
      if (fig) { e.preventDefault(); open(fig); return; }
      if (e.target.closest('[data-close]') || e.target === viewer) { close(); return; }
      if (e.target.closest('[data-prev]')) { show(idx - 1); return; }
      if (e.target.closest('[data-next]')) { show(idx + 1); }
    });
    document.addEventListener('keydown', function (e) {
      if (viewer.hidden) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(idx - 1);
      else if (e.key === 'ArrowRight') show(idx + 1);
    });
    // Balayage horizontal sur écran tactile
    var x0 = null;
    viewer.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    viewer.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) show(idx + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });
  }

  /* -------------------------------------- apparition douce et sommaire ---*/
  if ('IntersectionObserver' in window) {
    var rv = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); rv.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px' });
    Array.prototype.forEach.call(document.querySelectorAll('.rv'), function (el) { rv.observe(el); });

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
        var s = document.querySelector(a.getAttribute('href'));
        if (s) spy.observe(s);
      });
    }
  } else {
    Array.prototype.forEach.call(document.querySelectorAll('.rv'), function (el) { el.classList.add('in'); });
  }

  /* ------------------------------------------------------------- année ---*/
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
