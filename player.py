import pygame
import math
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.invulnerable_timer = 0
        self.blink_timer = 0
        self.visible = True
        self.shield_timer = 0

    def draw(self, screen):
        if self.visible:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
            
        # Draw shield if active
        if self.shield_timer > 0:
            # Animated shield effect
            shield_alpha = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.5 + 0.5
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 10, 2)
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 15, 1)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        
        # Handle shield timer
        if self.shield_timer > 0:
            self.shield_timer -= dt
        
        # Handle invulnerability
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = RESPAWN_BLINK_RATE
        else:
            self.visible = True
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.wrap_position()
    
    def respawn(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = RESPAWN_INVULNERABILITY_TIME
        self.visible = True
        self.shield_timer = 0  # Reset shield on respawn
        
    def has_shield(self):
        return self.shield_timer > 0
        
    def activate_shield(self):
        self.shield_timer = SHIELD_DURATION
