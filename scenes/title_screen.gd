extends Control

@onready var _title: Label = $VBox/TitleLabel
@onready var _subtitle: Label = $VBox/SubtitleLabel
@onready var _eras: Label = $VBox/ErasLabel
@onready var _stats: Label = $VBox/StatsLabel
@onready var _hint: Label = $VBox/HintLabel


func _ready() -> void:
	if not is_instance_valid(_title):
		push_error("title_screen.gd belongs on TitleScreen.tscn (VBox/TitleLabel), not on HUD.")
		return
	Game.load_stats()
	_title.text = "Traversee du Temps"
	_subtitle.text = "Platformer a travers 4 eres de l'histoire"
	_eras.text = "Prehistoire  >  Antiquite  >  Moyen Age  >  Industrie"
	_refresh_stats()
	_hint.text = "Entree / Espace - Jouer    |    Echap - Quitter"


func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_tree().quit()
		return
	if event.is_action_pressed("ui_accept") or event.is_action_pressed("jump"):
		_start_game()


func _refresh_stats() -> void:
	if not Game.has_run_record:
		_stats.text = "Aucune partie terminee - bat ton record!"
		return
	_stats.text = "Derniere: %d morts, %.1fs  |  Record: %d morts, %.1fs" % [
		Game.last_deaths,
		Game.last_time,
		Game.best_deaths,
		Game.best_time,
	]


func _start_game() -> void:
	Game.start_run()
	get_tree().change_scene_to_file("res://scenes/Main.tscn")
