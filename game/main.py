import sys
import pygame

# CONFIGURACIÓN DE DIMENSIONES Y COLORES
ANCHO = 1000
ALTO = 700
ALTO_ARENA = 470   # Parte superior: escenario de batalla
ALTO_CAJA = 230    # Parte inferior: diálogos y botones
FPS = 60

COLOR_FONDO_ARENA = (34, 48, 68)
COLOR_SUELO_ARENA = (48, 68, 94)
COLOR_CAJA_INFERIOR = (28, 38, 56)
COLOR_BORDE_DORADO = (218, 178, 62)
COLOR_BLANCO = (245, 247, 250)

# INICIALIZAR PYGAME Y CREAR LA VENTANA
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Gran Esmeralda de la Vida - Paso 1")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("segoeui", 22, bold=True)

# BUCLE PRINCIPAL DEL JUEGO
while True:
    # A) Escuchar eventos (cerrar ventana, teclas, clics)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # B) Dibujar las capas en memoria (de atrás hacia adelante)
    # Parte superior: Arena de combate
    pygame.draw.rect(pantalla, COLOR_FONDO_ARENA, (0, 0, ANCHO, ALTO_ARENA))
    pygame.draw.rect(pantalla, COLOR_SUELO_ARENA, (0, ALTO_ARENA - 150, ANCHO, 150))

    # Parte inferior: Caja estilo Pokémon
    pygame.draw.rect(pantalla, COLOR_CAJA_INFERIOR, (0, ALTO_ARENA, ANCHO, ALTO_CAJA))
    pygame.draw.rect(
        pantalla,
        COLOR_BORDE_DORADO,
        (8, ALTO_ARENA + 8, ANCHO - 16, ALTO_CAJA - 16),
        width=4,
        border_radius=12
    )

    # Textos guía para visualizar la división
    txt_arriba = fuente.render("ZONA SUPERIOR (470 px): Escenario, sprites y barras de vida", True, COLOR_BLANCO)
    txt_abajo = fuente.render("ZONA INFERIOR (230 px): Narrativa secuencial y botones 2x2", True, COLOR_BORDE_DORADO)
    pantalla.blit(txt_arriba, (40, 40))
    pantalla.blit(txt_abajo, (40, ALTO_ARENA + 40))

    # C) Mostrar el fotograma terminado en la pantalla
    pygame.display.flip()
    reloj.tick(FPS)