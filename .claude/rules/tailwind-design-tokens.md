# Tailwind & Design Tokens

**Scope** : tout fichier utilisant Tailwind (`.astro`, `.tsx`, `.html`).

## Principe directeur

**Aucune valeur de couleur, espacement, typographie ou rayon hard-codée** en dehors de `src/styles/global.css` (section `@theme`). Tout passe par les *tokens*. La source de verite est `src/styles/global.css`, **pas** un `tailwind.config.ts`.

## Tokens autorises — uniques sources de verite

### Couleurs

| Token | Hex | Usage exclusif |
|---|---|---|
| `marine-deep` | `#0f2436` | Hero, CTA final, nav solidifiee — fond le plus immersif |
| `marine` | `#16324f` | Sections sombres, **titres** (`h1`–`h6`) sur fond clair, nav |
| `marine-surface` | `#1d3a57` | Cartes sur fond sombre |
| `marine-surface-2` | `#223f5e` | Variation de surface sombre |
| `cool-white` | `#edf1f5` | Fonds de section alternatifs, cartes |
| `near-black` | `#1d1d1f` | **Body** (texte courant) sur fond clair — inchange |
| `slate` | `#45535f` | Texte secondaire, legendes, baseline sur fond clair |
| `mist` | `#9fb0bf` | Texte secondaire, baseline sur fond marine |
| `apple-blue` | `#0071e3` | CTA principal, accent d'action, focus ring |
| `link-blue` | `#0066cc` | Liens texte sur fond clair |
| `bright-blue` | `#2997ff` | Liens sur fond sombre — reserve a `marine-deep` (voir a11y) |
| `copper` | `#c46a38` | Accent d'identite sur fond clair (logo, eyebrow, filet) |
| `bright-copper` | `#d98a55` | Accent d'identite sur fond sombre (logo, eyebrow) |
| `pure-black` | `#000000` | **Legacy** — n'est plus utilise pour les surfaces |
| `button-active` | `#ededf2` | Etat actif boutons clairs |
| `button-light` | `#fafafc` | Boutons de filtre |
| `text-primary` | `#1d1d1f` | Texte principal |
| `text-secondary` | `rgba(0,0,0,0.8)` | Texte secondaire |
| `text-tertiary` | `rgba(0,0,0,0.48)` | Texte tertiaire, legendes |

**Trois registres, un accent d'action isole.** Le marine (`marine-deep` / `marine` / `marine-surface`) porte la **structure** : surfaces sombres et titres, a la place du noir/near-black d'origine. Le bleu (`apple-blue` / `bright-blue` / `link-blue`) signale l'**action** : CTA, liens, focus — inchange. Le cuivre (`copper` / `bright-copper`) porte l'**identite** de marque — logo, chiffre « 2 » du wordmark, eyebrow, filet — et ne doit jamais signaler un element cliquable, inchange. Le gris-bleu de baseline (`slate` / `mist`) porte le texte secondaire.

Regle titres/body : `text-near-black` **sur un titre** (`h1`–`h6`) devient `text-marine` ; le **body** (paragraphes, texte courant) conserve `text-near-black`.

Contrastes cles : `bright-copper` sur `marine-deep` = 5,8:1 (OK) ; `copper` sur blanc = 3,8:1 (gros glyphes de marque uniquement, jamais de texte courant ni de lien) ; `bright-blue` sur `marine-deep` = 5,25:1 (OK, liens) mais `bright-blue` sur `marine` moyen = 4,34:1 (texte large / UI uniquement, pas de lien texte en petits caracteres).

### Repointage (churn minimal)

`light-gray` → repointe vers `#edf1f5` (meme role : fond clair alterne). `dark-surface-1` / `dark-surface-2` → repointes vers `#1d3a57` / `#223f5e` (meme role : cartes sur fond sombre). Les classes `bg-light-gray`, `bg-dark-surface-1`, `bg-dark-surface-2` restent valides et rendent desormais les nouvelles valeurs automatiquement.

### Aliases legacy

Les anciens tokens sont conserves comme aliases pour eviter les regressions :

| Ancien token | Redirige vers |
|---|---|
| `bleu-nuit` | `#0f2436` (marine-deep) |
| `sarcelle` | `#0071e3` (apple-blue) |
| `cuivre` | `#0071e3` (apple-blue) |
| `creme-pierre` | `#edf1f5` (cool-white) |
| `anthracite` | `#1d1d1f` (near-black) |

**Preferer les nouveaux tokens.** Les aliases legacy sont destines a la transition ; les nouveaux composants doivent utiliser exclusivement la palette marine/cuivre/bleu.

### Typographie

- **Titres et texte courant** : `Inter Variable`, fallback `Helvetica Neue`, `Helvetica`, `Arial`, `system-ui`.
- **Mono** : `JetBrains Mono`, fallback `monospace` (pour bloc code uniquement).

Une seule police pour heading et body. Charger via `@fontsource-variable/inter`. **`font-display: swap`** systematique. Pas de Google Fonts CDN (RGPD).

#### Headlines

- `font-semibold` (600) pour tous les titres.
- `line-height: 1.07` pour les hero headlines, `1.10` pour les titres de section.
- `letter-spacing: -0.02em` sur tous les titres.

Echelle :

| Token | Taille / line-height |
|---|---|
| `text-h1` | clamp(2.25rem, 4vw, 3.5rem) / 1.07 |
| `text-h2` | clamp(1.75rem, 3vw, 2.5rem) / 1.10 |
| `text-h3` | 1.5rem / 1.15 |
| `text-body` | 1rem / 1.6 |
| `text-small` | 0.875rem / 1.5 |
| `text-caption` | 0.75rem / 1.4 (uppercase, tracking) |

### Espacements

Echelle Tailwind par defaut, mais **utiliser uniquement** les multiples : `1`, `2`, `3`, `4`, `6`, `8`, `12`, `16`, `24`, `32`. Pas de valeurs intermediaires (`5`, `7`, `9`...) sauf cas justifie.

### Conteneur

Largeur maximale : `max-w-[980px]` (au lieu de `max-w-screen-xl`). Centre avec `mx-auto px-6`.

### Rayons

- `rounded-lg` (8 px) : rayon standard pour cartes et conteneurs.
- `rounded-[980px]` : CTA pill (bouton arrondi Apple).
- `rounded-full` (50 %) : media controls, avatars.
- `rounded-none` : cas exceptionnel.

Pas de `rounded-sm`, `rounded`, `rounded-xl` sauf justification explicite.

### Ombres

Sobres et rares. Un seul `shadow-soft` autorise : `3px 5px 30px rgba(0,0,0,0.22)`.

### Bordures

**Pas de bordures sur les cartes.** L'esthetique Apple repose sur le contraste de surface (fond blanc / fond blanc froid / fond marine) et non sur des bordures visibles. Seule exception : les champs de formulaire et les separateurs semantiques (`<hr>`).

## Patterns autorises

```astro
<!-- ✅ Bon — lien Apple sur fond clair -->
<a class="text-link-blue hover:underline">En savoir plus ›</a>

<!-- ✅ Bon — lien Apple sur fond sombre (marine-deep uniquement) -->
<a class="text-bright-blue hover:underline">En savoir plus ›</a>

<!-- ✅ Bon — CTA pill -->
<a class="bg-apple-blue text-white rounded-[980px] px-4 py-2">Parlons-en</a>

<!-- ✅ Bon — section hero / CTA final, fond le plus immersif -->
<section class="bg-marine-deep text-white">…</section>

<!-- ✅ Bon — section sombre secondaire (ex. Secteurs) -->
<section class="bg-marine text-white">…</section>

<!-- ✅ Bon — titre sur fond clair -->
<h2 class="text-marine">Nos expertises</h2>

<!-- ✅ Bon — carte sur fond blanc froid, sans bordure -->
<div class="bg-cool-white rounded-lg shadow-soft p-6">…</div>

<!-- ❌ Mauvais — couleur arbitraire -->
<a class="text-[#0071e3]">…</a>

<!-- ❌ Mauvais — bordure sur carte -->
<div class="border border-gray-200 rounded">…</div>

<!-- ❌ Mauvais — typographie hors echelle -->
<h2 class="text-[28px]">…</h2>

<!-- ❌ Mauvais — ancien conteneur trop large -->
<div class="max-w-screen-xl">…</div>

<!-- ❌ Mauvais — noir pur pour une surface (legacy) -->
<section class="bg-pure-black">…</section>
```

## Mode sombre

**Non applicable.** Le site utilise deja des sections marine / blanc froid alternees pour creer le rythme visuel. Ne pas implementer `dark:`.
