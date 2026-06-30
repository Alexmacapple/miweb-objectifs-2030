# sg-improve preview - ShipGuard 2.3.4

Mode : `--dry-run`
Date : 2026-06-29

## Résumé

Ce preview montre ce que `sg-improve` écrirait sans modifier `.shipguard/`,
sans créer de snapshot, sans appeler GitHub et sans toucher au code source.

Sources lues :

- `visual-tests/_results/audit-results.json`
- `visual-tests/_results/visual-results.json`
- `visual-tests/_results/fix-manifest.json`
- `visual-tests/_results/shipguard-postmortem-loic-2.3.4.md`
- `visual-tests/_results/visual-fix-plan.md`

## Données structurées

- Audit : `quick`, 1 round, 5 agents legacy, 125 fichiers audités.
- Bugs : 19 total, 0 critical, 4 high, 11 medium, 4 low.
- Routes impactées : 8.
- Backend impacté : 5.
- Visual run : 28 tests, 28 pass, 0 fail, 0 stale.
- Annotation UI : 1 annotation exportée dans `fix-manifest.json`.

## Fichiers cibles qui seraient écrits en mode réel

- `.shipguard/history/<timestamp>/meta.yaml`
- `.shipguard/learnings.yaml`
- `.shipguard/mistakes.md`
- GitHub issue ou commentaire dans `bacoco/ShipGuard`

## YAML qui serait proposé pour `.shipguard/learnings.yaml`

```yaml
schema_version: 2
last_updated: "2026-06-29T17:11:26Z"

success_patterns:
  - pattern: "visual-results.json canonical contract"
    note: "Dashboard 2.3.4 rendered 28 pass, 0 stale from canonical JSON."
    first_seen: "2026-06-29"
    occurrences: 1
  - pattern: "review and monitor smoke tests"
    note: "Both official smoke tests pass outside sandbox and catch dashboard/monitor regressions."
    first_seen: "2026-06-29"
    occurrences: 1

noise_filters:
  - pattern: "legacy audit findings about pre-2.3.4 dashboard code"
    action: "mark_stale_after_plugin_upgrade"
    reason: "audit-results.json was produced before 2.3.4 and still references fixed dashboard issues."

session_history:
  - date: "2026-06-29"
    mode: "quick"
    files: 125
    bugs_found: 19
    bugs_fixed: 0
    critical: 0
    high: 4
    visual_pass: 28
    visual_fail: 0
    notes: "Plugin 2.3.4 tested; no source fixes applied."
```

## Sections qui seraient proposées pour `.shipguard/mistakes.md`

```markdown
# Erreurs à ne pas répéter

## JavaScript / Node

### Ne pas masquer stderr des serveurs enfants dans les smoke tests

Bad pattern:
\```js
const server = spawn(process.execPath, ["build-review.mjs", "--serve"], {
  stdio: ["ignore", "pipe", "pipe"]
});
throw new Error("review server did not become ready");
\```

Good pattern:
\```js
const stderr = [];
server.stderr.on("data", chunk => stderr.push(String(chunk)));
throw new Error(`review server did not become ready\n${stderr.slice(-20).join("")}`);
\```

Contexte : les smoke tests 2.3.4 échouaient en sandbox avec un message de
readiness générique alors que la vraie cause était `listen EPERM`.

### Ne pas afficher un badge Agents sans état vide explicite

Bad pattern:
\```js
if (typeof data.agents === "number") return data.agents;
// panel can still be empty if no agents[] and IDs do not match fallback regex
\```

Good pattern:
\```js
if (typeof data.agents === "number" && getAuditAgents(data).length === 0) {
  renderLegacyAgentsHint(data.agents);
}
\```

Contexte : un audit legacy avec `agents: 5` et IDs `SG-Z*` affiche un badge
Agents 5 mais un panneau vide.
```

## GitHub issue/comment preview

Titre proposé :

```text
Improve 2.3.4 upgrade and smoke-test diagnostics from Codex/Claude recipe
```

Corps proposé :

```markdown
## Session Insights - miweb-objectifs-2030 (2026-06-29)

### Improvements

1. Document migration from `shipguard-codex@personal` to official
   `shipguard@shipguard`.
2. Show the marketplace source path when Claude/Codex decide a plugin is
   already at latest.
3. Surface child-process stderr in `review-smoke-test.mjs` and
   `monitor-smoke-test.mjs`, especially `listen EPERM`.
4. Add `--port`, `--keep-tmp`, and `--debug` to smoke tests.
5. Add a legacy agents hint when `agents` is numeric but no cards can be
   rendered.
6. Protect dashboard brand, commands, statuses, and technical labels from
   Chrome auto-translation.
7. Serve or suppress `favicon.ico` to avoid noisy console errors.

### What worked well

- `visual-results.json` prevented stale visual status.
- Review and monitor smoke tests pass once local bind is authorized.
- `POST /save-manifest` produced a valid annotated `fix-manifest.json`.
- `sg-visual-fix --dry-run` produced a non-destructive plan.
```

## Signaux ignorés et pourquoi

- Bugs applicatifs MiWeb : ignorés pour ce preview générique, car la demande est
  d'améliorer ShipGuard, pas le harnais.
- Auto-traduction Chrome : gardée comme signal générique, mais pas classée comme
  bug ShipGuard pur.
- Ancien audit `agents: 5` : gardé comme signal de compatibilité legacy.

## Rollback snapshot qui serait créé en mode réel

```text
.shipguard/history/20260629-191126/
```

Dry-run terminé : aucune écriture `.shipguard/`, aucune issue GitHub, aucun
fichier source modifié.
