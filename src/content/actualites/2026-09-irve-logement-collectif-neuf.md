---
titre: "IRVE en logement collectif neuf : réserver plutôt qu’équiper"
chapo: "La loi d’orientation des mobilités impose un pré-équipement de recharge dans les bâtiments neufs dotés de stationnement. Sur les opérations de logement du bureau, ce que le lot électricité livre n’est presque jamais une borne — c’est une réserve."
date: 2026-09-04
auteur: "L’équipe FT2E"
categories: ["Article technique"]
piliers:
  - /expertises/electricite
  - /secteurs/logements
en_avant: false
demo: false
---

La loi d’orientation des mobilités impose un pré-équipement en bornes de recharge pour véhicules électriques (IRVE) dans les bâtiments neufs et rénovés disposant de places de stationnement. Dans une opération de [logement](/secteurs/logements), la conséquence pratique est moins spectaculaire qu’on ne l’imagine, et plus structurante : le [lot électricité](/expertises/electricite) ne pose pas des bornes, il ménage la possibilité de les poser.

Trois opérations récentes montrent comment cette réserve se dimensionne — et une quatrième, tertiaire, montre ce qui se passe quand on équipe vraiment.

## Ce que le lot électricité livre réellement

À l’[habitat inclusif de quatorze logements à Salignac-sur-Charente](/references/habitat-inclusif-salignac-sur-charente), le parc de stationnement entre dans la tranche de dix à vingt places. Le dossier en tire deux dispositions : des fourreaux desservent 100 % des places, et 22 kVA sont réservés au local technique pour l’infrastructure de recharge. Aucune borne n’est au marché. Le bilan foisonné de l’opération s’établit à 119 kVA utiles, sans poste de distribution intégré au bâtiment.

Au [Pas des Bœufs, au Bois-Plage-en-Ré](/references/logements-pas-des-boeufs-bois-plage), le parc compte onze places, et la même obligation produit la même réponse : des fourreaux desservant 100 % d’entre elles.

À la [résidence intergénérationnelle de 21 logements à Saint-Agnant](/references/residence-intergenerationnelle-saint-agnant), le lot électricité va un cran plus loin et installe une borne de recharge, aux côtés du précâblage voix-données-images, du contrôle d’accès et de l’alarme incendie.

Trois opérations, un même texte, trois épaisseurs de réponse. Le point commun n’est pas le nombre de bornes : c’est que le génie civil et la réserve de puissance sont posés dans les deux cas où rien n’est équipé.

## Où la recharge entre dans le bilan de puissance

C’est le détail de calcul qui décide du raccordement, et il mérite d’être lu de près.

Au Pas des Bœufs, le bilan retient 9 kVA monophasés par maison, soit 90 kVA installés. Ces 90 kVA sont ramenés par un coefficient de foisonnement de 0,63, **puis augmentés des 15 kVA de la recharge des véhicules électriques** : le résultat est 71 kVA utiles, 103 A.

L’ordre des opérations n’est pas anodin. La recharge n’entre pas dans le foisonnement : elle s’y ajoute après. Une puissance ajoutée après coefficient pèse donc pour sa valeur entière, quand les mêmes 15 kVA passés au foisonnement n’en auraient pesé qu’une part. Sur cette opération, la réserve de recharge pèse ainsi au bilan alors qu’aucune borne n’est posée.

C’est là que se joue l’essentiel pour le maître d’ouvrage. Le raccordement se dimensionne une fois, il se négocie avec le gestionnaire de réseau, et il ne se reprend pas sans coût ni délai. La réserve de recharge n’est pas une ligne de plus au descriptif : c’est une part du contrat de fourniture.

## Comment on dimensionne quand on équipe pour de bon

Le corpus du bureau compte une opération où l’infrastructure a été menée de l’avant-projet à la réception. Elle est tertiaire, mais sa méthode de calcul est transposable, et elle éclaire la précédente par contraste.

Aux [bornes de recharge de la Caisse primaire d’assurance maladie, à La Rochelle et à Saintes](/references/bornes-irve-la-rochelle-saintes), le dimensionnement part de l’usage, pas de la prise. Chaque véhicule parcourt au plus 500 km par semaine ; à 20 kWh aux 100 km, la flotte rochelaise demande 400 kWh par semaine, celle de Saintes 300. Les véhicules stationnent de 18 h à 8 h, soit 14 h de charge par nuit et 70 h sur cinq nuits. La puissance utile ressort à 5,7 kW à La Rochelle et à 4,3 kW à Saintes.

Conclusion du calcul : une seule borne monophasée de 7 kW par site suffit. Mutualisée, elle alimente jusqu’à quatre points de charge et répartit les cycles entre eux — quatre points à La Rochelle pour quatre véhicules, trois à Saintes.

Le contraste avec l’intuition est net. Sept véhicules ne demandent pas sept bornes, et une borne de 7 kW n’est pas un sous-dimensionnement : c’est le résultat d’un calcul qui tient compte du temps disponible. Quatorze heures de stationnement nocturne changent tout ce qu’une puissance instantanée laisserait croire.

## Deux règles, et elles ne sont pas la même

Ce dossier fait apparaître ce qui reste implicite ailleurs : **la borne se dimensionne sur l’usage, l’amont se dimensionne sur l’avenir.** Les deux règles cohabitent sans se contredire.

À la Caisse primaire, l’aval est calculé au juste — une borne de 7 kW. L’amont est prévu large : chaque tableau divisionnaire est alimenté en 22 kW tétrapolaire depuis le tableau général, et deux emplacements identiques restent libres, chacun posé sur une phase par le synoptique. Trois bornes monophasées de 7 kW, une par phase, soit douze véhicules au total — sans retoucher le tableau général ni le raccordement. La contrainte de départ était d’ailleurs explicite : la puissance de raccordement de chaque site ne devait pas changer, ce qui écartait toute démarche auprès du gestionnaire de réseau.

Aux [bureaux Undertech de La Pallice](/references/undertech-la-pallice-la-rochelle), la même amorce est posée sur un programme tertiaire dont les preneurs sont inconnus : 44 kVA réservés au tableau général, un chemin de câbles capable de desservir un cinquième des places, et une seule borne équipée, sur la place accessible aux personnes à mobilité réduite. La recharge y est, selon les termes du dossier, anticipée plus qu’installée.

## Le partage à faire en conception

La règle qui en découle n’est pas propre à la recharge. Le bureau l’a formulée sur un tout autre ouvrage, la [chaufferie de l’école maternelle de La Flotte-en-Ré](/references/chaufferie-ecole-la-flotte-en-re), et elle s’applique mot pour mot ici : ce qui ne se reprend pas sans rouvrir la cour est dimensionné pour la suite ; ce qui s’ajoute par la suite est posé au juste besoin.

En logement collectif neuf, la ligne de partage tombe donc ainsi. Se posent maintenant, parce qu’ils supposent des tranchées, des réservations ou une renégociation de contrat : les fourreaux sur 100 % des places, les chemins de câbles, la place au tableau, et la puissance réservée dans le bilan. S’ajoutent plus tard, au rythme réel des besoins des occupants : les bornes elles-mêmes, leurs protections terminales et leur gestion.

Un dernier point de calendrier, souvent sous-estimé. À La Flotte, porter le raccordement du site de 72 à 250 kVA a demandé près de huit mois d’attente du distributeur — une saison de chauffe entière, sur un chantier dont tout le reste avait tenu ses délais. Le poste dimensionné pour les extensions à venir a été celui qui a coûté le plus de temps. Une réserve de puissance mal anticipée en conception ne se rattrape pas en phase travaux : elle se paie en mois.
