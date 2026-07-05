extends CharacterBody2D

const SPEED := 220.0
const JUMP_VELOCITY := -380.0
const FALL_LIMIT_Y := 420.0

var _spawn_position: Vector2

@onready var _sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	_spawn_position = global_position


func set_spawn(pos: Vector2) -> void:
	_spawn_position = pos
	global_position = pos
	velocity = Vector2.ZERO


func _physics_process(delta: float) -> void:
	if Game.is_won or Game.era_complete_pending:
		velocity = Vector2.ZERO
		move_and_slide()
		return

	if global_position.y > FALL_LIMIT_Y:
		respawn()
		return

	if not is_on_floor():
		velocity += get_gravity() * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0.0:
		velocity.x = direction * SPEED
		_sprite.flip_h = direction < 0.0
	else:
		velocity.x = move_toward(velocity.x, 0.0, SPEED)

	move_and_slide()


func respawn() -> void:
	Game.register_death()
	global_position = _spawn_position
	velocity = Vector2.ZERO
