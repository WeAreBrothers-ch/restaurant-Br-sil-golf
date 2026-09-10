/* =============================================================================
   Le 9 — interactions du site. Aucune dépendance.
   Tout est facultatif : sans JavaScript, la page reste lisible et navigable.
   ============================================================================= */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- menu ---
     Le menu du téléphone est un vrai <dialog> : le navigateur se charge du
     piégeage du focus, de la touche Échap et du rôle de dialogue. On ne fait
     qu'ouvrir, fermer, et bloquer le défilement de la page derrière. */
  var menu = document.getElementById('menu');
  var burger = document.querySelector('.burger');
  if (menu && burger && typeof menu.showModal === 'function') {
    burger.addEventListener('click', function () {
      menu.showModal();
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    });
    menu.addEventListener('click', function (e) {
      // Un lien, la croix, ou le fond hors du panneau : on part, donc on ferme.
      if (e.target.closest('.mm__lien, .mm__fermer') || e.target === menu) menu.close();
    });
    menu.addEventListener('close', function () {
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  } else if (burger) {
    // Navigateur sans showModal : le bouton mène au pied de page, qui porte la
    // même navigation. Mieux qu'un bouton qui ne fait rien.
    burger.addEventListener('click', function () {
      var pied = document.querySelector('.foot');
      if (pied) pied.scrollIntoView({ behavior: 'smooth' });
    });
  }

  /* ------------------------------------------------- filet de l'en-tête ---
     ET SON TON. L'en-tête est crème ; sur les zones vertes il traçait une
     bande pâle en travers de la page. On mesure une fois pour toutes où
     commencent et finissent ces zones, puis on regarde, à chaque défilement,
     laquelle passe sous l'en-tête. Aucune lecture de mise en page pendant le
     défilement : c'est ce qui permet de le faire à chaque image de rendu. */
  var head = document.querySelector('.head');
  var zones = [];

  /* La page a deux fonds sombres : le vert de section, sur lequel se posent
     les panneaux du fil de la page, et le socle, réservé au pied. L'en-tête
     doit prendre l'un ou l'autre, sans quoi il retrace une bande d'un
     troisième vert par-dessus. Chaque zone dit donc lequel elle porte. */
  function mesurerZones() {
    zones = Array.prototype.map.call(
      document.querySelectorAll('.dark, .foot, .menu-page, .terr-hero'),
      function (el) {
        var r = el.getBoundingClientRect();
        // Le bandeau de la terrasse finit sur le socle : son dégradé y descend.
        var ton = el.classList.contains('foot') || el.classList.contains('terr-hero')
          ? 'socle' : 'section';
        return [r.top + window.scrollY, r.bottom + window.scrollY, ton];
      }
    );
  }

  var tonPose = null;
  function onScroll() {
    if (!head) return;
    head.classList.toggle('is-stuck', window.scrollY > 6);
    // Le point observé est juste SOUS le bas de l'en-tête : c'est ce qu'il
    // recouvre. Mesuré un pixel plus haut, il se voyait lui-même, et une page
    // sombre commençant exactement à sa hauteur n'était jamais reconnue.
    var y = window.scrollY + head.offsetHeight + 2;
    var ton = null;
    for (var i = 0; i < zones.length; i++) {
      if (y >= zones[i][0] && y < zones[i][1]) { ton = zones[i][2]; break; }
    }
    if (ton === tonPose) return;
    tonPose = ton;
    if (ton) head.setAttribute('data-ton', ton);
    else head.removeAttribute('data-ton');
  }

  var enAttente = false;
  window.addEventListener('scroll', function () {
    if (enAttente) return;
    enAttente = true;
    requestAnimationFrame(function () { enAttente = false; onScroll(); });
  }, { passive: true });
  window.addEventListener('resize', function () { mesurerZones(); tonPose = null; onScroll(); });
  // Les photographies changent la hauteur de la page en arrivant : on remesure.
  window.addEventListener('load', function () { mesurerZones(); tonPose = null; onScroll(); });
  mesurerZones();
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

  /* ------------------------------------------------------ apparitions ---*/
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

  /* ------------------------------------------------------------- année ---*/
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
