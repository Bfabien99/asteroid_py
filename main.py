import sys
import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from scoreboard import Scoreboard
from powerup import PowerUp


def reset_game():
    """Reset game state for a new game"""
    # Create new sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # Clear any existing containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    AsteroidField.containers = updatable
    
    # Create new game objects
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    return updatable, drawable, asteroids, shots, powerups, asteroid_field, player


def show_main_menu(screen, font, big_font, clock, scoreboard):
    """Display main menu and return selected option"""
    selected = 0  # 0 for New Game, 1 for Scoreboard
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected = 1 - selected
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return "new_game"
                    else:
                        return "scoreboard"
        
        screen.fill("black")
        
        # Title
        title_text = big_font.render("ASTEROIDS", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # Menu options
        new_game_color = "yellow" if selected == 0 else "white"
        scoreboard_color = "yellow" if selected == 1 else "white"
        
        new_game_text = font.render("New Game", True, new_game_color)
        new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(new_game_text, new_game_rect)
        
        scoreboard_text = font.render("Scoreboard", True, scoreboard_color)
        scoreboard_rect = scoreboard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(scoreboard_text, scoreboard_rect)
        
        # Instructions
        instructions_text = font.render("Use ↑/↓ to select, Enter to confirm", True, "gray")
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(instructions_text, instructions_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_scoreboard(screen, font, big_font, clock, scoreboard):
    """Display scoreboard screen"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return "menu"
        
        screen.fill("black")
        
        # Title
        title_text = big_font.render("HIGH SCORES", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Scores
        scores = scoreboard.get_top_scores()
        y_pos = 200
        
        if not scores:
            no_scores_text = font.render("No scores yet!", True, "white")
            no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(no_scores_text, no_scores_rect)
        else:
            for i, entry in enumerate(scores):
                # Rank
                rank_text = font.render(f"{i+1}.", True, "white")
                rank_rect = rank_text.get_rect(right=SCREEN_WIDTH // 2 - 150, y=y_pos)
                screen.blit(rank_text, rank_rect)
                
                # Name
                name_text = font.render(entry["name"], True, "white")
                name_rect = name_text.get_rect(left=SCREEN_WIDTH // 2 - 100, y=y_pos)
                screen.blit(name_text, name_rect)
                
                # Score
                score_text = font.render(str(entry["score"]), True, "white")
                score_rect = score_text.get_rect(right=SCREEN_WIDTH // 2 + 100, y=y_pos)
                screen.blit(score_text, score_rect)
                
                # Date
                date_text = font.render(entry["date"], True, "gray")
                date_rect = date_text.get_rect(left=SCREEN_WIDTH // 2 + 120, y=y_pos)
                screen.blit(date_text, date_rect)
                
                y_pos += 40
        
        # Back instruction
        back_text = font.render("Press ESC or Enter to return", True, "gray")
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()
        clock.tick(60)


def get_player_name(screen, font, big_font, clock):
    """Get player name for high score"""
    name = ""
    cursor_visible = True
    cursor_timer = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode and len(name) < 12:
                    name += event.unicode
        
        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        
        screen.fill("black")
        
        # Title
        title_text = big_font.render("NEW HIGH SCORE!", True, "yellow")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # Prompt
        prompt_text = font.render("Enter your name:", True, "white")
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(prompt_text, prompt_rect)
        
        # Name input
        display_name = name + ("|" if cursor_visible else "")
        name_text = font.render(display_name, True, "white")
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(name_text, name_rect)
        
        # Instructions
        inst_text = font.render("Press Enter when done", True, "gray")
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(inst_text, inst_rect)
        
        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)
    
    scoreboard = Scoreboard()
    
    while True:
        # Show main menu
        menu_choice = show_main_menu(screen, font, big_font, clock, scoreboard)
        
        if menu_choice == "exit":
            return
        elif menu_choice == "scoreboard":
            result = show_scoreboard(screen, font, big_font, clock, scoreboard)
            if result == "exit":
                return
            continue
        
        # Start new game
        updatable, drawable, asteroids, shots, powerups, asteroid_field, player = reset_game()

        dt = 0
        score = 0
        lives = PLAYER_LIVES
        paused = False
        game_over = False
        score_saved = False
        selected_option = 0  # 0 for Replay, 1 for Menu

        # Game loop
        running = True
        while running:
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
                                # Reset game directly without returning to menu
                                updatable, drawable, asteroids, shots, powerups, asteroid_field, player = reset_game()
                                score = 0
                                lives = PLAYER_LIVES
                                game_over = False
                                score_saved = False
                                paused = False
                                dt = 0
                            else:  # Menu
                                running = False  # Exit this game loop to return to menu

            if not paused and not game_over:
                updatable.update(dt)

                for asteroid in asteroids:
                    if asteroid.collides_with(player) and player.invulnerable_timer <= 0 and not player.has_shield():
                        lives -= 1
                        if lives <= 0:
                            game_over = True
                            # Create explosion for player
                            Explosion(player.position.x, player.position.y, player.radius)
                            # Check if it's a high score
                            if not score_saved and scoreboard.is_high_score(score):
                                player_name = get_player_name(screen, font, big_font, clock)
                                if player_name:
                                    scoreboard.add_score(player_name, score)
                                score_saved = True
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
                            
                            # Chance to spawn power-up (limited to max count)
                            if random.random() < POWERUP_SPAWN_CHANCE and len(powerups) < POWERUP_MAX_COUNT:
                                PowerUp(asteroid.position.x, asteroid.position.y)
                            
                            asteroid.split()
                
                # Check power-up collisions
                for powerup in powerups:
                    if powerup.collides_with(player):
                        powerup.kill()
                        
                        if powerup.type == "extra_life":
                            if lives < PLAYER_MAX_LIVES:
                                lives += 1
                        elif powerup.type == "instant_kill":
                            # Kill all asteroids on screen
                            for asteroid in list(asteroids):
                                # Calculate score
                                asteroid_kind = int(asteroid.radius / ASTEROID_MIN_RADIUS)
                                score += ASTEROID_SCORE.get(asteroid_kind, 0)
                                # Create explosion
                                Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                                asteroid.kill()
                        elif powerup.type == "shield":
                            player.activate_shield()
                        elif powerup.type == "bomb":
                            # Instant death
                            lives = 0
                            game_over = True
                            # Create explosion for player
                            Explosion(player.position.x, player.position.y, player.radius)
                            # Check if it's a high score
                            if not score_saved and scoreboard.is_high_score(score):
                                player_name = get_player_name(screen, font, big_font, clock)
                                if player_name:
                                    scoreboard.add_score(player_name, score)
                                score_saved = True

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)

            # Draw score
            score_text = font.render(f"Score: {score}", True, "white")
            screen.blit(score_text, (10, 10))
            
            # Draw lives
            lives_text = font.render(f"Lives: {lives}", True, "white")
            screen.blit(lives_text, (10, 50))
            
            # Draw shield timer if active
            if player.shield_timer > 0:
                shield_text = font.render(f"Shield: {player.shield_timer:.1f}s", True, "cyan")
                screen.blit(shield_text, (10, 90))
        
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
                menu_color = "yellow" if selected_option == 1 else "white"
            
                replay_text = font.render("Replay", True, replay_color)
                replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                screen.blit(replay_text, replay_rect)
            
                menu_text = font.render("Menu", True, menu_color)
                menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                screen.blit(menu_text, menu_rect)
            
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
