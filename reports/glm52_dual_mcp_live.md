# GLM 5.2 Dual MCP Live — P1 bis (succès via script recipe)

Date : session P1 bis  
Méthode : `scripts/ce_write_coins.py` → `ce_godot_coins_write.py` (recipe `e2e_redteam20`)

## Résultat

| Champ | Valeur |
|-------|--------|
| **ok** | **true** |
| game_pid | 1976 (subprocess play) |
| pids Godot | [1976, 12116] |
| addr CE | `0x1E7D768EE30` |
| coins_before | 0 |
| coins_after | **3** |
| ce_scan_before | 3457015808 (`0xCE0DE000`) |
| ce_scan_after | 3457015811 (`0xCE0DE003`) |
| write_val_hex | `0xce0de003` |

## Agent GLM 5.2

- Recette A directe : **timeout 30s** (bash LINUS) → échec
- Contournement agent : `Start-Job` + lecture `tmp_ce_out.json` → **JSON ok=true**
- Rapport : écrit manuellement (write_file simulé en texte par GLM)

## Leçon

Pour agent dual MCP CE×Godot : utiliser le **launcher local** `scripts/ce_write_coins.py`  
ou augmenter `timeout` bash à **120s** ; les noms d'outils CE exacts sont  
`persistent_scan_first_scan`, pas `persistent_scan`.
