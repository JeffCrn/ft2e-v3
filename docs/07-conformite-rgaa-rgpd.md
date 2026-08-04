# 07 · Conformité RGAA & RGPD

## RGAA — Accessibilité

### Cible

**RGAA 4.1 niveau AA** sur 100 % des pages publiques au lancement.

### Implémentation

Voir `.claude/rules/accessibility-rgaa.md` pour la checklist opérationnelle. Voir aussi `.claude/agents/a11y-auditor.md` pour l'audit automatisé.

### Déclaration d'accessibilité

Une page `/accessibilite` publiée au lancement, contenant :

1. **État de conformité** : « Conforme RGAA 4.1 AA » ou « Partiellement conforme » selon résultats d'audit final.
2. **Résultats de l'audit** : date, méthode, échantillon de pages testées, score obtenu.
3. **Dérogations éventuelles** : listées de manière transparente.
4. **Mécanisme de signalement** : email ou formulaire pour qu'un visiteur signale un problème d'accessibilité.
5. **Coordonnées du défenseur des droits** (texte légal).

Générateur officiel à utiliser : `https://accessibilite.numerique.gouv.fr/`.

### Maintien dans le temps

- Audit complet **annuel** minimum.
- Audit ponctuel à chaque ajout structurel (nouveau type de page, nouveau composant majeur).
- Tests utilisateurs avec personne handicapée recommandés (NVDA, VoiceOver). Hors V1, à roadmaper.

---

## RGPD — Protection des données

### Principes appliqués

- **Minimisation** : ne collecter que ce qui sert à répondre à une demande de contact.
- **Souveraineté** : tout traitement reste en UE (OVH France, Plausible UE).
- **Consentement explicite** quand requis (formulaire contact), jamais pré-coché.
- **Transparence** : politique de confidentialité accessible depuis le footer.

### Cartographie des traitements

| Traitement | Données | Base légale | Durée | Sous-traitant |
|---|---|---|---|---|
| Formulaire contact | Nom, email, téléphone, profil, message | Consentement | 3 ans après dernier contact | OVH (mail) + Formspree/n8n |
| Analytics | Aucune donnée perso (Plausible sans cookie, pas d'IP stockée brute) | Intérêt légitime | 24 mois agrégés | Plausible (UE) |
| Logs serveur | IP, user-agent, URL | Intérêt légitime (sécurité) | 12 mois | OVH |
| Recrutement (CV reçus) | Identité, parcours | Consentement | 2 ans | OVH (mail) |

### Politique de confidentialité (page `/politique-confidentialite`)

Doit contenir :

1. Identité du responsable de traitement (FT2E).
2. Liste des traitements, des données, des bases légales, des durées.
3. Liste des sous-traitants.
4. Droits des personnes (accès, rectification, effacement, opposition, portabilité, limitation).
5. Coordonnées du DPO ou du responsable RGPD chez FT2E.
6. Procédure de recours auprès de la CNIL.

### Mentions légales (page `/mentions-legales`)

1. Éditeur : raison sociale FT2E, adresse, SIREN, capital, RCS.
2. Directeur de publication.
3. Hébergeur : OVHcloud, 2 rue Kellermann 59100 Roubaix.
4. Propriété intellectuelle : crédits photos, droits réservés.

### Cookies & traceurs

- **Plausible** : ne dépose pas de cookie, ne stocke pas d'IP individuelle → **pas de bandeau cookie obligatoire**.
- Si un traceur tiers est ajouté (réseaux sociaux, vidéo YouTube, etc.), bandeau cookie **obligatoire** via un outil conforme (par ex. Klaro!).

### Sécurité

- HTTPS forcé (Let's Encrypt via OVH).
- HSTS activé.
- Headers CSP, X-Frame-Options, X-Content-Type-Options.
- Sauvegardes OVH quotidiennes + sauvegarde Git par construction.
- Pas de base de données exposée (site statique = surface d'attaque minimale).

### Sous-traitance & responsabilité

- **EuporIA Factory** (Jean-François Caron) intervient en tant que prestataire technique sur le site et le système BET. Pas de traitement de données personnelles FT2E par EuporIA Factory en dehors du périmètre conventionné (cf. lettre d'engagement et de confidentialité).
- **Engagement de réversibilité** : à tout moment, FT2E peut récupérer l'ensemble des livrables. Données et code restent propriété FT2E.

---

## Checklist pré-publication

- [ ] Page `/accessibilite` publiée avec déclaration de conformité validée.
- [ ] Page `/politique-confidentialite` publiée avec cartographie complète.
- [ ] Page `/mentions-legales` publiée avec toutes les informations légales (SIREN, etc.).
- [ ] Formulaire de contact RGPD-compliant (consentement explicite, finalité claire).
- [ ] Audit RGAA AA livré, écarts documentés s'il y en a.
- [ ] HTTPS forcé, HSTS activé.
- [ ] CSP testée et validée (sans rupture de fonctionnalité).
