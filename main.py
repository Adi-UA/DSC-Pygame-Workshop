# Author: Adi-UA

import pygame
import os
import random

########################################################################################################################

# STEP 1

def image_reader(directory, filename):
    """
    This function grabs the images from the specified filepath using pygame's
    image.load functionality and then returns them. It also scales the images to
    2x and uses convert() to boost performance.
    Arguments: directory   -- Path to the directory in which the image is
        located filename  -- The filename for the image.
    Returns: -- The image at the given location
    """

    return pygame.transform.scale2x(
        pygame.image.load(
            os.path.join(
                directory,
                filename))).convert_alpha()

pygame.init()
game_clock = pygame.time.Clock()

WIN_WIDTH = 1280
WIN_HEIGHT = 720
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

resource_path = os.path.dirname(__file__)  # Path to current directory
ENEMY_SHIP_IMG = image_reader(resource_path, "alien.png")
PLAYER_SHIP_IMG = image_reader(resource_path, "player_ship.png")

########################################################################################################################

# STEP 2

class EnemyShip:
    def __init__(self, x, y):
        """
        Initializes the enemy ship object

        Args:
            x (int): The x coordinate of this object on the screen
            y (int): The y coordinate of this object on the screen
        """

        self.x = x
        self.y = y

        self.has_collided = False  # Allows us to ensure collision only occurs once in its lifetime

        self.y_velocity = 0.3 / 100 * WIN_HEIGHT

        self.img = ENEMY_SHIP_IMG


    def draw(self, window):
        """
        Draws the enemy ship onto the given pygame window.
        """

        window.blit(self.img, (self.x, self.y))


    def collide(self, player_ship):
        """
        Checks if the enemy ship has collided with the given player object.

        Args:
            player_ship (PlayerShip): The player ship to check collision against

        Returns:
            boolean: True if collision occured and False otherwise
        """

        if not self.has_collided:
            player_ship_mask = player_ship.get_mask()
            self_mask = pygame.mask.from_surface(self.img)

            offset = (round(self.x - player_ship.x),
                      round(self.y - player_ship.y))

            overlaps = player_ship_mask.overlap(self_mask, offset)

            if overlaps:
                self.has_collided = True
                return True
            else:
                return False
        else:
            return False


    def get_mask(self):
        """
        Gets the mask for this object
        """

        return pygame.mask.from_surface(self.img)


    def move(self, reverse=False):
        """
        Defines how the object should move at each frame
        """

        if reverse:
            self.y_velocity = -self.y_velocity * 1.5

        self.y += self.y_velocity

########################################################################################################################

# STEP 3

class PlayerShip:
    def __init__(self, x, y):
        """
        Initializes the player ship object

        Args:
            x (int): The x coordinate of this object on the screen
            y (int): The y coordinate of this object on the screen
        """
        self.x = x
        self.y = y

        self.x_velocity = 0.6 / 100 * WIN_WIDTH

        self.MOVE_TICK = 0  # Controls acceleration

        self.img = PLAYER_SHIP_IMG


    def draw(self, window):
        """
        Draws the enemy ship onto the given pygame window.
        """
        
        window.blit(self.img, (self.x, self.y))


    def move(self, direction):
        """
        Defines how the object moves at each tick when told to move left,
        right or neither.

        Args:
            direction (str): "L" - Left, "R" - Right, Anything else results in no movement
        """

        if direction == "L":
            new_x = self.x - (self.x_velocity + self.MOVE_TICK)
        elif direction == "R":
            new_x = self.x + (self.x_velocity + self.MOVE_TICK)
        else:
            self.MOVE_TICK = 0
            return

        if new_x > 10 and new_x < WIN_WIDTH - 62:
            self.x = new_x

        if self.MOVE_TICK < 4:
            self.MOVE_TICK += 1


    def get_mask(self):
        """
        Gets the mask for this object
        """

        return pygame.mask.from_surface(self.img)

########################################################################################################################