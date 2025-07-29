import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation_speed = random.uniform(-50, 50)
        self.rotation = 0
        self.create_lumpy_shape()

    def create_lumpy_shape(self):
        # Create irregular polygon shape
        self.points = []
        num_points = 8
        for i in range(num_points):
            angle = (360 / num_points) * i
            # Add random variation to radius
            variation = random.uniform(0.8, 1.2)
            distance = self.radius * variation
            x = distance * pygame.math.Vector2(1, 0).rotate(angle).x
            y = distance * pygame.math.Vector2(1, 0).rotate(angle).y
            self.points.append((x, y))

    def draw(self, screen):
        # Draw lumpy asteroid with rotation
        rotated_points = []
        for p in self.points:
            # Rotate point around origin
            rotated = pygame.math.Vector2(p).rotate(self.rotation)
            rotated_points.append((self.position.x + rotated.x, self.position.y + rotated.y))
        pygame.draw.polygon(screen, "white", rotated_points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_position()

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
