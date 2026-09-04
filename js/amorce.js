/* ============================================================================
   L'AMORCE

   Ce fichier est le seul chargé sans `defer`, dans l'en-tête du document : il
   doit poser `data-js` sur la page AVANT le premier affichage. Sinon les blocs
   à révéler apparaîtraient une première fois en clair, puis sauteraient à leur
   position de départ — un clignotement à chaque chargement.

   Sans JavaScript, sans IntersectionObserver, ou si le système demande un
   mouvement réduit, `data-js` n'est jamais posé : tout s'affiche normalement.
   Le site n'a jamais besoin de ce fichier pour être lisible.
   ============================================================================ */
(function () {
  'use strict';
  try {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;
  } catch (e) { return; }
  document.documentElement.setAttribute('data-js', 'on');
})();
