# Prompts de génération — visuels de l'équipe

> Archive des prompts utilisés pour la **photo collective** de l'équipe FT2E
> (les 7 portraits individuels du board ont été cadrés sur un fond studio par FT2E,
> sans prompt particulier — pas archivés ici).
> Modèle cible : Midjourney v6.1, paramètres `--ar 3:2 --style raw --v 6.1`.

## Contraintes éditoriales rappelées

- **Équipe chaleureuse, réaliste, qui pose pour la photo** (visages visibles, sourires sincères)
- **Pas de silhouettes ni d'environnement trop « architecte »** — bureau ordinaire de PME française
- **Aucune distinction individuelle** (règle CLAUDE.md « team uniformity ») — pas de leader central
- **Mixité respectée** : équipe FT2E réelle = 3 hommes / 4 femmes
- **Anti-Fotolia** : aucun cliché stockphoto (high-five, bras croisés en formation, pouce levé, tablette-accessoire)

## Prompt principal — photo collective

```
Authentic candid-posed group portrait of a small French multidisciplinary
engineering team in La Rochelle, about seven members, mixed ages from
late twenties to mid-fifties, gender-balanced with slightly more women
than men, gathered naturally in their actual working office — an
ordinary sober professional space with white painted walls, light wood
and grey laminate desks, standard black office chairs, modest grey
office carpet, soft ceiling LED lighting complemented by daylight from
a side window, a few technical drawings of building systems pinned
discreetly on a side wall, a small architectural model visible on a
shelf in the soft background, green plants in pale ceramic pots, the
team standing in a relaxed natural arrangement at slightly varied depths
— not in a stiff line, some half a step in front, others behind —
looking warmly at the camera with genuine soft authentic smiles, no
forced expressions, wearing comfortable casual professional attire
(knit sweaters, plain shirts, dark chinos or jeans, simple sneakers or
loafers, no suits, no ties), nobody positioned as a central leader,
equal visual weight given to every face, warm natural color photography,
soft daylight, 35mm lens look, medium aperture with everyone in sharp
focus, subtle film grain, the feeling of a real working team momentarily
pausing their work for the photograph, French regional PME atmosphere
--ar 3:2 --style raw --v 6.1 --no high-five, crossed-arms, thumbs-up,
tablet-prop, laptop-prop, suit, tie, white-studio-background, over-
saturated-colors, glossy-corporate-look, perfect-teeth, model-poses
```

## Variantes testables si rendu décevant

### A — vue plus aérée
Remplacer « *the team standing in a relaxed natural arrangement at slightly varied depths* » par :
> *the team naturally scattered around their desks and the meeting corner — some standing, some seated on a desk edge or chair, one leaning casually against a wall — all turned toward the camera with relaxed smiles*

### B — détails du métier plus visibles
Ajouter avant `--ar 3:2` :
> *one team member casually holding a rolled-up technical plan under their arm, another with a hand resting on a small architectural model on a nearby desk, suggesting work just paused*

### C — ancrage La Rochelle discret
Ajouter dans la description du décor :
> *a soft glimpse of the La Rochelle harbor visible through a window in the far background, slightly defocused*

## Stratégie de génération recommandée

1. Lancer le prompt principal seul d'abord.
2. Si trop figé → variante A.
3. Si on veut un signal métier → ajouter B au prompt principal.
4. **Ne pas cumuler A + B + C** dans un même prompt (surcharge → décrochage du modèle).
5. Prévoir 3-5 régénérations : composer un groupe de 7 avec visages nets reste difficile.
