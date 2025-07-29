import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion


def reset_game():
    """Reset game state for a new game"""
    # Create new sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Clear any existing containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    
    # Create new game objects
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    return updatable, drawable, asteroids, shots, asteroid_field, player


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    updatable, drawable, asteroids, shots, asteroid_field, player = reset_game()

    dt = 0
    score = 0
    lives = PLAYER_LIVES
    paused = False
    game_over = False
    selected_option = 0  # 0 for Replay, 1 for Exit

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not game_over:
                    paused = not paused
                elif game_over:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_option = 1 - selected_option
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Replay
                            updatable, drawable, asteroids, shots, asteroid_field, player = reset_game()
                            score = 0
                            lives = PLAYER_LIVES
                            game_over = False
                            paused = False
                            dt = 0
                        else:  # Exit
                            return

        if not paused and not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player) and player.invulnerable_timer <= 0:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        # Create explosion for player
                        Explosion(player.position.x, player.position.y, player.radius)
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
        
        # Draw pause message
        if paused and not game_over:
            pause_text = font.render("PAUSED - Press P to resume", True, "white")
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_text, pause_rect)
        
        # Draw game over screen
        if game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill("black")
            screen.blit(overlay, (0, 0))
            
            # Game Over text
            game_over_text = big_font.render("GAME OVER", True, "white")
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(game_over_text, game_over_rect)
            
            # Score text
            final_score_text = font.render(f"Final Score: {score}", True, "white")
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(final_score_text, final_score_rect)
            
            # Menu options
            replay_color = "yellow" if selected_option == 0 else "white"
            exit_color = "yellow" if selected_option == 1 else "white"
            
            replay_text = font.render("Replay", True, replay_color)
            replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(replay_text, replay_rect)
            
            exit_text = font.render("Exit", True, exit_color)
            exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(exit_text, exit_rect)
            
            # Instructions
            instructions_text = font.render("Use ↑/↓ to select, Enter to confirm", True, "gray")
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        if not paused and not game_over:
            dt = clock.tick(60) / 1000
        else:
            clock.tick(60)  # Still limit framerate when paused or game over but don't update dt


if __name__ == "__main__":
    main()
