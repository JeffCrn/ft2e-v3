# Voix éditoriale & typographie française

**Scope** : tout contenu textuel destiné à l'utilisateur final (pages, fiches projet, actualités, microcopie, alt-text, métadonnées).

## Voix FT2E — trois adjectifs

1. **Sobre.** Pas de superlatif, pas de jargon marketing, pas d'emphase. « Nous concevons » et non « Nous révolutionnons ».
2. **Technique.** La précision est la signature. Chiffres concrets, terminologie métier juste (RT2012, RE2020, CFO/CFA, SSI), pas d'à-peu-près.
3. **Chaleureuse.** Lisibilité humaine, phrases courtes ou moyennes, présence implicite d'une équipe.

## À éviter absolument

- ❌ « Solutions sur-mesure », « accompagnement personnalisé », « expertise reconnue », « équipe passionnée », « excellence ».
- ❌ Emojis dans le contenu institutionnel (autorisés sur LinkedIn, jamais sur le site).
- ❌ Anglicismes évitables : préférer « mémoire technique » à « pitch », « cahier des charges » à « brief », « bureau d'études » à « consulting ».
- ❌ Points d'exclamation hors citations directes.
- ❌ Première personne du pluriel emphatique (« Chez FT2E, **nous croyons** que… »). Préférer le présent factuel.

## Vocabulaire métier — graphies attendues

| À écrire | Pas |
|---|---|
| **BET** (bureau d'études techniques) | BE, b.e.t |
| **MOA** / **MOE** | maître d'ouvrage écrit en toutes lettres ou MOA selon contexte |
| **CVC** (chauffage, ventilation, climatisation) | hvac |
| **CFO / CFA** (courants forts / courants faibles) | … |
| **SSI** (sécurité incendie) | … |
| **BIM** | bim, B.I.M. |
| **RT2012**, **RE2020** | RT 2012, RE 2020 (sans espace) |
| **Effinergie+**, **NF Habitat HQE** | … |
| **kWh/m²/an** | … |
| **m²** (avec exposant) | m2 |
| **°C** (degré) | … |

## Typographie française stricte

- **Espace insécable** avant : `:`, `;`, `!`, `?`, `»`, et après `«`.
- Utiliser **`&nbsp;`** ou caractère insécable Unicode (`U+00A0`).
- **Guillemets français** `« »` (jamais `" "`).
- **Apostrophe typographique** `'` (jamais `'`).
- **Tiret cadratin** `—` pour incise (jamais `--`).
- **Points de suspension** `…` (jamais `...`).
- **Espace fine insécable** (`U+202F`) idéalement entre nombres et unités : `17 ans`, `1 240 m²`.

## Nombres et quantités

**Cette règle a été relevée, pas décrétée.** Elle décrit l'usage déjà en vigueur dans les dix-neuf récits de `src/content/projets/`, constaté au 2026-08-09 : les récits l'appliquaient avant qu'elle soit écrite. Elle est consignée ici pour que les chapôs et les textes à venir s'y conforment sans avoir à la redécouvrir.

| Cas | Graphie | Exemple |
|---|---|---|
| **Quantité sous dix** | en **lettres** | « deux bâtiments », « quatre chambres », « sept niveaux », « neuf semaines » |
| **Quantité à partir de dix** | en **chiffres** | « 46 chambres », « 102 lits », « 13 logements », « 11 zones » |
| **Unité, mesure, échelle** | toujours en **chiffres**, quelle que soit la valeur | « 230 m² », « 3 lots techniques » → non : *trois* lots ; mais « 1/50 », « 7 °C », « 4,65 de COP », « 840 m³/h » |
| **Date, millésime, montant** | toujours en **chiffres** | « 16 juin 2026 », « 3 mai 2007 », « 58 255,70 € HT » |
| **Ordinal de classement** | en **lettres** — exception explicite | « quatrième catégorie », « cinquième étage », « 5ᵉ catégorie » n'est admis qu'en citation d'un texte réglementaire |

La frontière porte sur la **nature** du nombre, pas sur sa taille : une quantité se compte, une mesure se lit sur un instrument. « Quatre chambres » et « 230 m² » cohabitent dans la même phrase sans contradiction.

### Relevé de référence

Mesure reproductible sur les dix-neuf récits, en ne comptant que les nombres qui qualifient directement un nom dénombrable (`logement`, `chambre`, `lit`, `niveau`, `place`, `zone`, `lot`, `bâtiment`, `étage`, `mission`, `semaine`, `réunion`, `réserve`, `cotraitant`, `poste`, `maison`, `appartement`) :

- **74** quantités sous dix, en lettres ;
- **37** quantités à partir de dix, en chiffres ;
- **2** écarts à la règle, à corriger à la prochaine passe rédactionnelle : « 6 maisons » (`fougerou-sainte-marie-de-re.md`) et « 4 chambres » (`hotel-yachtman-quai-valin-la-rochelle.md`).

Le chiffrage dépend entièrement du périmètre de noms retenu — l'élargir à tout substantif le multiplie par trois, en happant des fragments de mesures. Toute reprise de ce relevé doit republier sa méthode avec ses chiffres, faute de quoi ils ne veulent rien dire.

## Formes longues vs abréviations

- **Première occurrence** d'un acronyme dans une page : forme longue suivie de l'acronyme entre parenthèses. « Coordination SSI (sécurité incendie) ». Ensuite, l'acronyme suffit.
- **Pas d'abréviation** dans les titres `<h1>` et `<h2>` sauf si le terme est universellement connu (RE2020, BIM, SSI sont OK).

## Style des fiches projet — gabarit narratif

Structure recommandée en 3 à 6 paragraphes :

1. **L'enjeu** — un paragraphe qui pose la situation initiale : programme, contraintes, objectifs.
2. **La solution** — un à deux paragraphes sur l'approche FT2E : choix techniques, méthodologie, lots concernés.
3. **Les particularités** — un paragraphe sur ce qui distingue ce projet (innovation, contrainte de site, performance).
4. **Le résultat** — un paragraphe court avec un ou deux chiffres concrets.

## Microcopie — formulaires & navigation

| Contexte | Texte attendu |
|---|---|
| Bouton CTA principal | « Parlons de votre projet » |
| Lien retour références | « Voir toutes les références » |
| Erreur formulaire | « Ce champ est requis » (court, calme) |
| Confirmation envoi | « Message reçu — réponse sous 48 h ouvrées. » |
| Lien externe | toujours assorti d'une indication d'ouverture nouvelle |

## Articles & actualités

- **Titre** : 50–70 caractères, factuel ou interrogatif modeste. Pas de clickbait.
- **Chapô** : 2–3 phrases qui annoncent le contenu sans le résumer entièrement.
- **Date de publication** affichée en clair.
- **Auteur** : nom + fonction si interne, citation respectueuse si externe.
