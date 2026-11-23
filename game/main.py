import sys
import pygame


# CONFIGURACIÓN GENERAL
ANCHO = 1000
ALTO = 700
ALTO_ARENA = 470

ALTO_CAJA = 230
FPS = 60

# Paleta estilo RPG
COLOR_FONDO_ARENA = (34, 48, 68)
COLOR_SUELO_ARENA = (48, 68, 94)
COLOR_CAJA_INFERIOR = (28, 38, 56)
COLOR_BORDE_DORADO = (218, 178, 62)
COLOR_BLANCO = (245, 247, 250)
COLOR_CREMA = (244, 242, 232)
COLOR_SELECCION = (255, 243, 196)
COLOR_TEXTO_OSCURO = (32, 36, 44)
COLOR_BORDE_OSCURO = (42, 48, 60)


def dibujar_texto_multilinea(superficie, texto, fuente, color, rect):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        subpalabras = palabra.split("\n")
        for idx, sub in enumerate(subpalabras):
            if idx > 0:
                lineas.append(linea_actual)
                linea_actual = sub
                continue
            prueba = f"{linea_actual} {sub}".strip()
            if fuente.size(prueba)[0] <= rect.width:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = sub
    if linea_actual:
        lineas.append(linea_actual)

    y = rect.y
    for linea in lineas:
        if y + fuente.get_linesize() > rect.bottom:
            break
        render = fuente.render(linea, True, color)
        superficie.blit(render, (rect.x, y))
        y += fuente.get_linesize()


# Escenas con páginas de texto + opciones + resultado
ESCENAS_DEMO = {
    "jungla_1": {
        "paginas": [
            "acabas de salir del reino y esta atravesando la jungla de los bambus",
            "detras de los bambus aparece un monstruo azul orejon de un metro que empieza a gritar",
            "que haras??"
        ],
        "opciones": [
            {
                "texto": "atacar",
                "resultado": ["atacas al enemigo y le haces 20 de daño."],
                "siguiente": "jungla_2"
            },
            {
                "texto": "intentar hablar con el",
                "resultado": ["intentas hablar con el monstruo, no quiere hablar y te tira a su mini hijo que te muerde (-20 HP)."],
                "siguiente": "jungla_2"
            },
            {
                "texto": "ignorarlo",
                "resultado": ["ignoras al monstruo y lo pasas de largo, el monstruo te ataca desde la espalda y te mata."],
                "siguiente": "jungla_1"
            }
        ]
    },
    "jungla_2": {
        "paginas": ["cual es tu siguiente movimiento??"],
        "opciones": [
            {
                "texto": "atacar",
                "resultado": ["atacas al monstruo con tu espada de hierro."],
                "siguiente": "jungla_1"
            },
            {
                "texto": "curarse",
                "resultado": ["te curas 20 puntos de vida."],
                "siguiente": "jungla_1"
            },
            {
                "texto": "huir",
                "resultado": ["intentaste escapar, el monstruo te ataca desde la espalda y te mata."],
                "siguiente": "jungla_1"
            }
        ]
    }
}

# INICIALIZAR PYGAME
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Gran Esmeralda de la Vida - Paso 3")
reloj = pygame.time.Clock()

fuente_narrativa = pygame.font.SysFont("segoeui", 22, bold=True)
fuente_prompt = pygame.font.SysFont("segoeui", 21, bold=True)
fuente_boton = pygame.font.SysFont("segoeui", 17, bold=True)
fuente_guia = pygame.font.SysFont("segoeui", 17)

# VARIABLES DE ESTADO DE LA MÁQUINA DE ESTADOS
escena_actual = "jungla_1"
estado_ui = "LEYENDO"          # Puede ser "LEYENDO" o "ELIGIENDO"
paginas_actuales = []
indice_pagina = 0
letras_visibles = 0.0
velocidad_texto = 50.0
tiempo_total = 0.0

opciones_actuales = []
botones_rects = []
indice_seleccionado = 0
mostrando_resultado = False
siguiente_escena_pendiente = None


def construir_cuadricula_botones(opciones):
    """Calcula los rectángulos 2x2 a la derecha de la caja inferior."""
    rects = []
    x_inicio = 385
    y_inicio = ALTO_ARENA + 20
    ancho_total = ANCHO - x_inicio - 20
    alto_total = ALTO_CAJA - 40
    sep = 10

    ancho_btn = (ancho_total - sep) // 2
    alto_btn = (alto_total - sep) // 2

    for i in range(len(opciones)):
        col = i % 2
        fila = i // 2
        rect = pygame.Rect(
            x_inicio + col * (ancho_btn + sep),
            y_inicio + fila * (alto_btn + sep),
            ancho_btn,
            alto_btn
        )
        rects.append(rect)
    return rects


def cargar_escena(id_escena):
    global escena_actual, estado_ui, paginas_actuales, indice_pagina
    global letras_visibles, opciones_actuales, botones_rects, indice_seleccionado, mostrando_resultado

    escena_actual = id_escena
    datos = ESCENAS_DEMO[id_escena]
    paginas_actuales = datos["paginas"]
    opciones_actuales = datos["opciones"]
    botones_rects = construir_cuadricula_botones(opciones_actuales)

    indice_pagina = 0
    letras_visibles = 0.0
    indice_seleccionado = 0
    mostrando_resultado = False
    estado_ui = "LEYENDO"


def avanzar_lectura():
    global indice_pagina, letras_visibles, estado_ui
    texto = paginas_actuales[indice_pagina]

    if int(letras_visibles) < len(texto):
        letras_visibles = float(len(texto))
    elif indice_pagina < len(paginas_actuales) - 1:
        indice_pagina += 1
        letras_visibles = 0.0
    else:
        # Si estábamos leyendo el resultado de un ataque, pasamos a la siguiente escena
        if mostrando_resultado:
            cargar_escena(siguiente_escena_pendiente)
        else:
            # Si terminamos la pregunta, desplegamos el menú 2x2
            estado_ui = "ELIGIENDO"
            indice_seleccionado = 0


def confirmar_opcion(indice):
    global paginas_actuales, indice_pagina, letras_visibles, estado_ui
    global mostrando_resultado, siguiente_escena_pendiente

    opcion = opciones_actuales[indice]
    paginas_actuales = opcion["resultado"]
    siguiente_escena_pendiente = opcion["siguiente"]
    indice_pagina = 0
    letras_visibles = 0.0
    mostrando_resultado = True
    estado_ui = "LEYENDO"


# Arrancar la primera escena
cargar_escena("jungla_1")

# BUCLE PRINCIPAL
while True:
    dt = reloj.tick(FPS) / 1000.0
    tiempo_total += dt
    pos_mouse = pygame.mouse.get_pos()

    # Si estamos eligiendo, mover el cursor ▶ si el ratón pasa por encima de un botón
    if estado_ui == "ELIGIENDO":
        for i, rect in enumerate(botones_rects):
            if rect.collidepoint(pos_mouse):
                indice_seleccionado = i

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_ui == "LEYENDO":
                avanzar_lectura()
            elif estado_ui == "ELIGIENDO":
                for i, rect in enumerate(botones_rects):
                    if rect.collidepoint(evento.pos):
                        confirmar_opcion(i)
                        break

        if evento.type == pygame.KEYDOWN:
            if estado_ui == "LEYENDO":
                if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                    avanzar_lectura()
            elif estado_ui == "ELIGIENDO":
                total = len(opciones_actuales)
                if evento.key == pygame.K_RIGHT and indice_seleccionado + 1 < total:
                    indice_seleccionado += 1
                elif evento.key == pygame.K_LEFT and indice_seleccionado - 1 >= 0:
                    indice_seleccionado -= 1
                elif evento.key == pygame.K_DOWN and indice_seleccionado + 2 < total:
                    indice_seleccionado += 2
                elif evento.key == pygame.K_UP and indice_seleccionado - 2 >= 0:
                    indice_seleccionado -= 2
                elif evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                    confirmar_opcion(indice_seleccionado)
                elif evento.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    idx = evento.key - pygame.K_1
                    if idx < total:
                        confirmar_opcion(idx)

    # Actualizar animación de escritura
    if estado_ui == "LEYENDO":
        texto_actual = paginas_actuales[indice_pagina]
        if letras_visibles < len(texto_actual):
            letras_visibles = min(len(texto_actual), letras_visibles + velocidad_texto * dt)

    # DIBUJAR ARENA SUPERIOR
    pygame.draw.rect(pantalla, COLOR_FONDO_ARENA, (0, 0, ANCHO, ALTO_ARENA))
    pygame.draw.rect(pantalla, COLOR_SUELO_ARENA, (0, ALTO_ARENA - 150, ANCHO, 150))
    info = fuente_guia.render(f"Estado actual: {estado_ui}  |  Usa Flechas + Enter, teclas 1-3 o el Ratón", True, COLOR_BLANCO)
    pantalla.blit(info, (25, 20))

    # DIBUJAR CAJA INFERIOR
    pygame.draw.rect(pantalla, COLOR_CAJA_INFERIOR, (0, ALTO_ARENA, ANCHO, ALTO_CAJA))
    pygame.draw.rect(pantalla, COLOR_BORDE_DORADO, (8, ALTO_ARENA + 8, ANCHO - 16, ALTO_CAJA - 16), width=4, border_radius=12)

    if estado_ui == "LEYENDO":
        texto_recortado = paginas_actuales[indice_pagina][:int(letras_visibles)]
        area_texto = pygame.Rect(34, ALTO_ARENA + 28, ANCHO - 68, ALTO_CAJA - 70)
        dibujar_texto_multilinea(pantalla, texto_recortado, fuente_narrativa, COLOR_BLANCO, area_texto)

        if int(letras_visibles) >= len(paginas_actuales[indice_pagina]) and int(tiempo_total * 3) % 2 == 0:
            flecha = fuente_narrativa.render("▼", True, COLOR_BORDE_DORADO)
            pantalla.blit(flecha, (ANCHO - 55, ALTO - 52))

    elif estado_ui == "ELIGIENDO":
        # Panel izquierdo: Pregunta de acción
        caja_izq = pygame.Rect(20, ALTO_ARENA + 20, 350, ALTO_CAJA - 40)
        pygame.draw.rect(pantalla, (20, 28, 42), caja_izq, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_BLANCO, caja_izq, width=2, border_radius=10)
        dibujar_texto_multilinea(
            pantalla, "¿Qué hará\nel caballero?", fuente_prompt, COLOR_BLANCO,
            pygame.Rect(caja_izq.x + 22, caja_izq.y + 45, caja_izq.width - 44, 100)
        )

        # Panel derecho: Cuadrícula 2x2 de opciones
        for i, rect in enumerate(botones_rects):
            seleccionado = (i == indice_seleccionado)
            color_fondo = COLOR_SELECCION if seleccionado else COLOR_CREMA
            color_borde = COLOR_BORDE_DORADO if seleccionado else COLOR_BORDE_OSCURO

            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=8)
            pygame.draw.rect(pantalla, color_borde, rect, width=3, border_radius=8)

            cursor = "▶ " if seleccionado else "   "
            etiqueta = f"{cursor}{opciones_actuales[i]['texto']}"
            area_btn = pygame.Rect(rect.x + 12, rect.y + 10, rect.width - 24, rect.height - 20)
            dibujar_texto_multilinea(pantalla, etiqueta, fuente_boton, COLOR_TEXTO_OSCURO, area_btn)

    pygame.display.flip()
    reloj.tick(FPS)