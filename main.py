import pygame
import random

WIDTH  = 1280
HEIGHT = 720

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
title = "Particles"

dt = 0
FPS = 60
clock = pygame.time.Clock()

font_size = 24
font = pygame.font.Font(pygame.font.get_default_font(), font_size)

N = 0
R = 2
K = WIDTH * 0.25

quit_game = False

class Particle:
    def __init__(self, pos):
        self.pos = pos

    def draw(self):
        p = pygame.Vector2(self.pos.x + WIDTH*0.5, self.pos.y + HEIGHT*0.5)
        pygame.draw.circle(screen, "white", p, R)

    # Gives birth to three other particle that are in a triangle formation
    def birth_particle(self):
        a = pygame.Vector2(self.pos.x/2, self.pos.y/2)
        a.y -= K * 0.5

        b = pygame.Vector2(self.pos.x/2, self.pos.y/2)
        b.x += K * -0.5
        b.y += K *  0.5

        c = pygame.Vector2(self.pos.x/2, self.pos.y/2)
        c.x += K *  0.5
        c.y += K *  0.5

        return [a, b, c]

def birth_particles(particles):
    new_particles = particles.copy()
    for p in particles:
        for x in p.birth_particle():
            new_particles.append(Particle(x))
    return new_particles

particles = [Particle(pygame.Vector2(0, 0))]

prev_right_key_state = False
prev_left_key_state  = False

right_key_pressed = False
left_key_pressed  = False

while not quit_game:
    right_key_state = pygame.key.get_pressed()[pygame.K_RIGHT]
    right_key_pressed = right_key_state and not prev_right_key_state
    prev_right_key_state = right_key_state

    left_key_state = pygame.key.get_pressed()[pygame.K_LEFT]
    left_key_pressed = left_key_state and not prev_left_key_state
    prev_left_key_state = left_key_state


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
    screen.fill("black")

    for p in particles:
        p.draw()

    if right_key_pressed:
        particles = [Particle(pygame.Vector2(0, 0))]
        N += 1
        for _ in range(N):
            particles = birth_particles(particles)

    if left_key_pressed and N > 0:
        particles = [Particle(pygame.Vector2(0, 0))]
        N -= 1
        for _ in range(N):
            particles = birth_particles(particles)

    tp = pygame.Vector2(0, 0)
    text_surf = font.render(f"Iterations: {N}", True, "white")
    screen.blit(text_surf, tp)
    tp.y += font_size

    text_surf = font.render(f"Particles: {len(particles)}", True, "white")
    screen.blit(text_surf, tp)
    tp.y += font_size

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000.0
    FPS_GOT = int(1//dt)

    pygame.display.set_caption(f"{title} | {FPS_GOT}/{FPS} fps | {dt} s")
