import os
import sys
import math
import pygame

# CONFIGURACIÓN GENERAL
ANCHO = 1000
ALTO = 700
ALTO_ARENA = 470
ALTO_CAJA = 230
FPS = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")

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

# Colores de barras de vida
HP_VERDE = (56, 200, 96)
HP_AMARILLO = (242, 196, 48)
HP_ROJO = (228, 64, 64)


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


# ESCENAS DEL COMBATE DE LA JUNGLA CON DAÑO REAL
ESCENAS_JUNGLA = {
    "jungla_1": {
        "sprite_enemigo": "stich_frente.png",
        "paginas": [
            "acabas de salir del reino y estas atravesando la jungla de los bambus",
            "detras de los bambus aparece un monstruo azul orejon de un metro que empieza a gritar",
            "que haras??"
        ],
        "opciones": [
            {
                "texto": "atacar",
                "dano_enemigo": 20,
                "resultado": ["atacas al enemigo y le haces 20 de daño."],
                "siguiente": "jungla_2"
            },
            {
                "texto": "intentar hablar con el",
                "dano_jugador": 20,
                "resultado": ["intentas hablar con el monstruo, no quiere hablar y te tira a su mini hijo que te muerde."],
                "siguiente": "jungla_2"
            },
            {
                "texto": "ignorarlo",
                "dano_jugador": 100,
                "resultado": ["ignoras al monstruo y lo pasas de largo, el monstruo te ataca desde la espalda y te mata."],
                "siguiente": "jungla_2"
            }
        ]
    },
    "jungla_2": {
        "sprite_enemigo": "stich_frente.png",
        "paginas": ["cual es tu siguiente movimiento??"],
        "opciones": [
            {
                "texto": "atacar",
                "dano_enemigo": 20,
                "resultado": ["atacas al monstruo con tu espada de hierro."],
                "siguiente": "jungla_3"
            },
            {
                "texto": "curarse",
                "curar_jugador": 20,
                "resultado": ["te curas la vida (+20 HP)."],
                "siguiente": "jungla_3"
            },
            {
                "texto": "huir",
                "dano_jugador": 100,
                "resultado": ["intentaste escapar, el monstruo te ataca desde la espalda y te mata."],
                "siguiente": "jungla_3"
            }
        ]
    },
    "jungla_3": {
        "sprite_enemigo": "stich_hijos_frente.png",
        "paginas": ["el monstruo acaba de sacar mas de sus hijos que estan por atacarte, que haras?"],
        "opciones": [
            {
                "texto": "ignorarlos y contraatacar",
                "dano_jugador": 30,
                "resultado": ["contraatacas pero los mini hijos te muerden y te hacen heridas."],
                "siguiente": "jungla_4"
            },
            {
                "texto": "defenderse",
                "dano_jugador": 5,
                "resultado": ["te defiendes de los mini hijos pero recibes un poco de daño."],
                "siguiente": "jungla_4"
            },
            {
                "texto": "atacar a los hijos del monstruo",
                "dano_enemigo": 10,
                "resultado": ["matas a los hijos del monstruo sin recibir daño, el monstruo recibe daño psicologico."],
                "siguiente": "jungla_4"
            }
        ]
    },
    "jungla_4": {
        "sprite_enemigo": "stich_frente.png",
        "paginas": ["tienes que hacer una estrategia para derrotar al monstruo, que haras?"],
        "opciones": [
            {
                "texto": "atacar de frente",
                "dano_enemigo": 100,
                "dano_jugador": 10,
                "resultado": ["atacas de frente y aunque recibes daño matas al enemigo."],
                "siguiente": "victoria_jungla"
            },
            {
                "texto": "tirarle comida para que se distraiga",
                "dano_jugador": 100,
                "resultado": ["le tiras comida la cual el monstruo ignora y te mata."],
                "siguiente": "victoria_jungla"
            },
            {
                "texto": "atacar por sorpresa tras los arboles",
                "dano_enemigo": 100,
                "resultado": ["te pones detras de los arboles rodeandolo y lo atacas por la espalda y lo matas."],
                "siguiente": "victoria_jungla"
            }
        ]
    },
    "derrota_jungla": {
        "sprite_enemigo": "stich_frente.png",
        "paginas": ["Has caído en combate. Reintentas desde el checkpoint de la jungla..."],
        "opciones": [
            {
                "texto": "Reintentar combate",
                "reiniciar_combate": True,
                "resultado": ["¡Vuelves a la jungla con toda tu vida!"],
                "siguiente": "jungla_1"
            }
        ]
    },
    "victoria_jungla": {
        "sprite_enemigo": None,
        "paginas": ["¡Has derrotado al monstruo azul! Sigues con tu aventura hacia el pueblo."],
        "opciones": [
            {
                "texto": "Repetir demo de combate",
                "reiniciar_combate": True,
                "resultado": ["Reiniciando encuentro en la jungla..."],
                "siguiente": "jungla_1"
            }
        ]
    }
}

# INICIALIZAR PYGAME
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Gran Esmeralda de la Vida - Paso 4 (Arena Pokémon)")
reloj = pygame.time.Clock()

fuente_nombre = pygame.font.SysFont("segoeui", 19, bold=True)
fuente_hud = pygame.font.SysFont("segoeui", 15, bold=True)
fuente_narrativa = pygame.font.SysFont("segoeui", 22, bold=True)
fuente_prompt = pygame.font.SysFont("segoeui", 21, bold=True)
fuente_boton = pygame.font.SysFont("segoeui", 17, bold=True)

# ESTADO DEL JUGADOR, ENEMIGO Y ANIMACIONES
nombre_jugador = "ANCASA"
vida_jugador = 100
vida_max_jugador = 100
vida_visual_jugador = 100.0
dinero = 50

nombre_enemigo = "Monstruo Azul"
vida_enemigo = 100
vida_max_enemigo = 100
vida_visual_enemigo = 100.0

# Temporizadores de efectos visuales
tiempo_total = 0.0
shake_jugador = 0.0
shake_enemigo = 0.0
flash_color = None
flash_alpha = 0.0
cache_sprites = {}

# Variables de la máquina de estados
escena_actual = "jungla_1"
estado_ui = "LEYENDO"
paginas_actuales = []
indice_pagina = 0
letras_visibles = 0.0
velocidad_texto = 55.0

opciones_actuales = []
botones_rects = []
indice_seleccionado = 0
mostrando_resultado = False
siguiente_escena_pendiente = None


# Carga de sprites y dibujo de cajas de estado
def obtener_sprite(nombre_archivo, tamano):
    clave = (nombre_archivo, tamano)
    if clave in cache_sprites:
        return cache_sprites[clave]

    ruta = os.path.join(IMG_DIR, nombre_archivo)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.smoothscale(img, tamano)
    else:
        # Silueta provisional elegante mientras agregas los PNG
        img = pygame.Surface(tamano, pygame.SRCALPHA)
        pygame.draw.rect(img, (48, 62, 88, 230), (15, 15, tamano[0] - 30, tamano[1] - 30), border_radius=20)
        pygame.draw.rect(img, COLOR_BORDE_DORADO, (15, 15, tamano[0] - 30, tamano[1] - 30), width=3, border_radius=20)
        etiqueta = fuente_hud.render(nombre_archivo, True, COLOR_BLANCO)
        img.blit(etiqueta, etiqueta.get_rect(center=(tamano[0] // 2, tamano[1] // 2)))

    cache_sprites[clave] = img
    return img


def color_barra_hp(porcentaje):
    if porcentaje > 0.50:
        return HP_VERDE
    elif porcentaje > 0.22:
        return HP_AMARILLO
    return HP_ROJO


def dibujar_caja_enemigo():
    caja = pygame.Rect(38, 30, 370, 86)
    pygame.draw.rect(pantalla, COLOR_CREMA, caja, border_top_left_radius=14, border_bottom_right_radius=14)
    pygame.draw.rect(pantalla, COLOR_BORDE_OSCURO, caja, width=4, border_top_left_radius=14, border_bottom_right_radius=14)

    nom = fuente_nombre.render(nombre_enemigo, True, COLOR_TEXTO_OSCURO)
    pantalla.blit(nom, (caja.x + 18, caja.y + 10))

    hp_num = max(0, int(round(vida_visual_enemigo)))
    txt_hp = fuente_hud.render(f"HP {hp_num}/{vida_max_enemigo}", True, COLOR_TEXTO_OSCURO)
    pantalla.blit(txt_hp, (caja.right - txt_hp.get_width() - 18, caja.y + 14))

    # Barra HP interpolada
    barra = pygame.Rect(caja.x + 18, caja.y + 48, caja.width - 36, 18)
    pygame.draw.rect(pantalla, COLOR_BORDE_OSCURO, barra, border_radius=6)
    pct = max(0.0, min(1.0, vida_visual_enemigo / vida_max_enemigo))
    if pct > 0:
        relleno = pygame.Rect(barra.x + 3, barra.y + 3, int((barra.width - 6) * pct), barra.height - 6)
        pygame.draw.rect(pantalla, color_barra_hp(pct), relleno, border_radius=4)


def dibujar_caja_jugador():
    caja = pygame.Rect(555, 336, 408, 112)
    pygame.draw.rect(pantalla, COLOR_CREMA, caja, border_top_left_radius=14, border_bottom_right_radius=14)
    pygame.draw.rect(pantalla, COLOR_BORDE_OSCURO, caja, width=4, border_top_left_radius=14, border_bottom_right_radius=14)

    nom = fuente_nombre.render(nombre_jugador, True, COLOR_TEXTO_OSCURO)
    pantalla.blit(nom, (caja.x + 18, caja.y + 8))

    oro = fuente_hud.render(f"Monedas: {dinero}", True, (165, 115, 10))
    pantalla.blit(oro, (caja.right - oro.get_width() - 18, caja.y + 12))

    # Barra HP interpolada
    barra = pygame.Rect(caja.x + 18, caja.y + 42, caja.width - 36, 18)
    pygame.draw.rect(pantalla, COLOR_BORDE_OSCURO, barra, border_radius=6)
    pct = max(0.0, min(1.0, vida_visual_jugador / vida_max_jugador))
    if pct > 0:
        relleno = pygame.Rect(barra.x + 3, barra.y + 3, int((barra.width - 6) * pct), barra.height - 6)
        pygame.draw.rect(pantalla, color_barra_hp(pct), relleno, border_radius=4)

    hp_num = max(0, int(round(vida_visual_jugador)))
    txt_hp = fuente_hud.render(f"Vida: {hp_num} / {vida_max_jugador}", True, COLOR_TEXTO_OSCURO)
    pantalla.blit(txt_hp, (caja.x + 18, caja.y + 66))

    inv = fuente_hud.render("Espada de hierro | Armadura de cuero", True, (85, 92, 105))
    pantalla.blit(inv, (caja.x + 18, caja.y + 86))


def construir_cuadricula_botones(opciones):
    rects = []
    x_inicio = 385
    y_inicio = ALTO_ARENA + 20
    ancho_total = ANCHO - x_inicio - 20
    alto_total = ALTO_CAJA - 40
    sep = 10

    if len(opciones) == 1:
        return [pygame.Rect(x_inicio, y_inicio, ancho_total, alto_total)]

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
    datos = ESCENAS_JUNGLA[id_escena]
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
        if mostrando_resultado:
            cargar_escena(siguiente_escena_pendiente)
        else:
            estado_ui = "ELIGIENDO"
            indice_seleccionado = 0


def confirmar_opcion(indice):
    global paginas_actuales, indice_pagina, letras_visibles, estado_ui
    global mostrando_resultado, siguiente_escena_pendiente
    global vida_jugador, vida_enemigo, vida_visual_jugador, vida_visual_enemigo
    global shake_jugador, shake_enemigo, flash_color, flash_alpha

    opcion = opciones_actuales[indice]

    if opcion.get("reiniciar_combate"):
        vida_jugador = 100
        vida_visual_jugador = 100.0
        vida_enemigo = 100
        vida_visual_enemigo = 100.0

    # Aplicar daños o curación y disparar efectos visuales
    if "dano_enemigo" in opcion:
        vida_enemigo -= opcion["dano_enemigo"]
        shake_enemigo = 0.45
        flash_color = COLOR_BLANCO
        flash_alpha = 110.0

    if "dano_jugador" in opcion:
        vida_jugador -= opcion["dano_jugador"]
        shake_jugador = 0.45
        flash_color = HP_ROJO
        flash_alpha = 125.0

    if "curar_jugador" in opcion:
        vida_jugador += opcion["curar_jugador"]
        flash_color = HP_VERDE
        flash_alpha = 110.0

    # Evaluar si alguien cayó en este turno
    if vida_jugador <= 0:
        siguiente_escena_pendiente = "derrota_jungla"
    elif vida_enemigo <= 0:
        siguiente_escena_pendiente = "victoria_jungla"
    else:
        siguiente_escena_pendiente = opcion["siguiente"]

    paginas_actuales = opcion["resultado"]
    indice_pagina = 0
    letras_visibles = 0.0
    mostrando_resultado = True
    estado_ui = "LEYENDO"


cargar_escena("jungla_1")

# BUCLE PRINCIPAL
while True:
    dt = reloj.tick(FPS) / 1000.0
    tiempo_total += dt
    pos_mouse = pygame.mouse.get_pos()

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

    # Actualizar escritura y suavizado de barras de vida
    if estado_ui == "LEYENDO":
        texto_actual = paginas_actuales[indice_pagina]
        if letras_visibles < len(texto_actual):
            letras_visibles = min(float(len(texto_actual)), letras_visibles + velocidad_texto * dt)

    objetivo_j = max(0.0, float(vida_jugador))
    vida_visual_jugador += (objetivo_j - vida_visual_jugador) * min(1.0, dt * 8.0)

    objetivo_e = max(0.0, float(vida_enemigo))
    vida_visual_enemigo += (objetivo_e - vida_visual_enemigo) * min(1.0, dt * 8.0)

    if shake_jugador > 0:
        shake_jugador = max(0.0, shake_jugador - dt)
    if shake_enemigo > 0:
        shake_enemigo = max(0.0, shake_enemigo - dt)
    if flash_alpha > 0:
        flash_alpha = max(0.0, flash_alpha - 360.0 * dt)

    # DIBUJAR ARENA SUPERIOR
    pygame.draw.rect(pantalla, COLOR_FONDO_ARENA, (0, 0, ANCHO, ALTO_ARENA))
    pygame.draw.rect(pantalla, COLOR_SUELO_ARENA, (0, ALTO_ARENA - 160, ANCHO, 160))

    # Plataformas ovaladas en perspectiva
    pygame.draw.ellipse(pantalla, (26, 36, 50), (585, 255, 290, 62))
    pygame.draw.ellipse(pantalla, (74, 94, 122), (585, 255, 290, 62), 3)

    pygame.draw.ellipse(pantalla, (26, 36, 50), (95, 405, 330, 72))
    pygame.draw.ellipse(pantalla, (74, 94, 122), (95, 405, 330, 72), 3)

    # Sprite Enemigo (arriba derecha) con respiración y sacudida
    sprite_ene_archivo = ESCENAS_JUNGLA[escena_actual]["sprite_enemigo"]
    if sprite_ene_archivo and vida_visual_enemigo > 0.5:
        visible_e = not (shake_enemigo > 0 and int(shake_enemigo * 30) % 2 == 0)
        if visible_e:
            off_y = math.sin(tiempo_total * 3.2) * 4
            off_x = math.sin(shake_enemigo * 55) * 10 if shake_enemigo > 0 else 0
            spr_e = obtener_sprite(sprite_ene_archivo, (210, 210))
            pantalla.blit(spr_e, (625 + off_x, 75 + off_y))

    # Sprite Caballero de espaldas (abajo izquierda)
    if vida_visual_jugador > 0.5:
        visible_j = not (shake_jugador > 0 and int(shake_jugador * 30) % 2 == 0)
        if visible_j:
            off_y_j = math.sin(tiempo_total * 2.6 + 1.0) * 3
            off_x_j = math.sin(shake_jugador * 55) * 12 if shake_jugador > 0 else 0
            spr_j = obtener_sprite("caballero_espalda.png", (230, 230))
            pantalla.blit(spr_j, (145 + off_x_j, 225 + off_y_j))

    # Cajas de estado
    if sprite_ene_archivo:
        dibujar_caja_enemigo()
    dibujar_caja_jugador()

    # Destello de impacto o curación sobre la arena
    if flash_alpha > 0 and flash_color:
        overlay = pygame.Surface((ANCHO, ALTO_ARENA), pygame.SRCALPHA)
        overlay.fill((*flash_color, int(flash_alpha)))
        pantalla.blit(overlay, (0, 0))

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
        caja_izq = pygame.Rect(20, ALTO_ARENA + 20, 350, ALTO_CAJA - 40)
        pygame.draw.rect(pantalla, (20, 28, 42), caja_izq, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_BLANCO, caja_izq, width=2, border_radius=10)
        dibujar_texto_multilinea(
            pantalla, f"¿Qué hará\n{nombre_jugador}?", fuente_prompt, COLOR_BLANCO,
            pygame.Rect(caja_izq.x + 22, caja_izq.y + 45, caja_izq.width - 44, 100)
        )

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