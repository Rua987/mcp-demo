# mcp-demo

Platformer Godot **4.6** (« Traversée du Temps », 4 ères) branché au **plugin MCP Godot** et à **Cheat Engine** via ancres mémoire fixes.

Démo reproductible : Python mirror ↔ runtime Godot ↔ écriture CE, avec receipts JSON (style T3MP3ST).

## Prérequis

| Outil | Version / détail |
|-------|------------------|
| Godot | 4.6.x — ouvrir ce dossier, plugin `addons/godot_mcp` activé |
| MCP Cursor | `~/.cursor/mcp.json` avec serveurs `godot` + `cheatengine` |
| Cheat Engine | Pipe `\\.\pipe\CE_MCP_Bridge_v99` (bridge Lua MCP) |
| Python | 3.11+ — `pytest` pour les tests offline |

## Démarrage rapide

```powershell
# 1. Godot : ouvrir le projet, Agents MCP verts, F5 (Main en play)
# 2. Chaîne Python (offline, sans CE) :
python scripts/ce_workflow.py

# 3. Démo live CE × Godot (receipt JSON) :
.\scripts\ce_live_demo.ps1 -SkipPytest
```

Receipt : `reports/ce_live_demo.json`  
Journal campagne : `reports/mcp_live_campaign.md`

## Ancres CE (ground truth)

| Variable | Hex | Formule |
|----------|-----|---------|
| `CE_SCAN_COINS` | `0xCE0DE000` | `ce_scan_coins = base + coins` |
| `CE_SCAN_DEATHS` | `0xCE0DE100` | `ce_scan_deaths = base + deaths` |

Vérification fichiers Godot : `python scripts/verify_ce_anchors.py`

## Scripts principaux

| Script | Rôle |
|--------|------|
| `scripts/ce_workflow.py` | Pre-flight : ancres + pytest + snapshot |
| `scripts/ce_cli.py` | Snapshot hex coins/deaths/ère |
| `scripts/ce_live_demo.py` | Orchestrateur live + receipt JSON |
| `scripts/ce_write_coins.py` | Lance `ce_godot_coins_write.py` (LINUS) |

Écriture CE **sans reset d'ère** : `--skip-prepare --no-reset` (voir LINUS `linus_nanochat/scripts/ce_godot_coins_write.py`).

## Tests

```powershell
python -m pytest scripts/ -q
```

35 tests offline (chaîne Python + démo sans live CE).

## Liens

- Écriture CE live (LINUS red-team) : [Rua987/temple-iam-simple](https://github.com/Rua987/temple-iam-simple) branche `linus-v4-redteam`
