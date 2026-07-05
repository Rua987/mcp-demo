extends AnimatableBody2D

@export var travel_x := 100.0
@export var speed := 70.0

var _origin_x: float
var _direction := 1.0


func _ready() -> void:
	_origin_x = global_position.x


func _physics_process(delta: float) -> void:
	global_position.x += speed * _direction * delta
	if abs(global_position.x - _origin_x) >= travel_x:
		_direction *= -1.0
