"""
=============================================================================
 PROJECT: Star-Force Sentinel (Space Shooter Build)
 VERSION: 9.9.9 [Stable Archive]
 LEAD DEVELOPER: Nosrat Jahan
 STATUS: v2025.1 Portfolio Legacy Build
=============================================================================
 DEV NOTES:
 - Using Arcade's SpriteList for better FPS on older hardware.
 - Integrated simple ping-pong movement logic for enemy fleet.
 - Scaling factor 0.5 works best for 900x600 resolution.
 - Need to fix: Audio implementation for laser fire in next patch.
=============================================================================
"""

import arcade
import random

# Global config - standard 900x600 for better aspect ratio
SCREEN_W = 900
SCREEN_H = 600
GAME_TITLE = "Star-Force Sentinel | Build: Nosrat-Jahan"

# Asset Scaling (Adjusted for visual balance)
S_HERO = 0.5
S_FLEET = 0.5
S_BOLT = 0.8
MAX_ENEMIES = 15

class StarForceGame(arcade.Window):
    """
    Core game engine. 
    Manages sprites, physics updates, and user input.
    """

    def __init__(self):
        # Initializing parent window with global constants
        super().__init__(SCREEN_W, SCREEN_H, GAME_TITLE)
        
        # Space environment (Classic Black)
        arcade.set_background_color(arcade.color.BLACK)

        # Global sprite list containers
        self.player_assets = None
        self.enemy_fleet = None
        self.laser_bolts = None

        # State management
        self.ship = None
        self.total_score = 0

    def setup(self):
        """ Initial environment configuration and asset loading """
        self.player_assets = arcade.SpriteList()
        self.enemy_fleet = arcade.SpriteList()
        self.laser_bolts = arcade.SpriteList()

        self.total_score = 0

        # Constructing the Hero Ship
        # Asset path: built-in arcade resources
        hero_path = ":resources:images/space_shooter/playerShip1_orange.png"
        self.ship = arcade.Sprite(hero_path, S_HERO)
        self.ship.center_x = SCREEN_W // 2
        self.ship.center_y = 65 # Offset from screen bottom
        self.player_assets.append(self.ship)

        # Deploying the Invader Fleet 👾
        for i in range(MAX_ENEMIES):
            alien = arcade.Sprite(":resources:images/space_shooter/alienBige_clipping.png", S_FLEET)
            
            # Randomized spawn logic to keep gameplay fresh
            alien.center_x = random.randrange(SCREEN_W)
            alien.center_y = random.randrange(350, SCREEN_H - 50)
            
            # Initial drift velocity
            alien.change_x = random.randrange(-4, 5)
            if alien.change_x == 0: alien.change_x = 2 # Prevent stationary enemies
            
            self.enemy_fleet.append(alien)

    def on_draw(self):
        """ Render loop: drawing graphics to the screen """
        arcade.start_render()

        # Render all sprite layers (Order: Bottom to Top)
        self.laser_bolts.draw()
        self.enemy_fleet.draw()
        self.player_assets.draw()

        # HUD: Score and Branding
        arcade.draw_text(f"SCORE: {self.total_score}", 25, 30, arcade.color.NEON_GREEN, 11, bold=True)
        arcade.draw_text("Nosrat-Jahan | v9.9.9 Archive Build", SCREEN_W - 240, 30, arcade.color.DIM_GRAY, 8)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handling mouse movement for ship control """
        self.ship.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """ Laser firing logic on mouse click """
        bolt = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", S_BOLT)
        bolt.center_x = self.ship.center_x
        bolt.bottom = self.ship.top
        
        # Projectile vertical speed
        bolt.change_y = 12 
        self.laser_bolts.append(bolt)

    def on_update(self, delta_time):
        """ Physics and game loop updates """
        self.laser_bolts.update()
        self.enemy_fleet.update()

        # --- Resolve Collisions 💥 ---
        for bolt in self.laser_bolts:
            # Check if this laser hit any enemy in the fleet
            hits = arcade.check_for_collision_with_list(bolt, self.enemy_fleet)
            
            if len(hits) > 0:
                bolt.remove_from_sprite_lists() # Bolt destroyed on impact

            for target in hits:
                target.remove_from_sprite_lists() # Target neutralised
                self.total_score += 15 # +15 per kill

            # Cleanup: Despawn bolts that leave the viewport
            if bolt.bottom > SCREEN_H:
                bolt.remove_from_sprite_lists()

        # --- Enemy Boundary Management ---
        for invader in self.enemy_fleet:
            if invader.left < 0 or invader.right > SCREEN_W:
                invader.change_x *= -1 # Bounce back effect

def start_game():
    """ App entry point """
    window = StarForceGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    start_game()
