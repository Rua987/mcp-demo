# MCP Live Campaign — mcp-demo (2026-07-07)

Style T3MP3ST : recon → exécution → preuves reproductibles.

## Cible

- Projet : `C:/Users/admin/Documents/GodotProjects/mcp-demo/`
- Godot : 4.6.1.stable, plugin MCP connecté (Agents 2)

## Phase 1 — Recon

| Step | Outil | Résultat |
|------|-------|----------|
| Status | `get_godot_status` | `connected: true`, mode `live` |
| Scripts | `validate_script` hud.gd / game.gd | parse OK (autoload — non instanciable en éditeur, normal) |
| Erreurs | `get_errors` | **0 error(s)** |

## Phase 2 — Exécution live

| Step | Outil | Résultat |
|------|-------|----------|
| Lancer jeu | `run_scene` Main.tscn | `started: true`, runtime_root `/root/Main` |
| Probe HUD | `query_runtime_node` `/root/Main/HUD/StatsLabel` | `text` contient `CE coins=0xCE0DE000` |
| Probe Game | `query_runtime_node` `/root/Game` | `ce_scan_coins=3457015808`, `coins=0`, `deaths=0` |
| Screenshot | `take_screenshot` | `screenshot_37666.png` — HUD visible en jeu |
| Stop | `stop_scene` | OK |

## Phase 3 — Cross-check Python (ground truth)

| Source | Valeur | Attendu |
|--------|--------|---------|
| Godot `ce_scan_coins` | `3457015808` | `0xCE0DE000` |
| Godot HUD | `CE coins=0xCE0DE000` | base + 0 coins |
| Python `ce_cli --coins 0` | `0xCE0DE000` | **match** |
| `verify_ce_anchors.py` | SUCCES | ancres game.gd |
| `ce_workflow.py` | PASS | chaîne complète |

## Verdict

**HOLDS** — Python mirror, fichiers Godot, runtime live et HUD affichent la même ancre CE.

`match=False` au démarrage (coins=0, expected=3 pour ère 0) est **correct** : le joueur n'a pas encore collecté les 3 os.

## Campagne coin +1 (2026-07-07)

| Step | Preuve |
|------|--------|
| Input | `send_input` jump → collision coin (0, 95) |
| Game.coins | **0 → 1** |
| Game.ce_scan_coins | **0xCE0DE000 → 0xCE0DE001** (3457015809) |
| HUD ScoreLabel | `Os: 1 / 3` |
| HUD StatsLabel | `CE coins=0xCE0DE001` |
| Python ce_cli | `coins=1 … 0xCE0DE001` — **hex match** |
| Screenshot | `campaign_coin1.png` |

`match=False` avec `--era 0 --coins 1` est correct (expected=3 pour fin d'ère, pas 1).

## Campagne CE write → jeu (2026-07-07)

| Step | Preuve |
|------|--------|
| Prérequis | Pipe `CE_MCP_Bridge_v99` + Godot MCP connecté |
| Outil | `ce_godot_coins_write.py --target 2` |
| CE write | `0xCE0DE000` → `0xCE0DE002` @ PID 9476 |
| Game.coins | **0 → 2** (via `_physics_process` sync) |
| HUD | `Os: 2 / 3`, `CE coins=0xCE0DE002` |
| Python ce_cli | aligné sur runtime |
| JSON | `"ok": true` |

**Sens inverse prouvé :** CE écrit en mémoire → Godot lit → HUD + oracle MCP confirment.

## Campagne P0 — transition ère 0 → Antiquité (2026-07-07)

| Step | Avant | Après |
|------|-------|-------|
| Input | `era_complete_pending=true`, coins=2 | `send_input` ui_accept (Entrée) |
| `current_era_index` | 0 | **1** |
| `coins` | 2 | **0** (reset par `advance_era()`) |
| `ce_scan_coins` | `0xCE0DE002` | **`0xCE0DE000`** |
| HUD ScoreLabel | Prehistoire Os 2/3 | **Antiquite Artefacts 0/4** |
| VictoryLabel | visible | **hidden** |
| Screenshot | — | `campaign_era1_antiquite.png` |

**Note :** `ce_godot_coins_write.py` appelle `stop_scene` + `run_scene` → remet l'ère à 0. Pour tester CE write **sans** reset, attacher CE manuellement pendant le jeu sans relancer le script de prep.

CE write post-transition (script prep) : coins=4, `0xCE0DE004`, ok=true — mais scène repartie en Préhistoire (effet secondaire du harness, pas du jeu).

## Rejouer

```powershell
# Terminal 1 : Godot ouvert sur mcp-demo (plugin MCP vert)
# Terminal 2 :
cd C:\Users\admin\Documents\GodotProjects\mcp-demo
python scripts/ce_workflow.py
# Puis via MCP : run_scene → query_runtime_node → take_screenshot → stop_scene
```
