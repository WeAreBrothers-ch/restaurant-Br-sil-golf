/* ============================================================================
   LE MOUVEMENT DU PREMIER ÉCRAN

   Les dessins tombent et vrillent pendant qu'on quitte le premier écran ;
   l'enseigne remonte et s'efface. Le mouvement suit le doigt, pixel pour pixel.

   Deux moteurs, un seul mouvement :
   1. là où le navigateur sait lier une animation au défilement (Safari 26,
      Chrome, Edge), il la joue lui-même, sur le compositeur — c'est ce qui la
      rend parfaitement fluide, sur iPhone en particulier ;
   2. ailleurs, le script écrit l'avancée `--p` à chaque image, et la feuille
      de style en tire le même mouvement.

   Les deux donnent les mêmes positions au pixel près : départ à `--p: 0`,
   arrivée à `--p: 1`, en ligne droite entre les deux.

   Si le système demande un mouvement réduit, ce fichier ne fait rien du tout :
   les dessins restent où ils sont posés.
   ============================================================================ */
(function () {
  "use strict";

  var REGLAGES = {
    ecran: ".home-hero",
    titre: ".mono",
    champ: ".home-champ",
    piece: ".piece",
    titreMontee: 2.5, // en rem
    titreEchelle: 0.95,
    titreOpacite: 0.1,
    champOpacite: 0.28,
    // Le geste d'un dessin, dans l'ordre exact de la feuille de style.
    geste: function (chute, angle) {
      return "translateY(" + chute + "px) rotate(" + angle + "deg) translate(-50%, -50%)";
    },
  };

  var premier = document.querySelector(REGLAGES.ecran);
  if (!premier) return;

  try {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  } catch (e) {
    return;
  }

  var titre = premier.querySelector(REGLAGES.titre);
  var champ = premier.querySelector(REGLAGES.champ);
  var pieces = Array.prototype.slice.call(premier.querySelectorAll(REGLAGES.piece));

  // La course est la hauteur du premier écran : le mouvement est terminé quand
  // il est entièrement passé.
  var course = 1;
  var mesurer = function () {
    course = Math.max(1, premier.offsetHeight);
  };

  /* ==========================================================================
     1. LE NAVIGATEUR JOUE LE MOUVEMENT LUI-MÊME

     Chaque élément reçoit une animation aux valeurs fixes — lues une fois
     dans la feuille de style : chute, vrille, pente —, attachée au défilement
     de la page. Le navigateur la joue sur le compositeur, dans la même image
     que le défilement : le dessin ne peut plus avoir de retard sur le doigt,
     même quand la page est occupée ailleurs. Sur iPhone, c'est Safari 26.4
     et au-delà.

     L'animation couvre tout le défilement de la page ; le mouvement en occupe
     le début — la hauteur du premier écran — et reste à son terme ensuite.
     Elle est reconstruite quand la page change de taille, puisque les dessins
     changent alors de réglages.
     ========================================================================== */
  var source = document.scrollingElement || document.documentElement;
  var parNavigateur = false;
  try {
    parNavigateur = typeof window.ScrollTimeline === "function" && typeof premier.animate === "function";
  } catch (e) {
    parNavigateur = false;
  }

  var nombre = function (el, nom) {
    var v = parseFloat(getComputedStyle(el).getPropertyValue(nom));
    return isFinite(v) ? v : 0;
  };

  var animations = [];
  var empreinte = "";

  var construire = function () {
    mesurer();
    var etendue = source.scrollHeight - source.clientHeight;
    if (etendue <= 0) return;
    var fin = Math.min(1, course / etendue);
    var rem = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;

    var lot = [];
    if (titre) {
      lot.push([
        titre,
        { transform: "translateY(0px) scale(1)", opacity: 1 },
        {
          transform: "translateY(" + -REGLAGES.titreMontee * rem + "px) scale(" + REGLAGES.titreEchelle + ")",
          opacity: REGLAGES.titreOpacite,
        },
      ]);
    }
    if (champ) lot.push([champ, { opacity: 1 }, { opacity: REGLAGES.champOpacite }]);
    pieces.forEach(function (piece) {
      var chute = nombre(piece, "--chute");
      var vrille = nombre(piece, "--vrille");
      var pente = nombre(piece, "--r");
      lot.push([
        piece,
        { transform: REGLAGES.geste(0, pente) },
        { transform: REGLAGES.geste(chute, pente + vrille) },
      ]);
    });

    // Rien n'a changé depuis la dernière construction : on garde ce qui tourne.
    var cle = fin + "|" + JSON.stringify(lot.map(function (x) { return [x[1], x[2]]; }));
    if (cle === empreinte) return;

    var temps = new window.ScrollTimeline({ source: source, axis: "block" });
    var nouvelles = lot.map(function (x) {
      var images = [Object.assign({ offset: 0 }, x[1]), Object.assign({ offset: fin }, x[2])];
      if (fin < 1) images.push(Object.assign({ offset: 1 }, x[2]));
      return x[0].animate(images, { timeline: temps, fill: "both", easing: "linear" });
    });

    // Les anciennes ne s'arrêtent qu'une fois les nouvelles posées : jamais une
    // image où le dessin reviendrait à sa place de repos.
    animations.forEach(function (a) {
      a.cancel();
    });
    animations = nouvelles;
    empreinte = cle;
  };

  if (parNavigateur) {
    try {
      construire();
      var demande = false;
      var plusTard = function () {
        if (demande) return;
        demande = true;
        window.requestAnimationFrame(function () {
          demande = false;
          construire();
        });
      };
      window.addEventListener("resize", plusTard);
      window.addEventListener("load", plusTard);
      // La page s'allonge quand les photographies et les polices arrivent : la
      // part du défilement qui revient au premier écran change avec elle.
      if (typeof ResizeObserver === "function") new ResizeObserver(plusTard).observe(document.body);
      return;
    } catch (e) {
      animations.forEach(function (a) {
        a.cancel();
      });
      animations = [];
    }
  }

  /* ==========================================================================
     2. AILLEURS, LE SCRIPT ÉCRIT `--p`

     À chaque image de rendu où l'on a défilé, sans arrondi visible : un
     dix-millième de chute, c'est moins d'un dixième de pixel. La feuille de
     style en tire le même mouvement.
     ========================================================================== */
  var dernier = -1;
  var enAttente = false;

  var ecrire = function () {
    enAttente = false;
    var p = window.scrollY / course;
    if (p < 0) p = 0;
    if (p > 1) p = 1;
    var arrondi = Math.round(p * 10000) / 10000;
    if (arrondi === dernier) return;
    dernier = arrondi;
    premier.style.setProperty("--p", String(arrondi));
  };

  var auDefilement = function () {
    if (enAttente) return;
    enAttente = true;
    window.requestAnimationFrame(ecrire);
  };

  try {
    mesurer();
    ecrire();
    window.addEventListener("scroll", auDefilement, { passive: true });
    window.addEventListener("resize", function () {
      mesurer();
      dernier = -1;
      auDefilement();
    });
  } catch (e) {
    // En cas de pépin, on efface le chiffre : tout revient à sa position de
    // repos, et le premier écran reste parfaitement lisible.
    premier.style.removeProperty("--p");
  }
})();
