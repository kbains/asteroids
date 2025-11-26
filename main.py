import sys
import pygame
from constants import *
from logger import log_state, log_event
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # initialize pygame
    pygame.init()
    # get new instance of a GUI window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # game clock to control FPS
    clock = pygame.time.Clock()
    dt = 0 #delta time

    # create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    # add Player and Asteroid classes to groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    # instantiate the player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()


    # game loop
    while True:
        log_state()
        # check if the user has closed the window and exit the game
        # allows using X to close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # player movement
        updatable.update(dt)

        # detect collisions
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # fill the screen with black
        screen.fill("black")
        # draw the player
        for d in drawable:
            d.draw(screen)
        # refresh the screen
        pygame.display.flip()
        # pause the game loop until 1/60th of a second has passed
        # convert from milliseconds to seconds
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
