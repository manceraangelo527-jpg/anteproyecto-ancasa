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

# Ajustar texto largo dentro de la caja ---
def dibujar_texto_multilinea(superficie, texto, fuente, color, rect):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = f"{linea_actual} {palabra}".strip()
        if fuente.size(prueba)[0] <= rect.width:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)

    y = rect.y
    for linea in lineas:
        if y + fuente.get_linesize() > rect.bottom:
            break
        render = fuente.render(linea, True, color)
        superficie.blit(render, (rect.x, y))
        y += fuente.get_linesize()

# INICIALIZAR PYGAME Y CREAR LA VENTANA
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Gran Esmeralda de la Vida")
reloj = pygame.time.Clock()
fuente_narrativa = pygame.font.SysFont("segoeui", 22, bold=True)
fuente_guia = pygame.font.SysFont("segoeui", 18)

# Páginas de narrativa y estado del texto
paginas_dialogo = [
    "bienvenido al primer minijuego de ANCASA Games",
    "ANCASA es el mejor caballero de todo el reino, y te asignaron la gran mision...",
    "una mision cuyo objetivo es matar al malvado rey de los pinguinos que ha robado la gran esmeralda de la vida."
]

indice_pagina = 0
letras_visibles = 0.0
velocidad_texto = 45.0
tiempo_total = 0.0

def avanzar_dialogo():
    global indice_pagina, letras_visibles
    texto_actual = paginas_dialogo[indice_pagina]

    # Si todavía no termina de escribirse, completarlo de inmediato
    if int(letras_visibles) < len(texto_actual):
        letras_visibles = float(len(texto_actual))
    # Si ya terminó y hay más páginas, avanzar a la siguiente
    elif indice_pagina < len(paginas_dialogo) - 1:
        indice_pagina += 1
        letras_visibles = 0.0

# BUCLE PRINCIPAL DEL JUEGO
while True:
    # dt = segundos transcurridos desde el fotograma anterior
    dt = reloj.tick(FPS) / 1000.0
    tiempo_total += dt

    # Escuchar eventos (cerrar ventana, teclas, clics)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Avanzar diálogo con clic izquierdo o teclas Espacio / Enter
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            avanzar_dialogo()
        elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_RETURN):
            avanzar_dialogo()
    # Actualizar animación de letras
    texto_actual = paginas_dialogo[indice_pagina]
    if letras_visibles < len(texto_actual):
        letras_visibles = min(len(texto_actual), letras_visibles + velocidad_texto * dt)

    # Dibujar las capas en memoria (de atrás hacia adelante)
    # Parte superior: Arena de combate
    pygame.draw.rect(pantalla, COLOR_FONDO_ARENA, (0, 0, ANCHO, ALTO_ARENA))
    pygame.draw.rect(pantalla, COLOR_SUELO_ARENA, (0, ALTO_ARENA - 150, ANCHO, 150))
    info = fuente_guia.render(f"Página {indice_pagina + 1} de {len(paginas_dialogo)} (Haz clic o presiona Espacio)", True, COLOR_BLANCO)
    pantalla.blit(info, (30, 25))

    # Parte inferior
    pygame.draw.rect(pantalla, COLOR_CAJA_INFERIOR, (0, ALTO_ARENA, ANCHO, ALTO_CAJA))
    pygame.draw.rect(pantalla, COLOR_BORDE_DORADO, (8, ALTO_ARENA + 8, ANCHO - 16, ALTO_CAJA - 16), width=4, border_radius=12
    )

    # Dibujar solo las letras visibles hasta este instante
    texto_recortado = texto_actual[:int(letras_visibles)]
    area_texto = pygame.Rect(34, ALTO_ARENA + 28, ANCHO - 68, ALTO_CAJA - 70)
    dibujar_texto_multilinea(pantalla, texto_recortado, fuente_narrativa, COLOR_BLANCO, area_texto)

# Indicador ▼ parpadeante cuando el párrafo termina
    texto_terminado = int(letras_visibles) >= len(texto_actual)
    hay_mas_paginas = indice_pagina < len(paginas_dialogo) - 1
    if texto_terminado and hay_mas_paginas and int(tiempo_total * 3) % 2 == 0:
        flecha = fuente_narrativa.render("▼", True, COLOR_BORDE_DORADO)
        pantalla.blit(flecha, (ANCHO - 55, ALTO - 52))

    # Mostrar el fotograma terminado en la pantalla
    pygame.display.flip()
    reloj.tick(FPS)