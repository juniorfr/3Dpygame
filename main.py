import sys
import pygame as pg
import pygame.gfxdraw
import math
from penger import VS, FS

# VS = [
#     {"x":  0.25, "y":  0.25, "z":  0.25},
#     {"x": -0.25, "y":  0.25, "z":  0.25},
#     {"x": -0.25, "y": -0.25, "z":  0.25},
#     {"x":  0.25, "y": -0.25, "z":  0.25},
#
#     {"x":  0.25, "y":  0.25, "z": -0.25},
#     {"x": -0.25, "y":  0.25, "z": -0.25},
#     {"x": -0.25, "y": -0.25, "z": -0.25},
#     {"x":  0.25, "y": -0.25, "z": -0.25},
# ]

# FS = [
#     [0, 1, 2, 3],
#     [4, 5, 6, 7],
#     [0, 4],
#     [1, 5],
#     [2, 6],
#     [3, 7],
# ]

# Definindo a cor das linhas
FOREGROUND_COLOR = (80, 255, 80)
# FPS target
FPS = 60

WIDTH = 800
HEIGHT = 800


def point(screen, x, y):
    s = 20
    # Cria um objeto Rect: (posição_x, posição_y, largura, altura)
    # Convertemos para int porque pixels não podem ser fracionados
    rect = pg.Rect(int(x - s / 2), int(y - s / 2), s, s)

    # Desenha o retângulo diretamente na tela principal
    pg.gfxdraw.box(screen, rect, FOREGROUND_COLOR)

def line(screen, p1, p2):
    # 1. Multiplica pelo zoom (SCALE) e centraliza (OFFSET)
    # 2. Converte para inteiro (int) pois a tela não aceita decimais
    x1 = int(p1['x'])
    y1 = int(p1['y'])
    x2 = int(p2['x'])
    y2 = int(p2['y'])

    pg.gfxdraw.line(screen, x1, y1, x2, y2, FOREGROUND_COLOR)

def display(p: dict) -> dict:
    return {
        "x": (p['x'] + 1) / 2 * WIDTH,
        "y": (1 - (p['y'] + 1) / 2) * HEIGHT,
    }

def project(coord: dict) -> dict:
    return {
        "x": coord['x']/coord['z'],
        "y": coord['y']/coord['z'],
    }

def translate_z(coord: dict, dz) -> dict:
    result ={"x": coord['x'], "y": coord['y'], "z": coord['z'] + dz}
    return result

def rotate_xz(coord: dict, angle) -> dict:
    c = math.cos(angle)

    s = math.sin(angle)

    result = {
        "x": coord["x"] * c - coord["z"] * s,
        "y": coord["y"],
        "z": coord["x"] * s + coord["z"] * c,
    }
    print(result)
    return result


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    dz = 3.0  # Afastei um pouco mais para ver melhor
    angle = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        dt = clock.tick(FPS) / 1000

        angle += math.pi * dt * 0.5

        screen.fill((16, 16, 16))

        # Desenhar as linhas
        for f in FS:
            for i in range(len(f)):
                a = VS[f[i]]
                b = VS[f[(i + 1) % len(f)]]

                # Projeta os pontos
                p1_proj = display(project(translate_z(rotate_xz(a, angle), dz)))
                p2_proj = display(project(translate_z(rotate_xz(b, angle), dz)))

                # A função line agora cuida da Escala e Inteiros
                line(screen, p1_proj, p2_proj)

        pg.display.flip()


if __name__ == "__main__":
    main()