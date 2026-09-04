/* ============================================================================
   LE MOUVEMENT DU PREMIER ÉCRAN

   Ce fichier ne déplace rien. Il écrit un seul nombre, --p, l'avancée du
   premier défilement de 0 à 1, et la feuille de style en tire la chute et la
   vrille de chacun des neuf dessins. Une écriture par image de rendu, pas neuf :
   c'est ce qui permet au navigateur de tout composer sur la carte graphique.

   Passé le premier écran, le nombre reste à 1 et plus rien n'est écrit : la
   page ne travaille pas pendant les milliers de pixels qui suivent.

   Si le système demande un mouvement réduit, ce fichier ne fait rien : les
   dessins restent où ils sont posés.
   ============================================================================ */
(function () {
  'use strict';

  var hero = document.querySelector('.home-hero');
  if (!hero) return;

  try {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  } catch (e) { return; }

  var course = 1;
  var dernier = -1;
  var attente = false;

  // La course est la hauteur du premier écran : le mouvement est fini quand on
  // l'a entièrement passé. Elle est remesurée à chaque changement de taille,
  // car sur téléphone la barre d'adresse qui se replie la fait varier.
  function mesurer() { course = Math.max(1, hero.offsetHeight); }

  function ecrire() {
    attente = false;
    var p = window.scrollY / course;
    if (p < 0) p = 0;
    if (p > 1) p = 1;
    // Deux décimales suffisent ; au-delà on réécrit une valeur que personne ne
    // voit. Et si elle n'a pas changé, on ne touche pas au style.
    var v = Math.round(p * 100) / 100;
    if (v === dernier) return;
    dernier = v;
    hero.style.setProperty('--p', String(v));
  }

  function auDefilement() {
    if (attente) return;
    attente = true;
    window.requestAnimationFrame(ecrire);
  }

  try {
    mesurer();
    ecrire();
    window.addEventListener('scroll', auDefilement, { passive: true });
    window.addEventListener('resize', function () { mesurer(); dernier = -1; auDefilement(); });
  } catch (e) {
    // En cas de pépin, on efface le nombre : tout revient au repos et le
    // premier écran reste parfaitement lisible.
    hero.style.removeProperty('--p');
  }
})();
