import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
    
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # draw the player
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        # unit vector pointing straight up from (0,0) to (0,1)
        unit_vector = pygame.Vector2(0, 1)
        # rotate the vector until it's pointing the same dir as the player
        rotated_vector = unit_vector.rotate(self.rotation)
        # determine length player should move this frame
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        # move the player
        self.position += rotated_with_speed_vector

    def update(self, dt):
        # reduce the shot cooldown timer
        self.shot_cooldown_timer -= dt
        
        keys = pygame.key.get_pressed()

        # rotate left
        if keys[pygame.K_a]:
            self.rotate(-dt)
        # rotate right
        if keys[pygame.K_d]:
            self.rotate(dt)
        # move forward
        if keys[pygame.K_w]:
            self.move(dt)
        # move backward
        if keys[pygame.K_s]:
            self.move(-dt)
        # shoot
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return # don't shoot!
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot_vector = pygame.Vector2(0, 1)
        shot.velocity = shot_vector.rotate(self.rotation) * PLAYER_SHOOT_SPEED
        
