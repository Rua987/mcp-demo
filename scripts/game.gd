extends Node

const SAVE_PATH := "user://traverse_stats.cfg"
# Ancres CE : valeur live = base + compteur (scan exact unique, evite scan 0 global)
const CE_SCAN_COINS := 0xCE0DE000
const CE_SCAN_DEATHS := 0xCE0DE100

var current_era_index: int = 0
var coins: int = 0
var deaths: int = 0
var is_won: bool = false
var era_complete_pending: bool = false

var ce_scan_coins: int = CE_SCAN_COINS
var ce_scan_deaths: int = CE_SCAN_DEATHS

var has_run_record: bool = false
var last_deaths: int = 0
var last_time: float = 0.0
var best_deaths: int = 0
var best_time: float = 0.0

signal coins_changed(value: int)
signal deaths_changed(value: int)
signal era_changed
signal era_completed
signal game_won


func _ready() -> void:
	load_stats()
	_sync_ce_anchors()


func _sync_ce_anchors() -> void:
	ce_scan_coins = CE_SCAN_COINS + coins
	ce_scan_deaths = CE_SCAN_DEATHS + deaths


func _physics_process(_delta: float) -> void:
	# Permet a CE d'ecrire ce_scan_* ; le jeu resynchronise coins/deaths
	var from_ce_coins := ce_scan_coins - CE_SCAN_COINS
	if from_ce_coins != coins and from_ce_coins >= 0 and from_ce_coins <= 99:
		coins = from_ce_coins
		coins_changed.emit(coins)
		if coins >= get_total_coins() and not era_complete_pending and not is_won:
			era_complete_pending = true
			if is_final_era():
				is_won = true
				game_won.emit()
			else:
				era_completed.emit()
	var from_ce_deaths := ce_scan_deaths - CE_SCAN_DEATHS
	if from_ce_deaths != deaths and from_ce_deaths >= 0:
		deaths = from_ce_deaths
		deaths_changed.emit(deaths)


func start_run() -> void:
	current_era_index = 0
	coins = 0
	deaths = 0
	is_won = false
	era_complete_pending = false
	_sync_ce_anchors()
	coins_changed.emit(coins)
	deaths_changed.emit(deaths)
	era_changed.emit()


func get_current_era() -> Dictionary:
	return EraData.eras()[current_era_index]


func get_era_name() -> String:
	return get_current_era()["name"]


func get_collectible_name() -> String:
	return get_current_era()["collectible"]


func get_total_coins() -> int:
	return get_current_era()["total_coins"]


func is_final_era() -> bool:
	return current_era_index >= EraData.eras().size() - 1


func add_coin() -> void:
	if is_won or era_complete_pending:
		return
	coins += 1
	_sync_ce_anchors()
	coins_changed.emit(coins)
	if coins >= get_total_coins():
		era_complete_pending = true
		if is_final_era():
			is_won = true
			game_won.emit()
		else:
			era_completed.emit()


func register_death() -> void:
	if is_won:
		return
	deaths += 1
	_sync_ce_anchors()
	deaths_changed.emit(deaths)


func advance_era() -> void:
	if not era_complete_pending or is_won:
		return
	era_complete_pending = false
	coins = 0
	current_era_index += 1
	_sync_ce_anchors()
	coins_changed.emit(coins)
	era_changed.emit()


func save_run_result(run_deaths: int, run_time: float) -> void:
	has_run_record = true
	last_deaths = run_deaths
	last_time = run_time
	if not _has_best_record() or _is_better_run(run_deaths, run_time):
		best_deaths = run_deaths
		best_time = run_time
	_save_stats()


func load_stats() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(SAVE_PATH) != OK:
		return
	has_run_record = cfg.get_value("stats", "has_run_record", false)
	last_deaths = cfg.get_value("stats", "last_deaths", 0)
	last_time = cfg.get_value("stats", "last_time", 0.0)
	best_deaths = cfg.get_value("stats", "best_deaths", 0)
	best_time = cfg.get_value("stats", "best_time", 0.0)


func _save_stats() -> void:
	var cfg := ConfigFile.new()
	cfg.set_value("stats", "has_run_record", has_run_record)
	cfg.set_value("stats", "last_deaths", last_deaths)
	cfg.set_value("stats", "last_time", last_time)
	cfg.set_value("stats", "best_deaths", best_deaths)
	cfg.set_value("stats", "best_time", best_time)
	cfg.save(SAVE_PATH)


func _has_best_record() -> bool:
	return has_run_record and best_time > 0.0


func _is_better_run(run_deaths: int, run_time: float) -> bool:
	if not _has_best_record():
		return true
	if run_deaths != best_deaths:
		return run_deaths < best_deaths
	return run_time < best_time
