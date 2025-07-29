import pygame
import random
import math
from constants import *
from circleshape import CircleShape


class PowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_RADIUS)
        # Randomly choose power-up type
        self.type = random.choice(["extra_life", "instant_kill", "shield", "bomb"])
        
        # Set random velocity
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * POWERUP_SPEED
        
        # Visual properties
        self.pulse_timer = 0
        self.pulse_size = 0
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()
        
        # Pulsing effect
        self.pulse_timer += dt
        self.pulse_size = abs(math.sin(self.pulse_timer * 3)) * 5
        
    def draw(self, screen):
        # Draw outer circle with pulsing effect
        radius = self.radius + self.pulse_size
        
        # Set color based on type
        if self.type == "extra_life":
            color = "green"
            symbol = "+"
        elif self.type == "instant_kill":
            color = "red"
            symbol = "X"
        elif self.type == "shield":
            color = "cyan"
            symbol = "S"
        else:  # bomb
            color = "orange"
            symbol = "B"
        
        # Draw power-up circle
        pygame.draw.circle(screen, color, self.position, radius, 3)
        pygame.draw.circle(screen, color, self.position, radius - 5, 1)
        
        # Draw symbol in center
        font = pygame.font.Font(None, 24)
        text = font.render(symbol, True, color)
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)