SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_MAX_COUNT = 20  # Maximum asteroids on screen at once

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200

PLAYER_SHOOT_COOLDOWN = 0.3  # seconds
PLAYER_SHOOT_SPEED = 500

SHOT_RADIUS = 5

# Lives and respawning
PLAYER_LIVES = 3
PLAYER_MAX_LIVES = 5
RESPAWN_INVULNERABILITY_TIME = 3.0  # seconds
RESPAWN_BLINK_RATE = 0.1  # seconds

# Power-ups
POWERUP_RADIUS = 15
POWERUP_SPEED = 50
POWERUP_MAX_COUNT = 3  # Maximum power-ups on screen at once
POWERUP_SCORE_MIN = 200  # Minimum score increase to spawn power-up
POWERUP_SCORE_MAX = 1000  # Maximum score increase to spawn power-up
SHIELD_DURATION = 10.0  # seconds

# Scoring
ASTEROID_SCORE = {
    1: 100,  # Small asteroid
    2: 50,   # Medium asteroid
    3: 20    # Large asteroid
}
