# Postmortem ShipGuard 2.3.6 - bootstrap MacBook Pro

Date : 2026-06-30

Contexte : retour d'installation ShipGuard sur un MacBook Pro distinct du
harness principal. Objectif : comparer les frictions observees avec les
postmortems deja envoyes, isoler ce qui est nouveau, et tracer les preuves
locales disponibles.

## Verdict court

Une partie du retour est deja couverte par les postmortems `2.3.5` / `2.3.6` :

- migration depuis l'ancien adaptateur Codex local ;
- difference entre plugin officiel `shipguard@shipguard` et ancien
  `shipguard-codex@personal` ;
- besoin d'une doc d'installation Codex claire ;
- confusion possible entre runtimes Claude et Codex ;
- distinction entre `agent-browser` disponible et dependances runtime reelles.

Nouveaux points a remonter / garder pour Loic :

1. Le hook `SessionStart` qui echoue en `code 127` semble relever du harnais
   local, mais il pollue le bootstrap ShipGuard.
2. Le check de harnais local est trop multi-runtime : il peut FAIL sur Claude
   absent meme si l'usage vise uniquement Codex.
3. Le contrat local garde des chemins tres stricts et versionnes en `2.3.0`.
4. Le bootstrap Codex par adaptateur local reste manuel sur une machine neuve,
   alors que le plugin officiel Codex existe maintenant.
5. Le check devrait produire un verdict runtime-aware : `Codex OK`, `Claude
   absent/non verifie WARN`, et non un echec global si le runtime cible est OK.
6. Le script de check a aussi une dependance Python `PyYAML` non documentee
   dans le retour initial ; sans elle, il echoue avant les checks ShipGuard.

## Ce qui etait deja dans les postmortems

### Deja couvert - ancien adaptateur Codex

Les postmortems `2.3.5` documentent deja :

```text
shipguard-codex@personal  installed, enabled  <ancienne version>
shipguard@shipguard       installed, enabled  <version officielle>
```

et la migration :

```bash
codex plugin remove shipguard-codex@personal
codex plugin add shipguard@shipguard
```

Le retour MacBook Pro ajoute toutefois un angle nouveau : sur une machine
neuve, le chemin par adaptateur peut encore etre percu comme le chemin normal,
car le check local attend `shipguard-codex@personal`.

### Deja couvert - Playwright / agent-browser

Le postmortem `2.3.6` contient deja l'addendum :

- une commande Playwright globale/Python ne suffit pas ;
- `sg-record.mjs` exige le package Node `playwright` importable ;
- `agent-browser` disponible ne prouve pas que `sg-record` peut tourner.

Le retour MacBook Pro confirme le meme type de probleme : les prerequis CLI
peuvent etre OK sans que le plugin/adaptateur ShipGuard soit operationnel.

## Points nouveaux traces

### B7 - `SessionStart hook` echoue en `code 127`

Severite : moyenne, surtout bootstrap / DX.

Retour MacBook Pro :

```text
SessionStart hook (failed) error: hook exited with code 127
```

Trace locale :

Le hook SessionStart du harnais Codex local est configure dans :

```text
/Users/alex/Claude/.codex/hooks.json
```

Commandes executees :

```json
{
  "type": "command",
  "command": "bash /Users/alex/Claude/scripts/session-start-todo.sh"
}
```

```json
{
  "type": "command",
  "command": "uv run --directory /Users/alex/Claude/wiki python hooks/session-start.py",
  "timeout": 15
}
```

Interpretation :

`127` est typiquement un exit shell "command not found". Sur une machine neuve,
les causes probables sont :

- `uv` absent du PATH ;
- chemin `/Users/alex/Claude/wiki` absent ;
- script de hook non present ou non executable ;
- PATH du runtime hook different du shell interactif.

Preuve locale :

Sur la machine principale, les commandes existent :

```text
uv            -> /Users/alex/.local/bin/uv
agent-browser -> /opt/homebrew/bin/agent-browser
node          -> /opt/homebrew/bin/node
git           -> /usr/bin/git
claude        -> /Users/alex/.local/bin/claude
codex         -> /Users/alex/.local/bin/codex
```

Conclusion :

Ce n'est probablement pas un bug du plugin ShipGuard amont, mais un probleme de
bootstrap du harnais. Il merite d'etre documente separement pour eviter de
confondre "hook de session casse" et "ShipGuard casse".

Proposition :

- rendre le hook SessionStart tolerant : si `uv` ou le dossier wiki manque,
  afficher WARN et sortir `0` ;
- ou documenter les prerequis du harnais avant d'activer le hook ;
- inclure la commande exacte echouee dans le message d'erreur.

Critere d'acceptation :

```text
SessionStart hook: WARN uv absent / wiki absent, bootstrap continue
```

### B8 - Check de harnais non runtime-aware

Severite : haute pour installation multi-machines.

Retour MacBook Pro :

Le check confirme que les prerequis CLI sont OK :

```text
node OK
agent-browser OK
git OK
```

mais le plugin/adaptateur lui-meme manque. Cote Claude, l'absence de Claude
Code ou d'installation Claude est traitee comme un echec, meme si l'usage vise
Codex.

Trace locale :

Le script :

```text
/Users/alex/Claude/scripts/check-shipguard-harness-fit.sh
```

charge toujours l'entree Claude :

```python
claude_entry = load_claude_entry(plugin_id)
```

`load_claude_entry()` fait `FAIL` si le registre est absent :

```text
~/.claude/plugins/installed_plugins.json
```

ou si le plugin Claude n'est pas installe.

Ensuite le script verifie aussi, sans mode optionnel :

```text
Claude: cache installe
Claude: plugin marketplace
Claude: manifeste natif
```

Impact :

- une installation Codex saine peut etre marquee KO parce que Claude est absent ;
- la validation `claude plugin validate --strict` est melangee avec le verdict
  Codex ;
- le check ne dit pas clairement "runtime non installe / non verifie".

Proposition :

- ajouter un argument de runtime cible :

```bash
check-shipguard-harness-fit.sh --runtime=codex
check-shipguard-harness-fit.sh --runtime=claude
check-shipguard-harness-fit.sh --runtime=all
```

- transformer les runtimes non demandes en WARN ;
- FAIL seulement si le runtime demande est cense etre operationnel mais casse.

Critere d'acceptation :

```text
Codex: OK
Claude: WARN non installe / non verifie
Verdict global: OK pour runtime cible codex
```

### B9 - Contrat local avec chemins stricts et versionnes `2.3.0`

Severite : moyenne.

Trace locale :

Le contrat :

```text
/Users/alex/Claude/config/plugin-harness-contracts/shipguard.yaml
```

contient des chemins stricts :

```yaml
claude:
  registry: "~/.claude/plugins/installed_plugins.json"
  marketplace_clone: "~/.claude/plugins/marketplaces/shipguard"
  plugin_root: "~/.claude/plugins/marketplaces/shipguard/plugins/shipguard"
  cache_root: "~/.claude/plugins/cache/shipguard/shipguard/2.3.0"

codex:
  adapter_plugin_id: "shipguard-codex@personal"
  adapter_root: "~/plugins/shipguard-codex"
  marketplace_clone: "~/.codex/.tmp/marketplaces/shipguard"
  plugin_root: "~/.codex/.tmp/marketplaces/shipguard/plugins/shipguard"
  cache_root: "~/.codex/plugins/cache/shipguard/shipguard/2.3.0"
```

Or la version testee et installee est `2.3.6`, et le plugin officiel Codex
est maintenant :

```text
shipguard@shipguard
```

Impact :

- le check peut pointer vers un cache ancien ou absent ;
- une machine propre peut echouer parce qu'elle n'a pas exactement les chemins
  historiques ;
- l'ancien adaptateur personnel reste encode comme cible Codex.

Proposition :

- remplacer les chemins de cache versionnes par une detection de version
  installee ;
- accepter `shipguard@shipguard` comme runtime Codex principal ;
- garder `shipguard-codex@personal` seulement comme legacy/migration.

Critere d'acceptation :

```text
Le check detecte la version installee via codex plugin list / claude plugin list
et ne depend pas d'un chemin cache 2.3.0.
```

### B10 - Bootstrap Codex clean encore trop manuel si le check attend l'adaptateur local

Severite : moyenne.

Retour MacBook Pro :

Le chemin de resolution a ete :

1. clone marketplace ShipGuard ;
2. pushurl neutralise ;
3. generation de l'adaptateur Codex via `sync-shipguard-codex-adapter.sh` ;
4. marketplace personal ;
5. `codex plugin add`.

Trace locale :

Le script d'adaptateur existe ici :

```text
/Users/alex/Claude/scripts/sync-shipguard-codex-adapter.sh
```

Il genere :

```text
~/plugins/shipguard-codex
~/.agents/plugins/marketplace.json
shipguard-codex@personal
```

Mais la doc amont ShipGuard `2.3.6` donne maintenant le chemin officiel :

```bash
codex plugin marketplace add bacoco/shipguard
codex plugin add shipguard@shipguard
```

Impact :

- le harnais local et la doc amont ne racontent pas le meme chemin ;
- une nouvelle machine peut reconstruire l'ancien adaptateur alors que le
  plugin officiel existe ;
- le check peut pousser l'utilisateur vers un chemin legacy.

Proposition :

- documenter un "Codex clean install" officiel et unique ;
- reserver `sync-shipguard-codex-adapter.sh` au legacy ;
- dans le check, preferer `shipguard@shipguard` et avertir si
  `shipguard-codex@personal` est encore utilise.

Critere d'acceptation :

```text
Sur une machine neuve Codex-only :
codex plugin marketplace add bacoco/shipguard
codex plugin add shipguard@shipguard
check --runtime=codex -> OK
```

### B11 - `claude plugin validate --strict` doit etre non bloquant si Claude CLI absent

Severite : moyenne.

Trace locale :

Le script gere deja partiellement ce cas :

```python
cli = shutil.which("claude")
if not cli:
    warn("Claude CLI absent: validation stricte non exécutée")
    return
```

Mais les checks precedents peuvent deja FAIL sur :

- registre Claude absent ;
- plugin Claude absent ;
- cache Claude absent ;
- marketplace Claude absent.

Proposition :

- deplacer toute la section Claude derriere un runtime target ;
- si runtime cible = Codex, transformer toute absence Claude en WARN ;
- si runtime cible = Claude, garder FAIL.

Critere d'acceptation :

```text
Claude: WARN CLI absent, validation stricte non verifiee
Codex: OK
Verdict global: OK pour runtime cible codex
```

### B12 - Dependances du check de harnais : `PyYAML`

Severite : basse a moyenne pour bootstrap.

Trace locale :

En lancant :

```bash
/Users/alex/Claude/scripts/check-shipguard-harness-fit.sh /Users/alex/Claude
```

le script echoue avant les checks ShipGuard :

```text
[FAIL] PyYAML indisponible: No module named 'yaml'
```

Impact :

- le check ne peut pas diagnostiquer ShipGuard si la dependance Python manque ;
- sur une machine neuve, le premier message peut etre une dependance du
  harnais, pas un probleme plugin.

Proposition :

- documenter `PyYAML` dans les prerequis du check ;
- ou remplacer la lecture YAML par une dependance vendoree / parser minimal ;
- ou afficher une commande d'installation claire.

Critere d'acceptation :

```text
PyYAML missing: install with python3 -m pip install --user PyYAML
```

## Synthese a envoyer a Loic

Message court :

```text
Retour bootstrap MacBook Pro : les prerequis CLI node/agent-browser/git peuvent
etre OK alors que le verdict ShipGuard reste KO parce que le check melange les
runtimes et attend encore des chemins/adaptateurs historiques. Le check devrait
etre runtime-aware : OK Codex si shipguard@shipguard ou l'adaptateur cible est
sain, WARN Claude absent/non verifie, FAIL seulement pour le runtime demande.
Le chemin Codex clean devrait etre une commande/doc unique ; l'ancien
sync-shipguard-codex-adapter.sh devrait etre clairement legacy. Separément, le
SessionStart hook code 127 semble venir du harnais local (uv/chemin manquant)
et devrait WARN sans bloquer le bootstrap ShipGuard.
```

## Statut par rapport aux postmortems existants

| Point MacBook Pro | Deja couvert ? | Action |
|---|---:|---|
| Ancien adaptateur Codex / migration | Partiel | deja dans 2.3.5, completer avec bootstrap clean |
| Plugin/adaptateur manquant mal distingue des CLI OK | Non | nouveau B8/B10 |
| Runtime Claude absent bloque un usage Codex | Non | nouveau B8/B11 |
| Chemins Claude stricts et cache `2.3.0` | Non | nouveau B9 |
| `claude plugin validate --strict` sans Claude CLI | Partiel dans script, pas dans RETEX | nouveau B11 |
| `SessionStart hook code 127` | Non | nouveau B7 |
| `PyYAML` manquant pour le check | Non | nouveau B12 |
