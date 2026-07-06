extends Node2D

const PLATFORM_SCENE := preload("res://scenes/Platform.tscn")
const MOVING_PLATFORM_SCENE := preload("res://scenes/MovingPlatform.tscn")
const COIN_SCENE := preload("res://scenes/Coin.tscn")
const SPIKE_SCENE := preload("res://scenes/Spike.tscn")

@onready var _background: ColorRect = $Background
@onready var _ground_visual: ColorRect = $Ground/GroundVisual
@onready var _platforms: Node2D = $Platforms
@onready var _coins: Node2D = $Coins
@onready var _hazards: Node2D = $Hazards
@onready var _player: CharacterBody2D = $Player2D


func _ready() -> void:
	Game.start_run()
	Game.era_changed.connect(_build_level)
	_build_level()


func _build_level() -> void:
	var era: Dictionary = Game.get_current_era()
	_clear_children(_platforms)
	_clear_children(_coins)
	_clear_children(_hazards)

	_background.color = era["background"]
	_ground_visual.color = era["ground"]

	for pos in era["platforms"]:
		var platform := PLATFORM_SCENE.instantiate()
		platform.position = pos
		_platforms.add_child(platform)

	for pos in era["moving_platforms"]:
		var moving := MOVING_PLATFORM_SCENE.instantiate()
		moving.position = pos
		_platforms.add_child(moving)

	for pos in era["coins"]:
		var coin := COIN_SCENE.instantiate()
		coin.position = pos
		_coins.add_child(coin)

	for pos in era["spikes"]:
		var spike := SPIKE_SCENE.instantiate()
		spike.position = pos
		_hazards.add_child(spike)

	if _player.has_method("set_spawn"):
		_player.set_spawn(era["player_spawn"])


func _clear_children(node: Node) -> void:
	for child in node.get_children():
		node.remove_child(child)
		child.free()
