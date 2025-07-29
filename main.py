import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    lives = PLAYER_LIVES

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player) and player.invulnerable_timer <= 0:
                lives -= 1
                if lives <= 0:
                    print(f"Game over! Final score: {score}")
                    sys.exit()
                else:
                    # Create explosion for player
                    Explosion(player.position.x, player.position.y, player.radius)
                    # Respawn player at center
                    player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    # Calculate score based on asteroid size
                    asteroid_kind = int(asteroid.radius / ASTEROID_MIN_RADIUS)
                    score += ASTEROID_SCORE.get(asteroid_kind, 0)
                    # Create explosion effect
                    Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
