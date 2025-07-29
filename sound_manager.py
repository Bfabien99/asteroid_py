import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.load_sounds()
        
    def load_sounds(self):
        """Load all game sounds"""
        sound_files = {
            'shoot': 'sounds/shoot.wav',
            'explosion': 'sounds/explosion.wav',
            'thrust': 'sounds/thrust.wav',
            'powerup': 'sounds/powerup.wav',
            'menu_select': 'sounds/menu_select.wav'
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sfx_volume)
                except pygame.error:
                    print(f"Could not load sound: {path}")
            else:
                print(f"Sound file not found: {path}")
        
        # Load music
        music_path = 'sounds/main_theme.mp3'
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
            except pygame.error:
                print(f"Could not load music: {music_path}")
    
    def play_sound(self, name):
        """Play a sound effect"""
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_music(self, loops=-1):
        """Play background music"""
        pygame.mixer.music.play(loops)
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pause background music"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause background music"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds"""
        pygame.mixer.stop()