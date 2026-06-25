# Albert OSS-120

Albert OSS-120 doit être traité comme un moteur texte tant qu'aucune documentation officielle ne prouve une capacité de génération d'image.

## Rôle adapté

Albert peut aider à :

- résumer une source longue ;
- extraire une colonne vertébrale PDS ;
- rédiger des fiches PDS ;
- produire des prompts de rendu ;
- contrôler les critères textuels ;
- reformuler pour un public non spécialiste.

## Rôle interdit sans preuve

Albert ne doit pas être présenté comme capable de :

- générer des PNG ;
- inspecter réellement une image locale ;
- garantir un ratio visuel ;
- confirmer la lisibilité d'une image non ouverte ;
- remplacer un moteur de rendu.

## Formulation sûre

Dire :

```text
Albert peut préparer le storyboard et les prompts. Le rendu image dépend d'un adaptateur séparé.
```

Ne pas dire :

```text
Albert génère les slides image.
```

## Vérification avant intégration réelle

Avant de brancher Albert :

- lire la documentation officielle actuelle ;
- confirmer le nom exact du modèle ;
- confirmer endpoint, authentification, quotas et limites ;
- tester un appel minimal ;
- journaliser les erreurs ;
- conserver un fallback sans Albert.
