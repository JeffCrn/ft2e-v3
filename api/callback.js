// Proxy OAuth Decap — étape 2 : vérifie le state anti-CSRF, échange le code
// GitHub contre un token, puis transmet le token à la fenêtre Decap (postMessage).
// Variables d'env requises : OAUTH_GITHUB_CLIENT_ID, OAUTH_GITHUB_CLIENT_SECRET
import crypto from 'node:crypto';

// Origine de confiance de l'interface /admin. Le token n'est transmis QU'À cette
// origine, et on ignore les messages provenant de toute autre fenêtre (anti-vol de token).
const ALLOWED_ORIGIN = 'https://ft2e-site.vercel.app';

function getCookie(req, name) {
  const header = req.headers.cookie || '';
  const entry = header
    .split(';')
    .map((s) => s.trim())
    .find((s) => s.startsWith(`${name}=`));
  return entry ? decodeURIComponent(entry.slice(name.length + 1)) : null;
}

function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  const ab = Buffer.from(a);
  const bb = Buffer.from(b);
  return ab.length === bb.length && crypto.timingSafeEqual(ab, bb);
}

// Embarque un OBJET comme littéral de chaîne JS parsable, sûr dans un <script> inline.
function jsLiteral(value) {
  return JSON.stringify(JSON.stringify(value))
    .split('<').join('\\u003c')
    .split('>').join('\\u003e')
    .split(String.fromCharCode(0x2028)).join('\\u2028')
    .split(String.fromCharCode(0x2029)).join('\\u2029');
}

function htmlEscape(s) {
  return String(s)
    .split('&').join('&amp;')
    .split('<').join('&lt;')
    .split('>').join('&gt;')
    .split('"').join('&quot;');
}

export default async function handler(req, res) {
  const clientId = process.env.OAUTH_GITHUB_CLIENT_ID;
  const clientSecret = process.env.OAUTH_GITHUB_CLIENT_SECRET;

  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const url = new URL(req.url, `${proto}://${host}`);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const cookieState = getCookie(req, 'oauth_state');

  // Le state est à usage unique : on l'efface dès maintenant.
  const clearStateCookie = 'oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/api; Max-Age=0';

  // Renvoie la page de handshake. L'origine cible (où va le token) est figée à ALLOWED_ORIGIN.
  // Le message d'amorce 'authorizing:github' part en '*' (aucun secret) : motif canonique Decap.
  const sendPage = (status, contentObj) => {
    const visible =
      status === 'success'
        ? 'Authentification réussie. Cette fenêtre va se fermer…'
        : `Erreur : ${htmlEscape(contentObj.error || 'inconnue')}`;
    res.statusCode = 200;
    res.setHeader('Set-Cookie', clearStateCookie);
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(`<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Authentification GitHub</title></head>
<body><p style="font-family:system-ui;padding:2rem">${visible}</p>
<script>
(function () {
  var origin = ${JSON.stringify(ALLOWED_ORIGIN)};
  var message = 'authorization:github:${status}:' + ${jsLiteral(contentObj)};
  function receive(e) {
    if (e.origin !== origin) return;
    if (!window.opener) return;
    window.opener.postMessage(message, origin);
    window.removeEventListener('message', receive, false);
  }
  window.addEventListener('message', receive, false);
  if (window.opener) window.opener.postMessage('authorizing:github', '*');
})();
</script></body></html>`);
  };

  if (!clientId || !clientSecret) {
    sendPage('error', {
      error: `Configuration serveur incomplète — client_id présent: ${!!clientId}, client_secret présent: ${!!clientSecret}`,
    });
    return;
  }
  // Vérification anti-CSRF AVANT tout appel au token endpoint.
  if (!state || !cookieState || !safeEqual(state, cookieState)) {
    sendPage('error', { error: 'Échec de la vérification anti-CSRF (state invalide ou expiré). Relancez la connexion.' });
    return;
  }
  if (!code) {
    sendPage('error', { error: "Code d'autorisation manquant dans la requête." });
    return;
  }

  try {
    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ client_id: clientId, client_secret: clientSecret, code }),
    });
    const tokenData = await tokenRes.json();

    if (tokenData.error || !tokenData.access_token) {
      sendPage('error', { error: tokenData.error_description || tokenData.error || "Échec de l'échange du token." });
      return;
    }

    sendPage('success', { token: tokenData.access_token, provider: 'github' });
  } catch (e) {
    sendPage('error', { error: String((e && e.message) || e) });
  }
}
