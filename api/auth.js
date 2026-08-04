// Proxy OAuth Decap — étape 1 : redirige vers GitHub pour autorisation.
// Le client_secret n'est PAS utilisé ici (uniquement dans /api/callback).
// Variable d'env requise : OAUTH_GITHUB_CLIENT_ID
import crypto from 'node:crypto';

export default function handler(req, res) {
  const clientId = process.env.OAUTH_GITHUB_CLIENT_ID;
  if (!clientId) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end("Configuration OAuth manquante : definir OAUTH_GITHUB_CLIENT_ID dans les variables d'environnement Vercel.");
    return;
  }

  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const redirectUri = `${proto}://${host}/api/callback`;

  // state anti-CSRF : CSPRNG + lié à la session via cookie HttpOnly (vérifié dans /api/callback)
  const state = crypto.randomBytes(32).toString('base64url');
  res.setHeader(
    'Set-Cookie',
    `oauth_state=${state}; HttpOnly; Secure; SameSite=Lax; Path=/api; Max-Age=600`,
  );

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    // 'repo' : nécessaire pour lire/écrire un dépôt privé
    scope: 'repo',
    state,
    allow_signup: 'false',
  });

  res.statusCode = 302;
  res.setHeader('Location', `https://github.com/login/oauth/authorize?${params.toString()}`);
  res.end();
}
