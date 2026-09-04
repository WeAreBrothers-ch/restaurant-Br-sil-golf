/* ============================================================================
   LA BARRE D'APPEL

   Elle monte une fois le premier écran passé, et s'efface pendant la saisie
   d'un champ pour ne pas se poser sur le clavier. Tant qu'elle est cachée,
   ses liens sortent de l'ordre de tabulation.
   ============================================================================ */
(function () {
  'use strict';

  var barre = document.querySelector('.barre');
  if (!barre) return;

  var liens = Array.prototype.slice.call(barre.querySelectorAll('a'));
  var etat = null;

  function appliquer() {
    // Le seuil est la hauteur du premier écran s'il y en a un, sinon une valeur
    // courte : sur les pages intérieures la barre doit venir tout de suite.
    var hero = document.querySelector('.home-hero');
    var seuil = hero ? hero.offsetHeight * .7 : 220;
    var visible = window.scrollY > seuil;
    if (visible === etat) return;
    etat = visible;
    barre.setAttribute('data-visible', visible ? 'true' : 'false');
    liens.forEach(function (a) {
      if (visible) a.removeAttribute('tabindex');
      else a.setAttribute('tabindex', '-1');
    });
  }

  var attente = false;
  window.addEventListener('scroll', function () {
    if (attente) return;
    attente = true;
    requestAnimationFrame(function () { attente = false; appliquer(); });
  }, { passive: true });
  window.addEventListener('resize', function () { etat = null; appliquer(); });
  appliquer();

  // Pendant la saisie, on laisse la place au clavier.
  document.addEventListener('focusin', function (e) {
    if (e.target.matches('input, textarea, select')) barre.setAttribute('data-saisie', 'true');
  });
  document.addEventListener('focusout', function (e) {
    if (e.target.matches('input, textarea, select')) barre.removeAttribute('data-saisie');
  });
})();
