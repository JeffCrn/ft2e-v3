// Données des CV de l'équipe FT2E — source : PDF transmis le 2026-08-05 (dossier cv/, non versionné).
// Coquilles des originaux corrigées : « 20012 » → 2012, « VOLTAREO » → VOLTAERO,
// Saint-Trojan-les-Bains (75) → (17), SPIE Saint-Herblain (17) → (44), Stade de France (75) → (93).

export const NBSP = ' ';

export const cvs = [
  {
    slug: 'Mathieu-Braud',
    prenom: 'Mathieu',
    nom: 'Braud',
    titre: 'Ingénieur Efficacité Énergétique & Énergies Renouvelables',
    fonction: 'Chargé d’affaires CVC et fluides',
    experience: '10 ans d’expérience en BET',
    statut: 'Co-gérant de FT2E depuis le 1ᵉʳ janvier 2026',
    contact: [
      ['téléphone', '05 46 27 85 93'],
      ['email', 'm.braud@ft2e.fr'],
    ],
    formations: [
      { annee: '2014', titre: 'Master 2 Gestion et intégration de l’efficacité énergétique et des énergies renouvelables', lieu: 'La Rochelle' },
      { annee: '2013', titre: 'Master 1 Équipements techniques et énergie', lieu: 'La Rochelle' },
      { annee: '2017', titre: 'Revit MEP — Atlancad', lieu: '5 jours de formation' },
      { annee: '2025', titre: 'ENR filière thermique', lieu: 'Bois énergie, biomasse et cogénération' },
    ],
    logiciels: ['Finalcad', 'Revit', 'AutoCAD LT', 'Optima Sydev'],
    realisations: [
      { annee: '2025', titre: 'Caravelle — réhabilitation d’un hôtel en logements', lieu: 'Rochefort (17)', detail: 'Conception chauffage / VMC / plomberie' },
      { annee: '2024', titre: 'Dufour Yachts — bâtiment industriel', lieu: 'La Rochelle (17)', detail: 'Conception CVC / VMC / plomberie · air comprimé / RIA' },
      { annee: '2023', titre: 'AP Yacht — bâtiment industriel', lieu: 'Marans (17)', detail: 'Conception CVC / VMC / plomberie · air comprimé / RIA' },
      { annee: '2022', titre: 'Voltaero — bâtiment industriel', lieu: 'Saint-Agnant (17)', detail: 'Conception CVC / VMC / plomberie · air comprimé / RIA' },
      { annee: '2021', titre: 'Aurora — construction de 150 logements', lieu: 'La Rochelle (17)', detail: 'Conception chauffage / VMC / plomberie' },
    ],
    experiences: [
      {
        periode: 'Depuis septembre 2015',
        poste: 'Technicien bureau d’études',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Conception des installations',
          'Réalisation des dossiers d’appels d’offres',
          'Estimation des travaux',
          'Suivi, contrôle et réception des travaux réalisés',
        ],
      },
      {
        periode: 'Mars – août 2015',
        poste: 'Stage de fin d’études',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Réglementation thermique RT2012 : maisons individuelles, logements collectifs, tertiaire',
          'Plans chauffage, ventilation, plomberie',
          'Dossiers de consultation des entreprises',
        ],
      },
      {
        periode: 'Juillet – août 2014',
        poste: 'Stage',
        org: 'TH2i — La Rochelle (17)',
        points: [
          'Dimensionnement de systèmes énergétiques',
          'Plans de chauffage, ventilation, plomberie',
        ],
      },
    ],
  },

  {
    slug: 'Geraldine-Michaud',
    prenom: 'Géraldine',
    nom: 'Michaud',
    titre: 'Ingénieur Thermique & Énergies Renouvelables',
    fonction: 'Calculs réglementaires, faisabilité, audit thermique, STD · Chargée d’études CVC et fluides',
    experience: '17 ans d’expérience en BET',
    statut: 'Co-gérante de FT2E depuis le 1ᵉʳ janvier 2026',
    contact: [
      ['téléphone', '05 46 27 85 93'],
      ['email', 'g.michaud@ft2e.fr'],
    ],
    formations: [
      { annee: '2008', titre: 'Master 1 et 2 Matériaux pour les énergies renouvelables et l’environnement', lieu: 'Poitiers' },
      { annee: '2020', titre: 'Simulation thermique dynamique', lieu: 'Logiciels Perrenoud — 1 jour' },
      { annee: '2021', titre: 'RE2020 + ACV, logements et tertiaire', lieu: 'Logiciels Perrenoud — 4 jours' },
      { annee: '2021', titre: 'Mise en application de la RE2020, des règles Th-BCE 2020 et du calcul ACV dynamique', lieu: '' },
      { annee: '2023', titre: 'Audit énergétique', lieu: 'Tertiaire, logements collectifs — 3 jours' },
    ],
    logiciels: ['Perrenoud (RE2020, RT2012, déperditions, STD, apports)', 'AutoCAD LT', 'Optima Sydev', 'Finalcad', 'BAO Évolution'],
    realisations: [
      { annee: '2024', titre: 'École primaire', lieu: 'La Flotte-en-Ré (17)', detail: 'Audit énergétique format ADEME' },
      { annee: '2023', titre: 'Construction de 20 logements', lieu: 'Saint-Rogatien (17)', detail: 'Calcul réglementaire RE2020 — label NF Habitat HQE · conception chauffage / ventilation / plomberie / sanitaire' },
      { annee: '2022', titre: 'Voltaero — bâtiment industriel', lieu: 'Saint-Agnant (17)', detail: 'Calcul réglementaire RT2012 — Cep −40 %' },
      { annee: '2021', titre: 'Aurora — construction de 150 logements', lieu: 'La Rochelle (17)', detail: 'Calcul réglementaire RT2012 −20 %' },
    ],
    experiences: [
      {
        periode: 'Depuis septembre 2008',
        poste: 'Technicienne bureau d’études',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Réglementation thermique : maisons individuelles, logements collectifs, tertiaire',
          'Audits énergétiques, études de faisabilité',
          'Simulation thermique dynamique',
        ],
      },
      {
        periode: 'Septembre 2007 – juin 2008',
        poste: 'Technicienne bureau d’études',
        org: 'TH2i — La Rochelle (17)',
        points: [
          'Application de la réglementation thermique 2005 : maisons individuelles, logements collectifs, tertiaire',
        ],
      },
      {
        periode: 'Mars – juin 2007',
        poste: 'Stage de fin d’études',
        org: 'TH2i — La Rochelle (17)',
        points: [
          'Suivi de projets intégrant des énergies renouvelables, sous le contrôle du chargé d’affaires',
        ],
      },
    ],
  },

  {
    slug: 'Sandrine-Rameau',
    prenom: 'Sandrine',
    nom: 'Rameau',
    titre: 'Ingénieur Efficacité Énergétique & Énergies Renouvelables',
    fonction: 'Calculs réglementaires RE2020, simulation thermique dynamique · Chargée d’études CVC et fluides',
    experience: '18 ans d’expérience dont 9 en BET',
    statut: '',
    contact: [
      ['téléphone', '05 46 27 85 93'],
      ['email', 's.rameau@ft2e.fr'],
    ],
    formations: [
      { annee: '2003', titre: 'Ingénieur Génie de l’environnement', lieu: '' },
      { annee: '2005 – 2006', titre: 'Master Sciences et technologies, spécialité I3ER', lieu: '' },
      { annee: '2021', titre: 'Mise en application de la RE2020, des règles Th-BCE 2020 et du calcul ACV dynamique', lieu: '' },
    ],
    logiciels: ['Perrenoud (RE2020, RT2012, déperditions, STD, apports)', 'Finalcad', 'Revit', 'BAO Évolution', 'AutoCAD LT', 'Optima Sydev'],
    realisations: [
      { annee: '2024', titre: 'Construction de 10 logements sociaux', lieu: 'Le Bois-Plage-en-Ré (17)', detail: 'Calcul réglementaire RE2020 −10 % · conception chauffage / ventilation / plomberie / sanitaire' },
      { annee: '2023', titre: 'Résidence intergénérationnelle', lieu: 'Saint-Agnant (17)', detail: 'Calcul réglementaire RE2020 −10 % · conception ventilation / plomberie / sanitaire' },
      { annee: '2023', titre: 'Nerea — 48 logements sociaux collectifs', lieu: 'Aytré (17)', detail: 'Calcul réglementaire RT2012 −20 % — label NF Habitat' },
      { annee: '2023', titre: 'Chambre des métiers et de l’artisanat', lieu: 'La Rochelle (17)', detail: 'Audit énergétique — décret tertiaire' },
    ],
    experiences: [
      {
        periode: 'Depuis septembre 2015',
        poste: 'Technicienne bureau d’études',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Conception des installations CVC et électricité courants forts et faibles',
          'Réglementation thermique : maisons individuelles, logements collectifs, tertiaire',
          'Audits énergétiques, études de faisabilité',
        ],
      },
      {
        periode: 'Novembre 2006 – octobre 2015',
        poste: 'Chargée d’affaires',
        org: 'Groupe INTIS-DIBAO — La Rochelle (17)',
        points: [
          'Ingénierie thermique et installations solaires',
          'Dimensionnement de systèmes mettant en œuvre des énergies renouvelables',
          'Spécialités : aérothermie, géothermie, aquathermie, solaire thermique et photovoltaïque, bois énergie',
        ],
      },
    ],
  },

  {
    slug: 'Vincent-Jaoul',
    prenom: 'Vincent',
    nom: 'Jaoul',
    titre: 'Ingénieur Électrotechnique',
    fonction: 'Chargé d’affaires électricité · Coordinateur SSI',
    experience: '30 ans d’expérience dont 25 en BET',
    statut: '',
    contact: [
      ['portable', '06 32 56 12 84'],
      ['téléphone', '05 46 27 85 93'],
      ['email', 'v.jaoul@ft2e.fr'],
    ],
    formations: [
      { annee: '1995', titre: 'Ingénieur ENSEEIHT', lieu: 'École nationale supérieure d’électrotechnique, d’informatique et d’hydraulique de Toulouse' },
      { annee: '2003', titre: 'Coordinateur des systèmes de sécurité incendie', lieu: '' },
      { annee: '2025', titre: 'Étude de conception IRVE', lieu: '' },
    ],
    logiciels: ['Finalcad', 'AutoCAD LT', 'Dialux EVO', 'Elium 4.1', 'Caneco', 'IP Video Design Tool'],
    realisations: [
      { annee: '2024', titre: 'Fountaine Pajot — bâtiment industriel', lieu: 'Aigrefeuille-d’Aunis (17)', detail: 'Conception électricité CFO / CFA / SSI' },
      { annee: '2023', titre: 'AP Yacht — bâtiment industriel', lieu: 'Marans (17)', detail: 'Conception électricité CFO / CFA / SSI' },
      { annee: '2023', titre: 'Undertech — bureaux', lieu: 'La Rochelle (17)', detail: 'Conception CFO / CFA / photovoltaïque' },
      { annee: '2022', titre: 'Cabanes urbaines', lieu: 'La Rochelle (17)', detail: 'Conception électricité CFO / CFA / coordination SSI' },
      { annee: '2021', titre: 'Restructuration d’une salle polyvalente', lieu: 'Saint-Trojan-les-Bains (17)', detail: 'Conception électricité CFO / CFA / coordination SSI' },
      { annee: '1997', titre: 'Boucle HTA — université Pierre-et-Marie-Curie', lieu: 'Paris (75)', detail: 'Études d’exécution' },
      { annee: '1995', titre: 'Parc de stationnement du Stade de France', lieu: 'Saint-Denis (93)', detail: 'Étude d’exécution CFO / CFA' },
    ],
    experiences: [
      {
        periode: 'Depuis 2018',
        poste: 'Chargé d’affaires électricité',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Gestion des projets en électricité courants forts et faibles',
          'Coordination des systèmes de sécurité incendie',
          'Contrôle et suivi technique de chantier',
        ],
      },
      {
        periode: '2003 – 2018',
        poste: 'Bureau d’études BETOM Ingénierie',
        org: 'Périgny (17)',
        points: [
          'Gestion des projets en électricité courants forts et faibles',
          'Études de projet en conception-construction, PPP',
          'Coordination des systèmes de sécurité incendie',
          'Contrôle et suivi technique de chantier',
        ],
      },
      {
        periode: '2000 – 2003',
        poste: 'Bureau d’études B2I',
        org: 'La Rochelle (17)',
        points: [
          'Gestion des projets en électricité courants forts et faibles',
          'Chiffrage pour entreprise',
          'Études d’exécution',
        ],
      },
      {
        periode: '1995 – 2000',
        poste: 'Bureau d’études BETEG',
        org: 'Paris (75)',
        points: [
          'Études d’exécution et de conception',
          'Assistance technique dans l’entreprise Forclum',
        ],
      },
    ],
  },

  {
    slug: 'Tanguy-Moinet',
    prenom: 'Tanguy',
    nom: 'Moinet',
    titre: 'Projeteur Électrotechnique',
    fonction: 'Technicien d’études électricité et SSI',
    experience: '10 ans d’expérience dont 5 en BET',
    statut: '',
    contact: [
      ['téléphone', '05 46 27 85 93'],
      ['email', 't.moinet@ft2e.fr'],
    ],
    formations: [
      { annee: '2024', titre: 'Formation NF C 14-100', lieu: 'Dimensionnement des colonnes électriques et distribution basse tension' },
      { annee: '2015 – 2016', titre: 'Licence professionnelle Génie électrique pour le bâtiment, en alternance', lieu: 'IUT d’Angers' },
      { annee: '2013 – 2015', titre: 'BTS Électrotechnique énergie équipements communicants', lieu: 'Lycée Paul-Guérin, Niort' },
      { annee: '2010 – 2013', titre: 'Baccalauréat professionnel Électrotechnique', lieu: 'Lycée Rompsay, La Rochelle' },
    ],
    logiciels: ['AutoCAD LT', 'Dialux EVO', 'Finalcad', 'Elium 4.1', 'Optima Sydev', 'Caneco'],
    realisations: [
      { annee: '2023', titre: 'Dufour Yachts — bâtiment industriel', lieu: 'Périgny (17)', detail: 'Conception électricité CFO / CFA / SSI' },
      { annee: '2022', titre: 'Auberge Central Hostel', lieu: 'La Rochelle (17)', detail: 'Conception électricité CFO / CFA' },
      { annee: '2019', titre: 'Aurora — 150 logements', lieu: 'La Rochelle (17)', detail: 'Conception électricité' },
      { annee: '2017', titre: 'La Poste', lieu: 'Saint-Martin-de-Ré (17)', detail: 'Conception électricité' },
    ],
    experiences: [
      {
        periode: 'Depuis 2020',
        poste: 'Technicien bureau d’études',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Gestion des projets d’études de conception courants forts et faibles',
          'Coordination des systèmes de sécurité incendie',
          'Contrôle et suivi technique des travaux',
        ],
      },
      {
        periode: '2017 – 2019',
        poste: 'Technicien bureau d’études',
        org: 'SPIE — La Rochelle (17)',
        points: [
          'Réalisation des études d’exécution',
          'Chiffrage d’appels d’offres',
          'Dossiers d’ouvrages exécutés',
        ],
      },
      {
        periode: '2016 – 2017',
        poste: 'Assistant chargé d’affaires',
        org: 'SPIE — Saint-Herblain (44)',
        points: [
          'Préparation des dossiers techniques pour l’installation d’antennes relais mobiles',
        ],
      },
      {
        periode: '2015 – 2016',
        poste: 'Technicien bureau d’études',
        org: 'SNEE — La Rochelle (17)',
        points: [
          'Réalisation des études d’exécution',
          'Dossiers d’ouvrages exécutés',
        ],
      },
    ],
  },

  {
    slug: 'Emma-Slawski',
    prenom: 'Emma',
    nom: 'Slawski',
    titre: 'Ingénieur Efficacité Énergétique & Énergies Renouvelables',
    fonction: 'Chargée d’affaires CVC et fluides',
    experience: '2 ans et demi d’expérience en BET',
    statut: '',
    contact: [
      ['téléphone', '05 46 27 95 93'],
      ['email', 'e.slawski@ft2e.fr'],
    ],
    formations: [
      { annee: '2024', titre: 'Master Génie civil, parcours GI3ER', lieu: 'La Rochelle' },
      { annee: '2021 – 2022', titre: 'Licence 3 Génie civil', lieu: 'La Rochelle — mécanique des fluides, équipements techniques (VMC, chauffage)' },
      { annee: '2019 – 2021', titre: 'DUT Génie civil — construction durable', lieu: 'La Rochelle — PHPP, Pléiades (RT2012, STD), ACV base INIES, projet tuteuré maisons passives bois' },
    ],
    logiciels: ['AutoCAD LT', 'Perrenoud', 'Revit', 'Optima Sydev'],
    realisations: [
      { annee: '2025', titre: 'Bureaux Enersteel — tertiaire', lieu: 'La Rochelle (17)', detail: 'Conception CVC / VMC / plomberie · air comprimé / RIA' },
      { annee: '2024', titre: 'Dufour Yachts — bâtiment industriel', lieu: 'La Rochelle (17)', detail: 'Conception CVC / VMC / plomberie · air comprimé / RIA' },
      { annee: '2023', titre: 'Hangar 17 — 34 logements', lieu: 'La Rochelle (17)', detail: 'Conception VMC / plomberie' },
      { annee: '2022', titre: 'AP Yacht — bâtiment industriel', lieu: 'Marans (17)', detail: 'Conception VMC / plomberie · air comprimé / RIA' },
    ],
    experiences: [
      {
        periode: 'Depuis septembre 2024',
        poste: 'Technicienne bureau d’études',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Gestion des projets d’études de conception CVC',
          'Contrôle et suivi technique des travaux',
        ],
      },
      {
        periode: 'Février – juillet 2024',
        poste: 'Stage de Master 2',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Dimensionnement de chaufferie',
          'Audits thermiques CCAS',
          'Plans CVC Revit · RT2012, RE2020',
        ],
      },
      {
        periode: 'Juillet 2023 et juillet 2024',
        poste: 'CDD',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Dimensionnement de conduits VMC',
          'Plans CVC AutoCAD',
        ],
      },
      {
        periode: 'Février – avril 2023',
        poste: 'Stage de Master 1',
        org: 'FT2E — La Rochelle (17)',
        points: [
          'Plans CVC Revit · RT2012, RE2020',
        ],
      },
    ],
  },
];
