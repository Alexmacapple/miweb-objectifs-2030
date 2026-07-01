# Proposal Trace - Recette ShipGuard sur MiWeb Objectifs 2030

Status: prepared
Generated at: 2026-06-30T23:18:35.273Z
Référence: SHIPGUARD-MIWEB-2026-06-29
Client: Équipe MiWeb
Client contact: validation-locale@example.invalid
Route / flow: /
Review target: http://localhost:8888/persona-reports/shipguard-recette-miweb/client.html

This file records what ShipGuard prepared for client validation. It is the local trace of the proposal before any manual email is sent.

# Proposed Changes

## Suite visuelle complète générée et exécutée

- Change ID: visual-suite
- Summary: n/a
- Problem: Le dépôt n'avait pas encore d'artefacts ShipGuard explicites pour distinguer le test visuel du contrôle accessibilité.
- Proposed decision: Créer une suite locale ShipGuard avec 28 routes, captures, rapport et planche-contact.
- Expected impact: Le site peut être revu dans une interface unique avec preuves visuelles et statuts PASS.
- Choices:
- n/a
- Residual risk: Le runner local reste un adaptateur de recette et doit être durci avant réutilisation durable.
- Tests / routes:
- pages/root-index
- pages/*
- Files:
- visual-tests/_shipguard_static_run.py
- visual-tests/_results/report.md

## Audit code report-only affiché dans Mission Control

- Change ID: code-audit
- Summary: n/a
- Problem: L'onglet Code Audit était vide tant que audit-results.json n'existait pas.
- Proposed decision: Agréger 5 zones d'audit quick report-only au format ShipGuard.
- Expected impact: L'interface affiche 19 constats, 4 high, 11 medium, 4 low, et 8 routes impactées.
- Choices:
- n/a
- Residual risk: Les constats sont non corrigés et certains restent à confirmer par tests ciblés.
- Tests / routes:
- sg-code-audit quick --report-only
- Files:
- visual-tests/_results/audit-results.json
- visual-tests/_results/audit-results.toon

## Accueil MiWeb disponible comme route de référence

- Change ID: home-page
- Summary: n/a
- Problem: Le workflow avait besoin d'une route simple pour vérifier le serveur local et les manifests enregistrés.
- Proposed decision: Utiliser l'accueil racine comme route smoke test.
- Expected impact: Le manifest enregistré peut rejouer une ouverture et une assertion textuelle sur Objectifs 2030.
- Choices:
- n/a
- Residual risk: Le recorder interactif complet n'a pas été lancé jusqu'au clic Stop humain.
- Tests / routes:
- recorded-miweb-home-smoke
- Files:
- visual-tests/manifests/recorded-miweb-home-smoke.yaml


# Generated Artifacts

- audience_index: index.html
- audience_html (client): client.html
- audience_html (product): product.html
- audience_html (design): design.html
- audience_html (engineering): engineering.html
- email_to_send: client-invite-email.md
- client_reply_email: client-response-email.md
- proposal_trace_markdown: proposal-trace.md
- proposal_trace_json: proposal-trace.json

# Client Return

The client can return validation manually by sending back `client-response-email.md`, or by exporting JSON from the HTML report.
