extends Area2D

@onready var _sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if body is CharacterBody2D:
		Game.add_coin()
		_collect()


func _collect() -> void:
	set_deferred("monitoring", false)
	var tween := create_tween()
	tween.tween_property(_sprite, "scale", Vector2(1.6, 1.6), 0.08)
	tween.parallel().tween_property(_sprite, "modulate:a", 0.0, 0.12)
	tween.tween_callback(queue_free)
