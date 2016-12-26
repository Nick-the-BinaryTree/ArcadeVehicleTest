"""
A vehicle physics test for the Python Arcade Library.

Based primarily on: https://pythonhosted.org/arcade/examples/sprite_ramps.html

By Nicholas Hartunian
"""

"""
Load a map stored in csv format, as exported by the program 'Tiled.'

Artwork from http://kenney.nl
"""
import arcade

SPRITE_SCALING = .5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 500

# Right edge of the map in pixels
END_OF_MAP = 3500

# Physics variables
GRAVITY = 0.5
DRAG = 0.2
ACCL = 0.5
SPEED_CAP = 15

def get_map():
    map_file = open("map.csv")
    map_array = []

    for line in map_file:
        line = line.strip()
        map_row = line.split(",")

        if map_row[-1] == '':
            del map_row[-1]

        for index, item in enumerate(map_row):
            map_row[index] = int(item)
        map_array.append(map_row)
    return map_array

class MyAppWindow(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        """
        Initializer
        :param width:
        :param height:
        """
        super().__init__(width, height)

        # Sprite lists
        self.all_sprites_list = None

        # Set up player
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.LEFT_DOWN = False
        self.RIGHT_DOWN = False

    def start_new_game(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up player
        self.player_sprite = arcade.Sprite("img/car.png", SPRITE_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270
        self.player_sprite.change_x = 0 # Added
        self.player_sprite.change_y = 0
        self.all_sprites_list.append(self.player_sprite)

        map_array = get_map()

        map_items = ["img/slice03_03.png",
                     "img/slice27_27.png",
                     "img/slice06_06.png",
                     "img/slice07_07.png"]

        if __name__ == '__main__':
            for row_index, row in enumerate(map_array):
                for column_index, item in enumerate(row):
                    if item == 0:
                        continue
                    else:
                        wall = arcade.Sprite(map_items[item-1], 1) # Adjust for empty tile zero starting index in CSV

                        # Change the collision polygon to be a ramp instead of
                        # a rectangle
                        if item == 3:
                            wall.points = ((-wall.width // 2, wall.height // 2),
                                           (wall.width // 2, -wall.height // 2),
                                           (-wall.width // 2, -wall.height // 2))
                        elif item == 4:
                             wall.points = ((-wall.width // 2, -wall.height // 2),
                                           (wall.width // 2, -wall.height // 2),
                                           (wall.width // 2, wall.height // 2))

                    wall.right = column_index * 70
                    wall.top = (15 - row_index) * 70
                    self.all_sprites_list.append(wall)
                    self.wall_list.append(wall)

                self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                                     self.wall_list,
                                                                     gravity_constant=GRAVITY)

                arcade.set_background_color(arcade.color.AERO_BLUE)

                # Set the viewport boundaries
                # These numbers set where we have 'scrolled' to.
                self.view_left = 0
                self.view_bottom = 0

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        self.all_sprites_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
           self.LEFT_DOWN = True
        elif key == arcade.key.RIGHT:
            self.RIGHT_DOWN = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.LEFT_DOWN = False
        elif key == arcade.key.RIGHT:
            self.RIGHT_DOWN = False

    def animate(self, delta_time):
        """ Movement and game logic """
        # Add car drag
        if self.player_sprite.change_x > 0:
            self.player_sprite.change_x -= DRAG
        elif self.player_sprite.change_x < 0:
            self.player_sprite.change_x += DRAG

        # Add acceleration

        if self.LEFT_DOWN and self.player_sprite.change_x > -SPEED_CAP:
            self.player_sprite.change_x -= ACCL
        elif self.RIGHT_DOWN and self.player_sprite.change_x < SPEED_CAP:
            self.player_sprite.change_x += ACCL

        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= int(left_bndry - self.player_sprite.left)
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += int(self.player_sprite.right - right_bndry)
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += int(self.player_sprite.top - top_bndry)
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= int(bottom_bndry - self.player_sprite.bottom)
            changed = True

        # If we need to scroll, let's do it!
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
def main():
    window = MyAppWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.start_new_game()
    arcade.run()

if __name__ == "__main__":
    main()