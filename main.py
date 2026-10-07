import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()


    updatable, drawable, asteroids, shots = [pygame.sprite.Group() for _ in range(4)]
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(x=SCREEN_WIDTH / 2, y= SCREEN_HEIGHT / 2)
    _asteroid_field = AsteroidField()
    

    dt: float = 0.0

    while True:
        log_state()
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        for object in drawable:
            object.draw(screen)

        for object in updatable:
            object.update(dt)

        for object in asteroids:
            if object.collides_with(player):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        for object in asteroids:
            for shot in shots:
                if object.collides_with(shot):
                    log_event("asteroid_shot")
                    object.split()
                    shot.kill()

        pygame.display.flip()
        print(dt)


if __name__ == "__main__":
    main()
