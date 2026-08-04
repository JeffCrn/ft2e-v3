# Prompts de génération — visuels des fiches projet de démo

> Archive des prompts utilisés pour générer les **7 visuels des références démo** du site
> (la photo de la Maison Pierre Loti n'est pas dans cette série — visuel fourni séparément par FT2E).
> Modèle cible : Midjourney v6.1 avec paramètres `--ar 3:2 --style raw --v 6.1`.
> Alternative : Flux 1.1 Pro / Imagen 3 (retirer les flags `--ar` et préciser « horizontal 3:2 aspect ratio »).

## Style commun

Esthétique « rendu architectural — perspective de promoteur » :
- 3D photoréaliste *soft*, ni cartoon ni hyper-photo
- Façades blanches enduites + bardage bois clair + attique zinc/foncé + soubassement pierre claire
- Personnages silhouettes discrètes (faceless), pas de visages identifiables
- Ciel bleu clair + cumulus diffus, lumière douce d'après-midi
- Palette muted : blanc / gris / bois clair / verts naturels / bleu ciel, **faible saturation**
- Cadrage 3/4 oblique au sol, large
- Aucun texte, logo ou panneau

## Recommandations d'usage

1. Générer les 7 dans la **même session du même modèle**, avec les mêmes flags, pour la cohérence sérielle.
2. Si rendu trop générique : ajouter « *architectural rendering style of MIR studio* » ou « *Stefano Boeri architectural visualization style* ».
3. Si rendu trop saturé : ajouter « *low saturation, matte finish, no HDR effect* ».
4. Si les humains sortent mal : retirer les personnages, ajouter « *no people* ».
5. Format de sortie : `.jpg` ~1600 px de large, qualité 80 → ~300-500 KB par image.
6. Nommer chaque fichier `01.jpg` dans `public/images/projets/<slug>/01.jpg` — la détection est automatique via `fs.existsSync` au build.

---

## 1. Centre nautique intercommunal · Île de Ré · Sport, Neuf

```
Contemporary intercommunal aquatic center on Île de Ré, France, low-rise
volumes with large glazed swimming hall facades opening onto a sandy
landscaped forecourt, pale grey standing-seam zinc roof, light timber
cladding alternating with white rendered walls, tall coastal reeds and
Atlantic dune grasses in the foreground, two cyclists arriving at the
entrance plaza as faceless silhouettes, architectural visualization, soft
photorealistic 3D rendering, soft afternoon daylight, blue sky with
scattered cumulus clouds, muted natural color palette, ground-level
three-quarter perspective, calm coastal atmosphere, no text, no logo,
no signage --ar 3:2 --style raw --v 6.1
```

## 2. EHPAD Le Doux-Refuge · Saintes · Santé, Réhabilitation

```
Three-storey nursing home (EHPAD) in Saintes, France, after thermal
renovation, freshly rendered white and warm grey facades, generous
balconies with light timber railings, large windows with discreet
exterior blinds, surrounded by a quiet therapeutic garden with mature
trees, gravel walking paths and wooden benches, an elderly resident and
a caregiver strolling along a path as faceless silhouettes, architectural
visualization, soft photorealistic 3D rendering, late morning daylight,
blue sky with thin cirrus clouds, muted natural palette of white, warm
grey and soft green, ground-level three-quarter perspective, peaceful
and dignified atmosphere, no text, no logo, no signage
--ar 3:2 --style raw --v 6.1
```

## 3. EXE 120 logements PSLA Bouygues · La Rochelle · Logement, Études d'exécution

```
Construction site of a 120-unit residential housing project in La Rochelle,
France, three R+4 buildings nearing completion, white rendered facades
partially installed, light timber cladding being mounted on balconies,
scaffolding still visible on one wing, a tower crane in the background,
two construction workers in high-visibility vests reviewing technical
plans in the foreground as faceless silhouettes, fenced perimeter,
architectural visualization, soft photorealistic 3D rendering, soft
morning daylight, blue sky with scattered clouds, muted natural color
palette with subtle high-visibility yellow accents, ground-level
three-quarter perspective, professional and orderly worksite atmosphere,
no readable text, no logo, no signage --ar 3:2 --style raw --v 6.1
```

## 4. Extension école primaire · Royan · Tertiaire, Extension

```
Single-storey contemporary extension of a French primary school in Royan,
timber-clad volume with large south-facing windows and steel sun
awnings, attached to an existing 1980s school building partially visible
on the side, paved schoolyard with painted hopscotch markings and young
trees in planters, a few children at play in the courtyard as faceless
silhouettes, distant glimpse of Atlantic coastal vegetation in the
background, architectural visualization, soft photorealistic 3D rendering,
midday daylight, blue sky with light clouds, muted natural color palette
of light timber, white, soft greens and sand tones, ground-level
three-quarter perspective, joyful and welcoming atmosphere, no text,
no logo, no signage --ar 3:2 --style raw --v 6.1
```

## 5. Réhabilitation Mireuil · La Rochelle · Logement social, Réhabilitation

```
Three R+4 social housing blocks in the Mireuil neighborhood of La
Rochelle, France, after thermal renovation with external insulation,
freshly rendered white and warm beige facades with discreet vertical
timber accents on balcony fronts, regular window grids with new aluminum
joinery, replanted courtyards between the buildings with paved walking
paths and wooden benches, residents chatting on a bench and a cyclist
passing through as faceless silhouettes, architectural visualization,
soft photorealistic 3D rendering, soft afternoon daylight, blue sky with
scattered cumulus clouds, muted natural palette of white, warm beige,
soft green and pale grey, ground-level three-quarter perspective, calm
residential atmosphere, no text, no logo, no signage
--ar 3:2 --style raw --v 6.1
```

## 6. Résidence Les Quais Domidylle · La Rochelle · Logement, Neuf

```
Contemporary residential building of 48 apartments along a renovated
quay in La Rochelle, France, four-storey volume with white rendered
facades, vertical light timber cladding on loggias and balconies, dark
zinc-clad upper attic level, pale limestone base, paved waterfront
promenade in the foreground with a cyclist with a backpack and a parent
walking with a child as faceless silhouettes, sailboat masts visible in
the harbor background, architectural visualization, soft photorealistic
3D rendering, soft afternoon daylight, blue sky with scattered cumulus
clouds, muted natural color palette, ground-level three-quarter
perspective, calm and bright maritime atmosphere, no text, no logo, no
signage --ar 3:2 --style raw --v 6.1
```

## 7. Siège régional tertiaire · Niort · Tertiaire, Neuf

```
Contemporary three-storey regional corporate headquarters in Niort,
France, sober rectangular volume with white rendered facades and large
aluminum-framed glazed openings, vertical brise-soleil louvers on the
south facade, light timber accents around the main entrance canopy,
landscaped forecourt with parking bays and ornamental grasses, a few
employees walking toward the entrance and a visitor seated on a bench
as faceless silhouettes, architectural visualization, soft photorealistic
3D rendering, late morning daylight, blue sky with light clouds, muted
natural color palette of white, light timber and soft greys, ground-level
three-quarter perspective, professional and welcoming atmosphere, no
text, no logo, no signage --ar 3:2 --style raw --v 6.1
```
