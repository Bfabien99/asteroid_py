import pygame
from circleshape import CircleShape
import random


class Explosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.particles = []
        # Create particles for explosion effect
        for _ in range(8):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            velocity = pygame.Vector2(0, 1).rotate(angle) * speed
            lifetime = random.uniform(0.3, 0.6)
            self.particles.append({
                'pos': pygame.Vector2(x, y),
                'vel': velocity,
                'lifetime': lifetime,
                'initial_lifetime': lifetime
            })
        self.total_lifetime = 0.6

    def update(self, dt):
        self.total_lifetime -= dt
        if self.total_lifetime <= 0:
            self.kill()
            return

        for particle in self.particles:
            particle['pos'] += particle['vel'] * dt
            particle['lifetime'] -= dt

    def draw(self, screen):
        for particle in self.particles:
            if particle['lifetime'] > 0:
                # Fade out effect
                alpha = particle['lifetime'] / particle['initial_lifetime']
                size = int(3 * alpha)
                if size > 0:
                    brightness = int(255 * alpha)
                    color = (brightness, brightness, brightness)
                    pygame.draw.circle(screen, color, particle['pos'], size)