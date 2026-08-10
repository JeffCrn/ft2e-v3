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

**Cette règle a été relevée, pas décrétée.** Elle décrit l'usage déjà en vigueur dans les vingt récits de `src/content/projets/`, constaté au 2026-08-09 : les récits l'appliquaient avant qu'elle soit écrite. Elle est consignée ici pour que les chapôs et les textes à venir s'y conforment sans avoir à la redécouvrir.

| Cas | Graphie | Exemple |
|---|---|---|
| **Quantité dont le nom s'écrit en un seul mot** | en **lettres** | « deux bâtiments », « quatre chambres », « sept niveaux », « **treize logements** », « **seize lots** », « **trente places** », « cent réunions » |
| **Quantité dont le nom est composé** | en **chiffres** | « 21 logements », « 26 locaux », « 46 chambres », « 102 lits » |
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

État des **vingt-trois** récits, remesuré le 2026-08-10 **après exécution de l'arbitrage** (passe de fin de chantier — le corpus applique désormais la règle du tableau des cas) :

| Bande | En lettres | En chiffres |
|---|---|---|
| de deux à neuf | **93** — conforme | **1** — la citation Yachtman |
| de dix à trente | **37** — tous d'un seul mot | **10** — tous composés |
| au-delà de trente | **1** — « soixante lits », un seul mot | **21** — tous composés |

**Zéro écart hors la citation Yachtman**, contrôlé par balayage des deux classes d'écart (nom d'un seul mot en chiffres, nom composé en lettres) sur le lexique du script. L'état antérieur à l'exécution — « 93 / 1 · 27 / 18 · 3 / 14 », publié le 2026-08-09 — se rejoue encore avec `--head` sur le commit d'avant la passe, à ceci près que la flexion des composés y était fausse (voir le cinquième piège ci-dessous).

Les chiffres ci-dessus remplacent le relevé « 71 / 27 / 13 / 3 / 12 » de la session 19, mesuré
sur vingt récits et avec un lexique plus étroit. Trois causes à l'écart, aucune éditoriale : le
corpus a gagné trois fiches, le lexique de noms a reçu **22 entrées** en session 21, et sa
fonction de flexion a été corrigée deux fois (`local` donnait *locals*, `repas` donnait
*repass*). **Un relevé n'est comparable qu'à périmètre et à lexique constants** : republier la
méthode avec les chiffres n'est pas une précaution de style.

⚠ **Le 62 de la mesure précédente était faux, et le script en était la cause.** Il engendrait ses pluriels par `nom + 's'`, ce qui donne *niveaus* : **aucune occurrence de « trois niveaux » ou « sept niveaux » n'a jamais été comptée**, alors que le tableau des cas ci-dessus cite « sept niveaux » comme exemple conforme. La flexion est désormais engendrée elle aussi — `-eau`, `-au` et `-eu` prennent `x`. Le passage de 62 à 71 se décompose en **sept occurrences jusque-là invisibles** dans les dix-neuf récits antérieurs (dont « sept niveaux » et « quatre niveaux » chez Yachtman) et **deux apportées** par la fiche de l'École des douanes. Les deux autres bandes ne bougent pas : aucun « niveaux » n'y figure.

C'est le troisième piège du même genre sur ce script, après la borne du lexique arrêtée à « trente » et le « trois » qui s'accrochait dans « quarante-trois ». Tous trois ont produit un zéro ou un sous-compte qui ressemblait à une mesure. **Un lexique engendré ne suffit pas : ses règles de flexion doivent l'être aussi.**

⚠ **Cinquième occurrence du piège, trouvée à l'exécution de l'arbitrage (2026-08-10)** : les noms **composés** du lexique n'étaient fléchis que sur leur dernier mot — `compte rendu` + `s` donnait *compte rendus*, jamais écrit. Les « 13 comptes rendus » de la fiche de Marans, que la S20 signalait comme invisibles, le sont restés **après** l'ajout de « compte rendu » au lexique en S21 : l'entrée existait, sa flexion non. La correction (chaque mot du composé se fléchit désormais) a révélé quatre occurrences de plus, dont deux composés en lettres — « quarante-cinq comptes rendus », « cinquante et un comptes rendus » — réécrits en chiffres dans la même passe.

- **Sous dix, plus aucun écart.** Le seul « 6 maisons » (`fougerou-sainte-marie-de-re.md`) a été corrigé le 2026-08-09 ; la seule occurrence chiffrée restante est la citation du contrat Yachtman, couverte par l'exception ci-dessus. Le relevé antérieur annonçait **2** écarts : il en comptait un de trop.
- **Au-delà de trente, conforme depuis le 2026-08-10** : 21 occurrences en chiffres, toutes composées (« 42 lits », « 54 maisons », « 152 réunions ») ; une seule en lettres, « soixante lits », d'un seul mot. Les trois composées en lettres (« quarante-six chambres », « quarante-trois postes », « trente-deux réunions ») ont été passées en chiffres, et « 60 lits » en lettres — soixante s'écrit en un mot, la règle ne connaît pas de bande.
- ✅ **Entre dix et trente : le point est tranché le 2026-08-09, et c'est la mesure qui l'a tranché.**
  L'ancienne règle — « à partir de dix, en chiffres » — décrivait **40 %** du corpus dans cette
  bande : 27 occurrences en lettres contre 18 en chiffres. Ce n'était pas un usage flottant, c'était
  une **règle fausse**. La ventilation des 18 occurrences chiffrées montre pourquoi : **dix sont des
  nombres composés** (21 salles, 26 locaux, 21 logements, 18 ballons, 19 lots) et **huit seulement
  des nombres d'un seul mot** (12 locaux, 12 chambres, 11 zones, 10 zones, 14 lits, 13 logements,
  13 lots, 11 places) ; or les 27 occurrences en lettres sont **toutes** d'un seul mot.
  **La frontière que suit le corpus n'est pas la valeur du nombre, c'est la longueur de son nom** —
  d'où la formulation retenue au tableau ci-dessus. Elle porte la conformité de 40 % à **82 %** et
  tranche du même coup les trois fiches qui se contredisaient d'un champ à l'autre :
  `fougerou` « vingt-sept » → **27**, `hotel-yachtman` « quarante-six chambres » → **46 chambres**,
  `exe-residence-horizon-mediatim` « 15 diffusions » → **quinze diffusions**.
  ✅ **Exécuté le 2026-08-10** : les 11 réécritures prévues, plus les cinq que l'instrument
  corrigé a révélées (« 13 comptes rendus » ×2, « quarante-cinq comptes rendus »,
  « cinquante et un comptes rendus », « 60 lits »). La réécriture d'une occurrence de récit
  s'est propagée aux champs `titre` et `synthese` qui portaient la même graphie
  (Maubec « treize logements », EHPAD « onze zones » / « dix zones ») : une fiche ne se
  contredit pas d'un champ à l'autre.
- ✅ **Les trois fiches qui se contredisaient d'un champ à l'autre sont alignées le 2026-08-10** : `fougerou` a « 27 calculs » aux deux champs, `exe-residence-horizon-mediatim` est tout en lettres (« Quinze diffusions » en synthèse, « quinze diffusions » et « quinze envois » au récit), `hotel-yachtman-quai-valin-la-rochelle` « 46 chambres » aux deux champs — la citation du contrat, « 4 chambres », reste intacte au titre de l'exception ci-dessus.

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
