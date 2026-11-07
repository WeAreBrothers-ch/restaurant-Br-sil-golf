<?php
declare(strict_types=1);

/* ============================================================================
   ENVOYER-MESSAGE.PHP — le formulaire de contact, branché sur l'hébergement

   Le formulaire de `contact.html` poste ici. Ce script vérifie le message et le
   transmet par courriel à l'adresse du restaurant, en SMTP authentifié sur une
   boîte mail du domaine (Infomaniak : mail.infomaniak.com). Il ne dépend
   d'aucun service tiers et n'a rien à installer.

   POURQUOI LE SMTP ET PAS mail()
   Infomaniak déconseille la fonction mail() de PHP : envoi non authentifié,
   quota réduit, mauvaise délivrabilité (les messages finissent en indésirables).
   Un envoi authentifié, lui, arrive dans la boîte de réception.

   OÙ SONT LES IDENTIFIANTS
   Pas ici, et jamais dans git : dans `contact-config.php`, à côté de ce fichier,
   créé à la main sur le serveur à partir de `contact-config.example.php`.
   Sans lui, ce script répond « indisponible » et le visiteur voit le numéro de
   téléphone du restaurant — rien d'autre ne se passe.

   CE QUI PROTÈGE LA BOÎTE DES ABUS
     · le champ-piège « site » (un robot le remplit, une personne ne le voit pas) ;
     · l'origine de la requête, qui doit être ce site ;
     · une limite par visiteur (5 messages par heure) et une limite globale
       (100 par jour), pour que la boîte n'atteigne jamais son quota d'envoi ;
     · les retours à la ligne retirés de tout ce qui finit dans un en-tête
       (c'est ce qui empêche d'ajouter un destinataire en cachette) ;
     · des longueurs plafonnées, un courriel validé, un message minimal.

   COMPATIBILITÉ : écrit pour fonctionner dès PHP 7.0 (aucune syntaxe récente), parce
   que la version choisie sur l'hébergement n'est pas toujours la dernière.

   La partie à adapter d'un site à l'autre est le tableau SITE ci-dessous.
   ============================================================================ */

const SITE = [
    'nom'          => 'Le 9 · Restaurant du Golf du Brésil',
    'prefixe'      => 'Site Le 9',
    'destinataire' => 'restaurantle9@golfbresil.ch',
    'hotes'        => ['www.votre-domaine.ch', 'votre-domaine.ch'],
    'telephone'    => '021 882 24 19',
    'retour'       => '/contact.html',
    'couleurs'     => [
        'fond'   => '#f7f1e1',
        'texte'  => '#12241b',
        'accent' => '#14563a',
    ],
];

@ini_set('display_errors', '0');
date_default_timezone_set('Europe/Zurich');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

/* ----------------------------------------------------------------- réponse -- */

/** Le visiteur est-il arrivé par JavaScript (fetch) ou par un envoi ordinaire ? */
function veut_json(): bool
{
    return strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
}

function repondre(int $statut, bool $ok, string $message, array $champs = [])
{
    http_response_code($statut);
    if (veut_json()) {
        header('Content-Type: application/json; charset=UTF-8');
        $corps = ['success' => $ok, 'message' => $message];
        if ($champs) {
            $corps['champs'] = $champs;
        }
        echo json_encode($corps, JSON_UNESCAPED_UNICODE);
        exit;
    }
    // Sans JavaScript : une petite page, aux couleurs du site, avec la sortie de secours.
    header('Content-Type: text/html; charset=UTF-8');
    $h = function (string $s): string {
        return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    };
    $c = SITE['couleurs'];
    $tel = $h(SITE['telephone']);
    $telLien = $h(preg_replace('/[^0-9+]/', '', SITE['telephone']) ?? '');
    echo '<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<meta name="robots" content="noindex"><title>' . $h(SITE['nom']) . '</title>'
        . '<style>body{margin:0;min-height:100vh;display:grid;place-items:center;padding:1.5rem;'
        . 'background:' . $c['fond'] . ';color:' . $c['texte'] . ';font:1.125rem/1.6 Georgia,serif}'
        . 'main{max-width:34rem}h1{font-size:1.6rem;font-weight:400;margin:0 0 1rem}'
        . 'a{color:inherit;text-decoration-color:' . $c['accent'] . ';text-underline-offset:.2em}</style></head>'
        . '<body><main><h1>' . $h(SITE['nom']) . '</h1><p>' . $h($message) . '</p>';
    if (!$ok) {
        echo '<p>Le plus sûr : nous appeler au <a href="tel:' . $telLien . '">' . $tel . '</a>.</p>';
    }
    echo '<p><a href="' . $h(SITE['retour']) . '">Retour au site</a></p></main></body></html>';
    exit;
}

function journal(string $texte)
{
    error_log('[contact ' . SITE['nom'] . '] ' . $texte);
}

/* ----------------------------------------------------- petits utilitaires -- */

/** Retire ce qui ne doit pas se trouver dans un champ : contrôles, retours à la ligne (sauf $multiligne). */
function nettoyer(string $s, bool $multiligne = false): string
{
    $s = str_replace(["\r\n", "\r"], "\n", $s);
    $s = preg_replace($multiligne ? '/[^\P{Cc}\n]+|[\p{Zl}\p{Zp}]+/u' : '/[\p{Cc}\p{Zl}\p{Zp}]+/u', '', $s);
    return trim($s ?? '');        // null si le texte n'est pas de l'UTF-8 valide
}

function caracteres(string $s): array
{
    return preg_split('//u', $s, -1, PREG_SPLIT_NO_EMPTY) ?: [];
}

function longueur(string $s): int
{
    return count(caracteres($s));
}

function couper(string $s, int $max): string
{
    return longueur($s) > $max ? implode('', array_slice(caracteres($s), 0, $max)) : $s;
}

/** Un nom d'affichage d'adresse : entre guillemets s'il est ASCII, encodé sinon. */
function nom_affiche(string $s): string
{
    return preg_match('/^[\x20-\x7e]*$/', $s) ? '"' . str_replace(['"', '\\'], '', $s) . '"' : entete($s);
}

/** Encode un texte pour un en-tête de courriel (RFC 2047), par mots de 45 octets au plus. */
function entete(string $s): string
{
    if (preg_match('/^[\x20-\x7e]*$/', $s)) {
        return $s;
    }
    $mots = [];
    $mot = '';
    foreach (caracteres($s) as $c) {
        if (strlen($mot . $c) > 45) {
            $mots[] = $mot;
            $mot = '';
        }
        $mot .= $c;
    }
    $mots[] = $mot;
    return implode("\r\n ", array_map(function (string $m): string {
        return '=?UTF-8?B?' . base64_encode($m) . '?=';
    }, $mots));
}

function hote_de(string $url): string
{
    return strtolower((string) (parse_url($url, PHP_URL_HOST) ?? ''));
}

/* ------------------------------------------------------------ garde-fous -- */

/** Vrai si le visiteur peut encore écrire. Compte les envois dans le dossier temporaire du serveur. */
function limiter(string $ip): bool
{
    $dossier = sys_get_temp_dir() . '/contact-' . substr(hash('sha256', __DIR__), 0, 12);
    if (!is_dir($dossier) && !@mkdir($dossier, 0700, true) && !is_dir($dossier)) {
        return true;              // pas de dossier : on ne bloque pas le visiteur pour autant
    }
    $maintenant = time();

    $compter = static function (string $fichier, int $fenetre, int $plafond) use ($maintenant): bool {
        $f = @fopen($fichier, 'c+');
        if ($f === false) {
            return true;
        }
        flock($f, LOCK_EX);
        $dates = json_decode((string) stream_get_contents($f), true);
        $dates = array_values(array_filter(is_array($dates) ? $dates : [], function ($t) use ($maintenant, $fenetre): bool {
            return is_int($t) && $t > $maintenant - $fenetre;
        }));
        $autorise = count($dates) < $plafond;
        if ($autorise) {
            $dates[] = $maintenant;
            ftruncate($f, 0);
            rewind($f);
            fwrite($f, json_encode($dates));
        }
        flock($f, LOCK_UN);
        fclose($f);
        return $autorise;
    };

    return $compter($dossier . '/ip-' . substr(hash('sha256', $ip), 0, 16) . '.json', 3600, 5)
        && $compter($dossier . '/jour.json', 86400, 100);
}

/* ------------------------------------------------------------------- SMTP -- */

function smtp_lire($flux): array
{
    $texte = '';
    while (($ligne = fgets($flux, 1024)) !== false) {
        $texte .= $ligne;
        if (strlen($ligne) < 4 || $ligne[3] === ' ') {
            break;
        }
    }
    if ($texte === '') {
        throw new RuntimeException('le serveur SMTP ne répond pas');
    }
    return [(int) substr($texte, 0, 3), trim($texte)];
}

/** Envoie une commande ; $nom est ce qu'on écrit dans le journal (jamais l'identifiant ni le mot de passe). */
function smtp_commande($flux, string $commande, array $attendus, string $nom): string
{
    fwrite($flux, $commande . "\r\n");
    list($code, $texte) = smtp_lire($flux);
    if (!in_array($code, $attendus, true)) {
        throw new RuntimeException('SMTP ' . $nom . ' refusé : ' . $texte);
    }
    return $texte;
}

function smtp_envoyer(array $cfg, string $expediteur, string $destinataire, string $message)
{
    $implicite = $cfg['chiffrement'] === 'ssl';
    $contexte = stream_context_create(['ssl' => [
        'verify_peer' => $cfg['verifier_certificat'],
        'verify_peer_name' => $cfg['verifier_certificat'],
        'peer_name' => $cfg['hote'],
    ]]);
    $flux = @stream_socket_client(
        ($implicite ? 'ssl://' : 'tcp://') . $cfg['hote'] . ':' . $cfg['port'],
        $errno,
        $erreur,
        10,
        STREAM_CLIENT_CONNECT,
        $contexte
    );
    if ($flux === false) {
        throw new RuntimeException('connexion SMTP impossible (' . $errno . ' ' . $erreur . ')');
    }
    stream_set_timeout($flux, 15);

    try {
        list($code, $texte) = smtp_lire($flux);
        if ($code !== 220) {
            throw new RuntimeException('accueil SMTP inattendu : ' . $texte);
        }
        $moi = preg_replace('/[^a-z0-9.-]/i', '', $_SERVER['SERVER_NAME'] ?? '') ?: 'localhost';
        smtp_commande($flux, 'EHLO ' . $moi, [250], 'EHLO');

        if ($cfg['chiffrement'] === 'starttls') {
            smtp_commande($flux, 'STARTTLS', [220], 'STARTTLS');
            $methode = STREAM_CRYPTO_METHOD_TLS_CLIENT;
            foreach (['STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT', 'STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT'] as $nom) {
                if (defined($nom)) {
                    $methode |= constant($nom);
                }
            }
            if (!stream_socket_enable_crypto($flux, true, $methode)) {
                throw new RuntimeException('le chiffrement TLS n\'a pas pu être établi');
            }
            smtp_commande($flux, 'EHLO ' . $moi, [250], 'EHLO');
        }

        if ($cfg['utilisateur'] !== '') {
            smtp_commande($flux, 'AUTH LOGIN', [334], 'AUTH');
            smtp_commande($flux, base64_encode($cfg['utilisateur']), [334], 'identifiant');
            smtp_commande($flux, base64_encode($cfg['mot_de_passe']), [235], 'mot de passe');
        }

        smtp_commande($flux, 'MAIL FROM:<' . $expediteur . '>', [250], 'MAIL FROM');
        smtp_commande($flux, 'RCPT TO:<' . $destinataire . '>', [250, 251], 'RCPT TO');
        smtp_commande($flux, 'DATA', [354], 'DATA');
        // Un point seul sur une ligne terminerait le message : on le double.
        $corps = preg_replace('/^\./m', '..', $message);
        smtp_commande($flux, $corps . "\r\n.", [250], 'envoi du message');
        try {
            smtp_commande($flux, 'QUIT', [221], 'QUIT');
        } catch (Throwable $e) {
            // Le message est déjà accepté : une fermeture de session brusque n'y change rien.
        }
    } finally {
        fclose($flux);
    }
}

/* ------------------------------------------------------------ la requête -- */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    repondre(405, false, 'Cette adresse reçoit les messages du formulaire de contact.');
}
if (in_array('votre-domaine.ch', SITE['hotes'], true)) {
    journal('SITE[hotes] porte encore « votre-domaine.ch » : renseigner le domaine du site dans envoyer-message.php');
    repondre(503, false, 'L\'envoi est momentanément indisponible.');
}
if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 20000) {
    repondre(413, false, 'Message trop long.');
}

// Le formulaire ne vient jamais d'un autre site : Origin (ou, à défaut, Referer) doit être le nôtre.
$origine = hote_de($_SERVER['HTTP_ORIGIN'] ?? '') ?: hote_de($_SERVER['HTTP_REFERER'] ?? '');
if ($origine !== '' && !in_array($origine, SITE['hotes'], true)) {
    journal('origine refusée : ' . $origine);
    repondre(403, false, 'Envoi refusé.');
}

// Un robot a rempli le champ-piège : on répond « c'est parti » sans rien envoyer.
if (nettoyer((string) ($_POST['site'] ?? '')) !== '') {
    repondre(200, true, 'Merci, votre message est parti.');
}

$nom = couper(nettoyer((string) ($_POST['nom'] ?? '')), 80);
$email = couper(nettoyer((string) ($_POST['email'] ?? '')), 120);
$sujet = couper(nettoyer((string) ($_POST['sujet'] ?? '')), 120);
$texte = couper(nettoyer((string) ($_POST['message'] ?? ''), true), 2000);

$manque = [];
if (longueur($nom) < 2) {
    $manque[] = 'nom';
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $manque[] = 'email';
}
if (longueur($texte) < 10) {
    $manque[] = 'message';
}
if ($manque) {
    repondre(422, false, 'Le message est incomplet.', $manque);
}

// La boîte d'envoi : sans elle, rien ne part (et le visiteur est renvoyé vers le téléphone).
$cfg = is_file(__DIR__ . '/contact-config.php') ? require __DIR__ . '/contact-config.php' : null;
$cfg = is_array($cfg) ? $cfg + ['port' => 587, 'chiffrement' => 'starttls', 'verifier_certificat' => true, 'expediteur' => ''] : null;
if (
    $cfg === null
    || !is_string($cfg['hote'] ?? null) || $cfg['hote'] === ''
    || !is_string($cfg['utilisateur'] ?? null) || !is_string($cfg['mot_de_passe'] ?? null)
    || !in_array($cfg['chiffrement'], ['starttls', 'ssl', 'aucun'], true)
) {
    journal('contact-config.php absent ou incomplet : aucun message ne peut partir');
    repondre(503, false, 'L\'envoi est momentanément indisponible.');
}
$expediteur = $cfg['expediteur'] !== '' ? $cfg['expediteur'] : $cfg['utilisateur'];
if (!filter_var($expediteur, FILTER_VALIDATE_EMAIL)) {
    journal('adresse d\'expédition invalide dans contact-config.php');
    repondre(503, false, 'L\'envoi est momentanément indisponible.');
}

if (!limiter($_SERVER['REMOTE_ADDR'] ?? 'inconnue')) {
    journal('limite atteinte pour ' . ($_SERVER['REMOTE_ADDR'] ?? 'inconnue'));
    repondre(429, false, 'Vous avez envoyé plusieurs messages : merci de patienter un peu, ou de nous appeler.');
}

/* ---------------------------------------------------------- le courriel -- */

$objet = SITE['prefixe'] . ' · ' . ($sujet !== '' ? $sujet : 'Nouveau message');
$nomSur = str_replace(['"', '\\', '<', '>'], '', $nom);
$corps = "Message envoyé depuis le site — " . SITE['nom'] . "\n\n"
    . 'De     : ' . $nom . ' <' . $email . ">\n"
    . 'Sujet  : ' . ($sujet !== '' ? $sujet : '(aucun)') . "\n"
    . 'Reçu le : ' . date('d.m.Y à H:i') . "\n\n"
    . "----------------------------------------\n\n"
    . $texte . "\n\n"
    . "----------------------------------------\n"
    . "Pour répondre, utilisez « Répondre » : l'adresse du visiteur est déjà dans le courriel.\n";

$domaine = substr(strrchr($expediteur, '@') ?: '@localhost', 1);
$entetes = [
    'Date: ' . date('r'),
    'From: ' . nom_affiche(SITE['nom']) . ' <' . $expediteur . '>',
    'Reply-To: ' . nom_affiche($nomSur) . ' <' . $email . '>',
    'To: <' . SITE['destinataire'] . '>',
    'Subject: ' . entete($objet),
    'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $domaine . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
];
$message = implode("\r\n", $entetes) . "\r\n\r\n" . chunk_split(base64_encode(str_replace("\n", "\r\n", $corps)), 76, "\r\n");

try {
    smtp_envoyer($cfg, $expediteur, SITE['destinataire'], rtrim($message, "\r\n"));
} catch (Throwable $e) {
    journal($e->getMessage());
    repondre(502, false, 'Le message n\'a pas pu être envoyé.');
}

repondre(200, true, 'Merci, votre message est parti. Nous vous répondons au plus vite.');
