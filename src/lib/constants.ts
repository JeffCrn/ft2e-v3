export const SITE_NAME = 'FT2E';
export const SITE_TAGLINE = "Bureau d’études techniques, La Rochelle";
export const SITE_URL = 'https://ft2e.fr';

export const NAV_LINKS = [
  { label: 'Accueil', href: '/' },
  { label: 'Société', href: '/societe' },
  { label: 'Équipe', href: '/equipe' },
  { label: 'Expertises', href: '/expertises' },
  { label: 'Références', href: '/references' },
  { label: 'Actualités', href: '/actualites' },
  { label: 'Contact', href: '/contact' },
] as const;

export const FT2E_BUSINESS = {
  '@context': 'https://schema.org',
  '@type': 'ProfessionalService',
  name: 'FT2E',
  alternateName: "FT2E Bureau d’études",
  description:
    "Bureau d’études techniques pluridisciplinaire à La Rochelle. Fluides, thermique, électricité, sécurité incendie, BIM.",
  url: 'https://ft2e.fr',
  telephone: '+33546278593',
  email: 'ft2e@ft2e.fr',
  address: {
    '@type': 'PostalAddress',
    streetAddress: '35 Rue Nicolas Denys de Fronsac',
    addressLocality: 'La Rochelle',
    postalCode: '17000',
    addressCountry: 'FR',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: 46.1624398,
    longitude: -1.2089345,
  },
  areaServed: [
    'La Rochelle', 'Rochefort', 'Royan', 'Saintes',
    "Île de Ré", "Île d’Oléron", 'Niort', 'La Roche-sur-Yon',
    'Charente-Maritime', 'Vendée', 'Deux-Sèvres',
  ],
  foundingDate: '2008',
  knowsAbout: [
    'Fluides', 'Thermique', 'Électricité', 'Sécurité incendie',
    'BIM', 'RT2012', 'RE2020', 'Simulation thermique dynamique',
  ],
};

export const CHIFFRES_CLES = [
  { valeur: 17, suffixe: 'ans', label: "d’expertise", demo: false },
  { valeur: 7, suffixe: '', label: 'collaborateurs', demo: false },
  { valeur: 150, suffixe: '+', label: 'projets livrés', demo: true },
  { valeur: 3200, suffixe: '+', label: 'logements conçus', demo: true },
] as const;
