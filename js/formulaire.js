/* ============================================================================
   LE FORMULAIRE DE CONTACT

   Il fonctionne sans ce fichier : `action` et `method` sont posés sur la
   balise, donc un envoi ordinaire part quand même. Le visiteur atterrit
   simplement sur la page du service de réception au lieu de rester ici.

   Ce fichier ne fait que retenir l'envoi pour afficher la réponse sur place et
   vérifier trois choses avant de partir. En cas d'échec, il redonne le numéro
   de téléphone : c'est la seule voie qui ne peut pas tomber en panne.
   ============================================================================ */
(function () {
  'use strict';

  var form = document.querySelector('.form');
  if (!form || !form.getAttribute('action')) return;

  var bouton = form.querySelector('.form__envoi');
  var zone = form.querySelector('.form__reponse');
  var TEL = form.getAttribute('data-telephone') || '';
  var LIEN_TEL = '<a href="tel:+41218822419">' + TEL + '</a>';

  function champ(nom) { return form.elements.namedItem(nom); }

  function effacer() {
    Array.prototype.forEach.call(form.querySelectorAll('.form__champ'), function (b) {
      b.removeAttribute('data-erreur');
    });
    Array.prototype.forEach.call(form.querySelectorAll('.form__erreur'), function (m) { m.remove(); });
    Array.prototype.forEach.call(form.querySelectorAll('[aria-invalid]'), function (e) {
      e.removeAttribute('aria-invalid');
    });
  }

  function signaler(nom, texte) {
    var el = champ(nom);
    if (!el) return;
    var bloc = el.closest('.form__champ');
    if (bloc) bloc.setAttribute('data-erreur', 'true');
    el.setAttribute('aria-invalid', 'true');
    var m = document.createElement('span');
    m.className = 'form__erreur';
    m.textContent = texte;
    if (bloc) bloc.appendChild(m);
    // Le curseur se place dans le champ à corriger : sans cela, la personne
    // doit retrouver elle-même où le problème se situe.
    el.focus();
  }

  function repondre(texte, etat) {
    zone.innerHTML = texte;
    zone.setAttribute('data-etat', etat);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    effacer();
    zone.removeAttribute('data-etat');
    zone.innerHTML = '';

    // Le piège : rempli, c'est un robot. On fait comme si tout allait bien.
    if (champ('site') && champ('site').value) {
      repondre('Merci, votre message est parti.', 'ok');
      return;
    }

    var nom = (champ('nom').value || '').trim();
    var email = (champ('email').value || '').trim();
    var message = (champ('message').value || '').trim();

    if (nom.length < 2) return signaler('nom', 'Votre nom, même en abrégé.');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return signaler('email', 'Cette adresse ne semble pas valide.');
    if (message.length < 10) return signaler('message', 'Quelques mots de plus, que nous puissions répondre.');

    bouton.disabled = true;
    var texteInitial = bouton.textContent;
    bouton.textContent = 'Envoi…';

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      form.reset();
      repondre('Merci, votre message est parti. Nous répondons sous un ou deux jours.', 'ok');
    }).catch(function () {
      repondre('L’envoi n’a pas abouti. Appelez-nous au ' + LIEN_TEL + ', c’est immédiat.', 'ko');
    }).finally(function () {
      bouton.disabled = false;
      bouton.textContent = texteInitial;
    });
  });
})();
