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

### L'exception de citation

**Un nombre cité entre guillemets se transcrit tel qu'il figure dans la pièce.** La fidélité au texte cité prime sur la convention du site : corriger un chiffre à l'intérieur d'une citation, c'est falsifier la pièce.

Occurrence en corpus — `hotel-yachtman-quai-valin-la-rochelle.md` cite l'article premier du contrat : « notre mission sera limitée à la création des **4 chambres** au R+1 et au réaménagement du RDC ». Le « 4 » reste. Ce n'est pas un écart, et le relevé ci-dessous ne le compte pas comme tel.

La même logique couvre déjà l'ordinal réglementaire de la dernière ligne du tableau (« 5ᵉ catégorie » admis en citation).

### Relevé de référence — mesuré le 2026-08-09

Le relevé **se rejoue** : `scripts/releve-numeral.py` (sans argument pour mesurer le disque, `--head` pour mesurer le dernier commit). Ne sont comptés que les nombres qui qualifient **directement** un nom dénombrable d'une liste close — `logement`, `chambre`, `lit`, `niveau`, `place`, `zone`, `lot`, `bâtiment`, `étage`, `mission`, `semaine`, `réunion`, `réserve`, `cotraitant`, `poste`, `maison`, `appartement`, singulier et pluriel. `un` et `une` sont exclus : ils sont article aussi souvent que numéral. Frontmatter exclu, corps de récit seul.

État des dix-neuf récits après la passe du 2026-08-09 :

| Bande | En lettres | En chiffres |
|---|---|---|
| de deux à neuf | **62** — conforme | **1** — la citation Yachtman |
| de dix à trente | **27** | **13** |
| au-delà de trente | **3** | **12** |

- **Sous dix, plus aucun écart.** Le seul « 6 maisons » (`fougerou-sainte-marie-de-re.md`) a été corrigé le 2026-08-09 ; la seule occurrence chiffrée restante est la citation du contrat Yachtman, couverte par l'exception ci-dessus. Le relevé antérieur annonçait **2** écarts : il en comptait un de trop.
- **Au-delà de trente, le chiffre domine sans régner** : douze occurrences en chiffres (« 42 lits », « 54 maisons », « 152 réunions ») contre trois en lettres (« quarante-six chambres », « quarante-trois postes », « trente-deux réunions »).
- ⚠ **Entre dix et trente, l'usage contredit la règle du tableau** : **27** occurrences en lettres (« treize logements », « seize lots », « trente places ») contre **13** en chiffres (« 12 chambres », « 11 zones », « 21 logements »). La consigne « à partir de dix, en chiffres » décrit donc la minorité du corpus, dans une bande où celui-ci n'est de toute façon pas cohérent avec lui-même. **Point ouvert, à trancher avant la prochaine passe rédactionnelle** — soit le seuil monte (les nombres qui s'écrivent en un mot restent en lettres jusqu'à trente, les composés passent en chiffres), soit 27 occurrences se réécrivent. Ne rien décider laisse en place une règle que le corpus désobéit deux fois sur trois.
- ⚠ **Trois fiches se contredisent d'un champ à l'autre** — même nombre, deux graphies dans le même fichier, donc lisibles d'un seul écran puisque la synthèse surmonte le récit : `fougerou` (« 27 calculs » en `synthese`, « vingt-sept » au récit), `exe-residence-horizon-mediatim` (« 15 diffusions » / « quinze envois »), `hotel-yachtman-quai-valin-la-rochelle` (« 46 chambres » / « quarante-six chambres »). L'arbitrage du seuil les tranchera toutes les trois d'un coup ; les corriger avant serait les corriger deux fois.

**Le lexique du script est engendré, jamais tapé.** Sa première version s'arrêtait à « trente » et concluait « au-delà de trente, jamais de lettres » : ce zéro n'était pas une mesure mais la forme du dictionnaire renvoyée en écho — les « quarante-six chambres » du corpus n'y avaient pas d'entrée. Pire, « quarante-trois postes » était compté dans la bande basse, l'entrée « trois » s'accrochant après le trait d'union. Toute extension du relevé doit engendrer ses formes, pas les énumérer.

Le chiffrage dépend entièrement du périmètre de noms retenu — l'élargir à tout substantif le multiplie par trois, en happant des fragments de mesures. Toute reprise de ce relevé doit republier sa méthode avec ses chiffres, faute de quoi ils ne veulent rien dire. **Les chiffres ci-dessus remplacent le relevé « 74 / 37 / 2 » de la première rédaction, dont la méthode n'a pas pu être reproduite** — seul son décompte d'écarts l'a été. C'est la raison d'être du script : un relevé qu'on ne peut pas rejouer n'est pas une mesure.

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
