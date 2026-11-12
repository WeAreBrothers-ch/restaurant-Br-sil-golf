/* ============================================================================
   LE MOUVEMENT DU PREMIER ÉCRAN

   La feuille de style tire la chute et la vrille des dessins d'un seul nombre,
   l'avancée du premier défilement, de 0 à 1. Ce fichier ne fait que lui donner
   cette avancée, de l'une de deux façons.

   1. Là où le navigateur sait lier une animation au défilement (Chrome, Edge,
      Safari 26) : il mesure la course — la hauteur du premier écran —, l'écrit
      dans --course, pose data-defilement="css", et s'arrête là. Pas un
      écouteur de défilement : le mouvement est joué par le compositeur, dans
      la même image que le défilement, même quand la page est occupée
      ailleurs. C'est ce qui le rend parfaitement fluide.

   2. Ailleurs : il écrit --p à chaque image de rendu où l'on a défilé. Sans
      arrondi : l'arrondi au centième faisait avancer les dessins par sauts de
      deux à trois pixels, et c'était cela, la saccade.

   Si le système demande un mouvement réduit, ce fichier ne fait rien : les
   dessins restent où ils sont posés.
   ============================================================================ */
(function () {
  'use strict';

  var hero = document.querySelector('.home-hero');
  if (!hero) return;

  var parCss = false;
  try {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    parCss = !!(window.CSS && CSS.supports('animation-timeline: scroll()'));
  } catch (e) { return; }

  var course = 1;
  var courseEcrite = 0;

  // La course est la hauteur du premier écran : le mouvement est fini quand on
  // l'a entièrement passé. Elle est remesurée à chaque changement de taille,
  // car sur téléphone la barre d'adresse qui se replie la fait varier.
  function mesurer() {
    course = Math.max(1, hero.offsetHeight);
    if (course === courseEcrite) return;
    courseEcrite = course;
    hero.style.setProperty('--course', course + 'px');
  }

  if (parCss) {
    try {
      mesurer();
      hero.setAttribute('data-defilement', 'css');
      window.addEventListener('resize', mesurer);
      return;
    } catch (e) { hero.removeAttribute('data-defilement'); }
  }

  var dernier = -1;
  var attente = false;

  function ecrire() {
    attente = false;
    var p = window.scrollY / course;
    if (p < 0) p = 0;
    if (p > 1) p = 1;
    // Quatre décimales : un dix-millième de chute, c'est moins d'un dixième de
    // pixel. Et si la valeur n'a pas changé, on ne touche pas au style.
    var v = Math.round(p * 10000) / 10000;
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
