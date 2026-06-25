# Contrat de rendu

Un moteur de rendu transforme un prompt PDS en actif visuel. Le skill ne suppose aucun fournisseur précis.

## Entrée minimale

```json
{
  "slide_id": "slide-01",
  "prompt": "texte complet du prompt",
  "expected_ratio": "16:9",
  "language": "fr",
  "text_exact": ["Titre", "Label 1", "Callout"],
  "avoid": ["logo", "texte illisible", "paragraphe"]
}
```

## Sortie minimale

```json
{
  "slide_id": "slide-01",
  "status": "rendered",
  "renderer": "nom-du-moteur",
  "asset_ref": "assets/slide-01.png",
  "prompt_ref": "prompts/slide-01.txt",
  "ratio": "16:9",
  "inspection": "OK",
  "notes": "Texte lisible."
}
```

## États autorisés

- `ready` : prompt prêt, rendu non lancé.
- `rendered` : fichier ou URL exploitable produit.
- `failed` : moteur appelé mais échec explicite.
- `not_verified` : sortie visible, incomplète, absente ou non inspectée.

## Règles bloquantes

- Ne jamais utiliser `rendered` sans fichier, URL ou artefact exploitable.
- Ne jamais remplacer une image absente par une promesse.
- Marquer `not_verified` si le ratio, le texte, le chemin ou l'inspection manque.
- Conserver le prompt utilisé, même si le rendu échoue.
- Nommer le moteur de rendu, ou écrire `none`.

## Contrôles

Vérifier :

- existence de l'artefact ;
- ratio 16:9 ou écart nommé ;
- lisibilité du titre et des labels ;
- absence de texte parasite critique ;
- progression cohérente dans la série ;
- stabilité du masque commun ;
- cohérence entre scène et message.
