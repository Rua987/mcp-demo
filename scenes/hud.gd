extends CanvasLayer

# In-game HUD only — attach to Main.tscn node "HUD", not TitleScreen.

@onready var score_label: Label = $ScoreLabel
@onready var stats_label: Label = $StatsLabel
@onready var victory_label: Label = $VictoryLabel
@onready var pause_label: Label = $PauseLabel

var _elapsed := 0.0
var _paused := false


func _ready() -> void:
	if not is_instance_valid(score_label):
		push_error(
			"hud.gd expects Main.tscn HUD children (ScoreLabel, StatsLabel, ...). "
			+ "Use title_screen.gd on TitleScreen.tscn."
		)
		return
	process_mode = Node.PROCESS_MODE_ALWAYS
	Game.coins_changed.connect(_update_score)
	Game.deaths_changed.connect(_update_deaths)
	Game.era_changed.connect(_update_era)
	Game.era_completed.connect(_on_era_completed)
	Game.game_won.connect(_on_game_won)
	_elapsed = 0.0
	_update_era()
	_update_score(Game.coins)
	_update_deaths(Game.deaths)
	victory_label.visible = false
	pause_label.visible = false


func _process(delta: float) -> void:
	if not Game.is_won and not Game.era_complete_pending and not _paused:
		_elapsed += delta
	_update_stats_line()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") and not Game.is_won and not Game.era_complete_pending:
		_toggle_pause()
		return
	if _paused:
		return
	if not event.is_action_pressed("ui_accept"):
		return
	if Game.era_complete_pending and not Game.is_won:
		victory_label.visible = false
		Game.advance_era()
	elif Game.is_won:
		get_tree().change_scene_to_file("res://scenes/TitleScreen.tscn")


func _toggle_pause() -> void:
	_paused = not _paused
	get_tree().paused = _paused
	pause_label.visible = _paused


func _update_era() -> void:
	_update_score(Game.coins)


func _update_score(_value: int) -> void:
	score_label.text = "Ere: %s  |  %s: %d / %d" % [
		Game.get_era_name(),
		Game.get_collectible_name(),
		Game.coins,
		Game.get_total_coins(),
	]


func _update_deaths(_value: int) -> void:
	_update_stats_line()


func _update_stats_line() -> void:
	stats_label.text = "Morts: %d  |  Temps: %.1fs  |  CE coins=0x%08X" % [
		Game.deaths,
		_elapsed,
		Game.ce_scan_coins,
	]


func _on_era_completed() -> void:
	var next_era: Dictionary = EraData.eras()[Game.current_era_index + 1]
	victory_label.text = "%s terminee!\nEntree -> %s" % [
		Game.get_era_name(),
		next_era["name"],
	]
	victory_label.visible = true


func _on_game_won() -> void:
	Game.save_run_result(Game.deaths, _elapsed)
	victory_label.text = (
		"Histoire completee!\n4 eres parcourues\n%d morts en %.1fs\nEntree -> menu"
		% [Game.deaths, _elapsed]
	)
	victory_label.visible = true
