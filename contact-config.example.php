<?php
/* ============================================================================
   CONTACT-CONFIG.PHP — la boîte mail qui envoie les messages du formulaire

   1. Copiez ce fichier sous le nom `contact-config.php` (sans « .example »).
   2. Remplissez l'adresse de la boîte et son mot de passe. C'est la MÊME boîte que
      pour le site de L'Étoile : le plus simple est de copier son `contact-config.php`.
   3. Déposez-le sur le serveur, dans le même dossier que `envoyer-message.php`
      (la racine du site).

   ⚠ Ne l'ajoutez JAMAIS à git : il contient un mot de passe. Il est déjà
   listé dans `.gitignore`. Il n'est donc pas non plus déployé par le dépôt :
   c'est un fichier à poser une fois à la main sur l'hébergement.
   ============================================================================ */

return [
    'hote'         => 'mail.infomaniak.com',
    'port'         => 587,
    'chiffrement'  => 'starttls',          // 'starttls' avec le port 587, ou 'ssl' avec le port 465
    'utilisateur'  => 'contact@restaurant-letoile.ch',   // la MÊME boîte que L'Étoile (adresse complète)
    'mot_de_passe' => '',
    // 'expediteur' => '',                 // par défaut : l'adresse ci-dessus (à garder ainsi)
];
