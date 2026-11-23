import os
import sys
import math
import pygame

# CONFIGURACIÓN GENERAL Y PALETAS POR ZONA
ANCHO = 1000
ALTO = 700
ALTO_ARENA = 470
ALTO_CAJA = 230
FPS = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# Colores de interfaz estilo RPG
COLOR_CAJA_INFERIOR = (28, 38, 56)
COLOR_BORDE_DORADO = (218, 178, 62)
COLOR_BLANCO = (245, 247, 250)
COLOR_CREMA = (244, 242, 232)
COLOR_SELECCION = (255, 243, 196)
COLOR_TEXTO_OSCURO = (32, 36, 44)
COLOR_BORDE_OSCURO = (42, 48, 60)

HP_VERDE = (56, 200, 96)
HP_AMARILLO = (242, 196, 48)
HP_ROJO = (228, 64, 64)

# Paletas ambientales de respaldo si aún no hay imágenes de fondo
AMBIENTES = {
    "reino": ((36, 44, 68), (54, 66, 98)),
    "jungla": ((26, 54, 42), (40, 82, 60)),
    "pueblo_noche": ((22, 26, 46), (38, 44, 72)),
    "pueblo_dia": ((58, 76, 96), (92, 84, 68)),
    "antartida": ((44, 76, 108), (165, 205, 232)),
}

# GESTOR DE AUDIO (MÚSICA DE FONDO Y EFECTOS DE SONIDO)
class GestorAudio:
    def __init__(self):
        self.activo = False
        self.musica_actual = None
        try:
            pygame.mixer.init()
            self.activo = True
        except pygame.error:
            self.activo = False

    def reproducir_musica(self, archivo, volumen=0.45):
        if not self.activo or not archivo or archivo == self.musica_actual:
            return
        ruta = os.path.join(SND_DIR, archivo)
        if os.path.exists(ruta):
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)
            self.musica_actual = archivo

    def reproducir_efecto(self, archivo, volumen=0.75):
        if not self.activo or not archivo:
            return
        ruta = os.path.join(SND_DIR, archivo)
        if os.path.exists(ruta):
            sonido = pygame.mixer.Sound(ruta)
            sonido.set_volume(volumen)
            sonido.play()

# UTILIDADES GRÁFICAS Y TEXTO MULTILÍNEA
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

# NARRATIVA COMPLETA DEL JUEGO ORIGINAL (3 ACTOS + CHECKPOINTS)
def obtener_escena(id_escena, n, vida, dinero):
    escenas = {
        # -------------------- INTRODUCCIÓN --------------------
        "intro_1": {
            "ambiente": "reino",
            "fondo": "portada_reino.png",
            "solo_cinematica": True,
            "musica": "tema_reino.mp3",
            "paginas": ["bienvenido al primer minijuego de angelo"],
            "opciones": [{"texto": "Comenzar aventura", "siguiente": "pedir_nombre"}],
        },
        "pedir_nombre": {
            "ambiente": "reino",
            "fondo": "portada_reino.png",
            "solo_cinematica": True,
            "musica": "tema_reino.mp3",
            "paginas": ["dame tu nombre:"],
            "pedir_nombre": True,
            "siguiente": "stats_iniciales",
        },
        "stats_iniciales": {
            "ambiente": "reino",
            "fondo": "fondo_reino.png",
            "musica": "tema_reino.mp3",
            "paginas": [
                f"aqui tienes tus estadisticas iniciales\nvida inicial: {vida}  |  dinero: {dinero}\ninventario: espada de hierro, armadura de cuero",
                f"{n} es el mejor caballero de todo el reino",
                "y le asignaron la gran mision... una mision cuyo objetivo es matar al malvado rey de los pinguinos que ha robado la gran esmeralda de la vida",
                f"{n} tiene que ir hasta la antartida para recuperar la joya, pero el camino no sera nada facil, estas listo para jugar??",
            ],
            "opciones": [
                {"texto": "si estoy listo", "efecto": "inicio.wav", "siguiente": "listo_si"},
                {"texto": "no", "siguiente": "listo_no"},
            ],
        },
        "listo_si": {
            "ambiente": "reino",
            "fondo": "fondo_reino.png",
            "paginas": ["perfecto empezemos"],
            "opciones": [{"texto": "Entrar a la jungla", "siguiente": "jungla_1"}],
        },
        "listo_no": {
            "ambiente": "reino",
            "fondo": "portada_reino.png",
            "solo_cinematica": True,
            "paginas": ["esta bien :("],
            "opciones": [{"texto": "Salir del juego", "accion": "salir"}],
        },

        # -------------------- ACTO 1: JUNGLA (CHECKPOINT 1) --------------------
        "jungla_1": {
            "checkpoint": "jungla_1",
            "ambiente": "jungla",
            "fondo": "fondo_jungla.png",
            "sprite_enemigo": "stich_frente.png",
            "musica": "combate_jungla.mp3",
            "enemigo": ("Monstruo Azul", 100),
            "paginas": [
                f"{n} acaba de salir del reino y esta atravesando la jungla de los bambus",
                "se escucha un ruido detras de unos bambus",
                "detras de los bambus aparece un monstruo azul orejon de un metro que empieza a gritar",
                "que haras??",
            ],
            "opciones": [
                {
                    "texto": "atacar",
                    "dano_enemigo": 20,
                    "efecto": "espada.wav",
                    "resultado": [f"{n} ataca al enemigo y le hace daño"],
                    "siguiente": "jungla_2",
                },
                {
                    "texto": "intentar hablar con el",
                    "dano_jugador": 20,
                    "efecto": "mordida.wav",
                    "resultado": [f"{n} intenta hablar con el monstruo, no quiere hablar y le tira a su mini hijo que muerde a {n}"],
                    "siguiente": "jungla_2",
                },
                {
                    "texto": "ignorarlo",
                    "dano_jugador": 100,
                    "efecto": "derrota.wav",
                    "resultado": [f"{n} ignora al monstruo y lo pasa de largo, el monstruo te ataca desde la espalda y te mata"],
                    "siguiente": "jungla_2",
                },
            ],
        },
        "jungla_2": {
            "ambiente": "jungla",
            "fondo": "fondo_jungla.png",
            "sprite_enemigo": "stich_frente.png",
            "paginas": ["cual es tu siguiente movimiento??"],
            "opciones": [
                {
                    "texto": "atacar",
                    "dano_enemigo": 20,
                    "efecto": "espada.wav",
                    "resultado": [f"{n} ataca al monstruo"],
                    "siguiente": "jungla_3",
                },
                {
                    "texto": "curarse",
                    "curar_jugador": 20,
                    "efecto": "curar.wav",
                    "resultado": [f"{n} se cura la vida"],
                    "siguiente": "jungla_3",
                },
                {
                    "texto": "huir",
                    "dano_jugador": 100,
                    "efecto": "derrota.wav",
                    "resultado": [f"{n} intento escapar, el monstruo te ataca desde la espalda y te mata"],
                    "siguiente": "jungla_3",
                },
            ],
        },
        "jungla_3": {
            "ambiente": "jungla",
            "fondo": "fondo_jungla.png",
            "sprite_enemigo": "stich_hijos_frente.png",
            "paginas": ["el monstruo acaba de sacar mas de sus hijos que estan por atacarte, que haras?"],
            "opciones": [
                {
                    "texto": "ignorarlos y contraatacar",
                    "dano_jugador": 30,
                    "efecto": "mordida.wav",
                    "resultado": [f"{n} contraataca pero los mini hijos lo muerden y le hacen heridas"],
                    "siguiente": "jungla_4",
                },
                {
                    "texto": "defenderse",
                    "dano_jugador": 5,
                    "efecto": "escudo.wav",
                    "resultado": [f"{n} se defiende de los mini hijos pero recibe un poco de daño"],
                    "siguiente": "jungla_4",
                },
                {
                    "texto": "atacar a los hijos del monstruo",
                    "dano_enemigo": 10,
                    "efecto": "espada.wav",
                    "resultado": [f"{n} mata a los hijos del monstruo sin recibir daño, el monstruo recibe daño psicologico"],
                    "siguiente": "jungla_4",
                },
            ],
        },
        "jungla_4": {
            "ambiente": "jungla",
            "fondo": "fondo_jungla.png",
            "sprite_enemigo": "stich_frente.png",
            "paginas": ["tienes que hacer una estrategia para derrotar al monstruo, que haras?"],
            "opciones": [
                {
                    "texto": "atacar de frente",
                    "dano_enemigo": 100,
                    "dano_jugador": 10,
                    "efecto": "espada_fuerte.wav",
                    "resultado": [f"{n} ataca de frente y aunque recibe daño mata al enemigo"],
                    "siguiente": "jungla_victoria",
                },
                {
                    "texto": "tirarle comida para que se distraiga",
                    "dano_jugador": 100,
                    "efecto": "derrota.wav",
                    "resultado": [f"{n} le tira comida la cual el monstruo ignora y te mata"],
                    "siguiente": "jungla_victoria",
                },
                {
                    "texto": "meterse detras de los arboles y atacar por sorpresa",
                    "dano_enemigo": 100,
                    "efecto": "espada_fuerte.wav",
                    "resultado": [f"{n} se pone detras de los arboles rodeandolo y lo ataca por la espalda y lo mata"],
                    "siguiente": "jungla_victoria",
                },
            ],
        },
        "jungla_victoria": {
            "limpiar_enemigo": True,
            "ambiente": "jungla",
            "fondo": "fondo_jungla.png",
            "musica": "tema_pueblo.mp3",
            "paginas": [
                f"sigues con tu aventura con {vida} de vida",
                f"inventario: espada de hierro, armadura de cuero  |  monedas: {dinero}",
            ],
            "opciones": [{"texto": "Avanzar hacia el pueblo", "siguiente": "pueblo_1"}],
        },

        # -------------------- ACTO 2: PUEBLO (CHECKPOINT 2) --------------------
        "pueblo_1": {
            "checkpoint": "pueblo_1",
            "ambiente": "pueblo_noche",
            "fondo": "fondo_pueblo_noche.png",
            "sprite_enemigo": "hotel_pueblo.png",
            "musica": "tema_pueblo.mp3",
            "paginas": [
                "para este nivel debes de quedar con al menos 10 monedas",
                f"luego de derrotar al monstruo {n} pasa el bosque y se encuentra con un pueblo por lo que al ser ya casi de noche debe quedarse ahi hasta el amanecer",
                f"{n} se encuentra un hotel que vale 10 monedas, que haras?",
            ],
            "opciones": [
                {
                    "texto": "pagas las 10 monedas y duermes",
                    "curar_jugador": 5,
                    "gastar_dinero": 10,
                    "efecto": "monedas.wav",
                    "resultado": ["duermes en el hotel, descansas y te recuperas"],
                    "siguiente": "pueblo_2",
                },
                {
                    "texto": "no duermes en hotel esta noche",
                    "dano_jugador": 200,
                    "efecto": "derrota.wav",
                    "resultado": ["decidiste no pagar el hotel asi que dormiste en la calle, por lo que a mitad de la noche te robaron y te mataron"],
                    "siguiente": "pueblo_2",
                },
            ],
        },
        "pueblo_2": {
            "ambiente": "pueblo_dia",
            "fondo": "fondo_pueblo_dia.png",
            "sprite_enemigo": "mercados_pueblo.png",
            "paginas": [
                "al amanecer debes ir a comprar comida, a donde compras?",
                f"{n} encuentra 3 mercados, en cual compras?",
            ],
            "opciones": [
                {
                    "texto": "lugar sucio con ratas, pasteles relusientes (8 monedas)",
                    "dano_jugador": 150,
                    "gastar_dinero": 8,
                    "efecto": "veneno.wav",
                    "resultado": ["el pastel y todo lo demás que compraste estaban vencidos, asi que te intoxicaste y moriste"],
                    "siguiente": "llegada_antartida",
                },
                {
                    "texto": "lugar decente acogedor con panes recien horneados (15 monedas)",
                    "gastar_dinero": 15,
                    "efecto": "monedas.wav",
                    "resultado": ["el pan y todo lo demas resulta ser delicioso por lo que sobrevives con eso"],
                    "siguiente": "llegada_antartida",
                },
                {
                    "texto": "lugar muy lujoso y pulcro con deliciosa carne (25 monedas)",
                    "gastar_dinero": 25,
                    "efecto": "monedas.wav",
                    "resultado": ["compraste carne y provisiones que salieron muy bien, aunque gastaste bastante dinero"],
                    "siguiente": "llegada_antartida",
                },
            ],
        },
        "llegada_antartida": {
            "limpiar_enemigo": True,
            "ambiente": "antartida",
            "fondo": "fondo_antartida.png",
            "musica": "jefe_pinguino.mp3",
            "paginas": [f"has llegado a la helada Antártida con {vida} de vida."],
            "opciones": [{"texto": "Entrar al castillo de hielo", "siguiente": "pinguino_1"}],
        },

        # -------------------- ACTO 3: REY PINGÜINO (CHECKPOINT 3) --------------------
        "pinguino_1": {
            "checkpoint": "pinguino_1",
            "ambiente": "antartida",
            "fondo": "fondo_castillo_hielo.png",
            "sprite_enemigo": "rey_pinguino_frente.png",
            "musica": "jefe_pinguino.mp3",
            "enemigo": ("Rey Pingüino", 200),
            "paginas": [
                "Llegas al castillo de hielo. El malvado Rey Pingüino te espera sentado en su trono sosteniendo la Gran Esmeralda de la Vida.",
                "El Rey Pingüino te mira y se ríe burlonamente: 'Jelou, humano tonto, creíste que llegarías lejos? ¡Prepárate a congelarte!'",
                "De repente, el rey te lanza con fuerza un enorme bloque de hielo directo al pecho. ¿Qué haces?",
            ],
            "opciones": [
                {
                    "texto": "Esquivarlo hacia un lado",
                    "efecto": "esquivar.wav",
                    "resultado": [f"{n} da un salto lateral rápido y esquiva el bloque de hielo sin un solo rasguño."],
                    "siguiente": "pinguino_2",
                },
                {
                    "texto": "Intentar cortarlo con la espada de frente",
                    "dano_jugador": 300,
                    "efecto": "hielo.wav",
                    "resultado": [f"{n} intenta cortar el hielo, pero es demasiado pesado y duro; te golpea fuerte y te mata."],
                    "siguiente": "pinguino_2",
                },
                {
                    "texto": "Saltar sobre él",
                    "dano_jugador": 150,
                    "efecto": "hielo.wav",
                    "resultado": [f"{n} saltas que pendejo, el hielo es gigante...moriste."],
                    "siguiente": "pinguino_2",
                },
            ],
        },
        "pinguino_2": {
            "ambiente": "antartida",
            "fondo": "fondo_castillo_hielo.png",
            "sprite_enemigo": "rey_pinguino_frente.png",
            "paginas": [
                "El Rey Pingüino se enoja, se pone furioso y se lanza a toda velocidad a embestirte con su gran panza.",
                "¿Qué haces?",
            ],
            "opciones": [
                {
                    "texto": "Esperar el momento justo para esquivar y hacerle zancadilla",
                    "dano_enemigo": 50,
                    "efecto": "golpe_trono.wav",
                    "resultado": [f"{n} esquiva en el último segundo y le hace una zancadilla, haciendo que el rey se golpee contra el trono."],
                    "siguiente": "pinguino_3",
                },
                {
                    "texto": "Recibir la embestida con los brazos abiertos para bloquearlo",
                    "dano_jugador": 400,
                    "efecto": "derrota.wav",
                    "resultado": [f"{n} intenta bloquearlo pero la fuerza del rey es descomunal, mandándolo a volar contra una pared mueres."],
                    "siguiente": "pinguino_3",
                },
                {
                    "texto": "Agacharte rápidamente",
                    "dano_enemigo": 20,
                    "efecto": "golpe_trono.wav",
                    "resultado": [f"{n} se agacha a tiempo y el rey pasa de largo chocando contra una columna de hielo."],
                    "siguiente": "pinguino_3",
                },
            ],
        },
        "pinguino_3": {
            "ambiente": "antartida",
            "fondo": "fondo_castillo_hielo.png",
            "sprite_enemigo": "rey_pinguino_aturdido.png",
            "paginas": ["El rey pingüino está tambaleándose. Es tu oportunidad de oro para contraatacar."],
            "opciones": [
                {
                    "texto": "Darle un espadazo directo al estómago",
                    "dano_enemigo": 80,
                    "efecto": "espada_fuerte.wav",
                    "resultado": [f"{n} le propina un golpe limpio con su espada de hierro, debilitando enormemente al rey."],
                    "siguiente": "pinguino_4",
                },
                {
                    "texto": "Lanzarle una roca pesada",
                    "dano_enemigo": 40,
                    "efecto": "roca.wav",
                    "resultado": [f"{n} le lanza una roca congelada que lo aturde un buen rato."],
                    "siguiente": "pinguino_4",
                },
                {
                    "texto": "Tratar de quitarle la esmeralda de las manos sin pelear",
                    "dano_jugador": 50,
                    "efecto": "rayo_hielo.wav",
                    "resultado": [f"{n} intenta arrebatar la joya con descuido, pero el rey te lanza un rayo de hielo congelándote el brazo."],
                    "siguiente": "pinguino_4",
                },
            ],
        },
        "pinguino_4": {
            "ambiente": "antartida",
            "fondo": "fondo_castillo_hielo.png",
            "sprite_enemigo": "rey_pinguino_veneno.png",
            "paginas": [
                "Derrotado y agonizando en el suelo, el Rey Pingüino tose y empieza a echar un extraño líquido negro y viscoso por la boca, amenazando con inundar toda la sala del trono con veneno.",
                "¿Qué haces rápido?",
            ],
            "opciones": [
                {
                    "texto": "Corrir a una zona alta de la sala para salvarte y atacar",
                    "fijar_enemigo_vida": 10,
                    "efecto": "espada_fuerte.wav",
                    "resultado": [f"{n} trepa ágilmente a una estatua de hielo, esquivando la inundación tóxica y saltas para rematarlo enterrando tu espada en su garganta."],
                    "siguiente": "pinguino_5",
                },
                {
                    "texto": "Intentar taparle la boca con las manos",
                    "dano_jugador": 600,
                    "efecto": "veneno.wav",
                    "resultado": [f"{n} se arriesga a taparle la boca,grave error moriste."],
                    "siguiente": "pinguino_5",
                },
                {
                    "texto": "Cruzar corriendo el líquido para rematarlo de una vez",
                    "dano_jugador": 300,
                    "efecto": "veneno.wav",
                    "resultado": [f"{n} cruza corriendo el charco ácido sufriendo quemaduras en las botas y piernas mueres ."],
                    "siguiente": "pinguino_5",
                },
            ],
        },
        "pinguino_5": {
            "ambiente": "antartida",
            "fondo": "fondo_castillo_hielo.png",
            "sprite_enemigo": "rey_pinguino_vencido.png",
            "paginas": [
                "El Rey Pingüino yace en el suelo, completamente vencido, piedad en sus pequeños ojos y temblando de frío. A su lado está la brillante Esmeralda de la Vida.",
                "¿Qué decides hacer?",
            ],
            "opciones": [
                {
                    "texto": "Perdonarle la vida, ayudarlo a levantarse y pedirle la esmeralda pacíficamente",
                    "dano_jugador": 200,
                    "efecto": "traicion.wav",
                    "resultado": ["¡Paila! El rey fingía estar débil, te traiciona por la espalda con un cuchillo de hielo y te mata al instante."],
                    "siguiente": "victoria_final",
                },
                {
                    "texto": "Ignorarlo, agarrar la esmeralda e irte del lugar",
                    "dano_jugador": 200,
                    "efecto": "traicion.wav",
                    "resultado": ["Tomas la esmeralda y huyes, pero el rey se recupera y te ataca por la espalda cuando bajas la guardia. ¡Has muerto!"],
                    "siguiente": "victoria_final",
                },
                {
                    "texto": "Rematarlo de una vez por todas con la espada para asegurar el reino",
                    "fijar_enemigo_vida": 0,
                    "efecto": "victoria.wav",
                    "resultado": [f"{n} cumple con su deber de caballero, remata al malvado rey y recupera la Esmeralda de la Vida con éxito total."],
                    "siguiente": "victoria_final",
                },
            ],
        },

        # -------------------- FINAL --------------------
        "victoria_final": {
            "limpiar_enemigo": True,
            "ambiente": "reino",
            "fondo": "cinematica_victoria_final.png",
            "solo_cinematica": True,
            "musica": "fanfarria_victoria.mp3",
            "paginas": [
                f"¡FELICIDADES {n}!",
                "Has derrotado al Rey Pingüino, recuperado la Esmeralda de la Vida y salvado a todo el reino.",
                "Te has convertido en una leyenda viva. ¡Fin del juego!",
            ],
            "opciones": [
                {"texto": "Jugar de nuevo", "accion": "reiniciar"},
                {"texto": "Salir", "accion": "salir"},
            ],
        },
    }
    return escenas[id_escena]

# INICIALIZACIÓN Y ESTADO GLOBAL DEL JUEGO
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Gran Esmeralda de la Vida")
reloj = pygame.time.Clock()
audio = GestorAudio()

fuente_nombre = pygame.font.SysFont("segoeui", 19, bold=True)
fuente_hud = pygame.font.SysFont("segoeui", 15, bold=True)
fuente_narrativa = pygame.font.SysFont("segoeui", 22, bold=True)
fuente_prompt = pygame.font.SysFont("segoeui", 21, bold=True)
fuente_boton = pygame.font.SysFont("segoeui", 16, bold=True)

nombre_jugador = ""
vida_jugador = 100
vida_max_jugador = 100
vida_visual_jugador = 100.0
dinero = 50
checkpoint_actual = "jungla_1"

nombre_enemigo = None
vida_enemigo = 0
vida_max_enemigo = 100
vida_visual_enemigo = 0.0

tiempo_total = 0.0
shake_jugador = 0.0
shake_enemigo = 0.0
flash_color = None
flash_alpha = 0.0
cache_imagenes = {}

escena_actual = "intro_1"
estado_ui = "LEYENDO"          # "LEYENDO", "INGRESANDO_NOMBRE" o "ELIGIENDO"
paginas_actuales = []
indice_pagina = 0
letras_visibles = 0.0
velocidad_texto = 55.0

opciones_actuales = []
botones_rects = []
indice_seleccionado = 0
mostrando_resultado = False
siguiente_escena_pendiente = None


def obtener_imagen(nombre_archivo, tamano, es_sprite=False):
    clave = (nombre_archivo, tamano)
    if clave in cache_imagenes:
        return cache_imagenes[clave]

    ruta = os.path.join(IMG_DIR, nombre_archivo)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.smoothscale(img, tamano)
        cache_imagenes[clave] = img
        return img

    if es_sprite:
        img = pygame.Surface(tamano, pygame.SRCALPHA)
        pygame.draw.rect(img, (48, 62, 88, 230), (15, 15, tamano[0] - 30, tamano[1] - 30), border_radius=20)
        pygame.draw.rect(img, COLOR_BORDE_DORADO, (15, 15, tamano[0] - 30, tamano[1] - 30), width=3, border_radius=20)
        etiqueta = fuente_hud.render(nombre_archivo, True, COLOR_BLANCO)
        img.blit(etiqueta, etiqueta.get_rect(center=(tamano[0] // 2, tamano[1] // 2)))
        cache_imagenes[clave] = img
        return img

    return None


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
    global letras_visibles, opciones_actuales, botones_rects, indice_seleccionado
    global mostrando_resultado, checkpoint_actual
    global nombre_enemigo, vida_enemigo, vida_max_enemigo, vida_visual_enemigo

    escena_actual = id_escena
    datos = obtener_escena(id_escena, nombre_jugador, vida_jugador, dinero)

    if "checkpoint" in datos:
        checkpoint_actual = datos["checkpoint"]

    if "enemigo" in datos:
        nombre_enemigo, hp_e = datos["enemigo"]
        vida_enemigo = hp_e
        vida_max_enemigo = hp_e
        vida_visual_enemigo = float(hp_e)

    if datos.get("limpiar_enemigo"):
        nombre_enemigo = None

    if "musica" in datos:
        audio.reproducir_musica(datos["musica"])

    paginas_actuales = datos["paginas"]
    indice_pagina = 0
    letras_visibles = 0.0
    indice_seleccionado = 0
    mostrando_resultado = False

    if datos.get("pedir_nombre"):
        opciones_actuales = []
        botones_rects = []
        estado_ui = "INGRESANDO_NOMBRE"
    else:
        opciones_actuales = datos["opciones"]
        botones_rects = construir_cuadricula_botones(opciones_actuales)
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
    global mostrando_resultado, siguiente_escena_pendiente, opciones_actuales, botones_rects
    global vida_jugador, vida_max_jugador, vida_visual_jugador, dinero
    global vida_enemigo, shake_jugador, shake_enemigo, flash_color, flash_alpha

    opcion = opciones_actuales[indice]
    accion = opcion.get("accion")

    if accion == "salir":
        pygame.quit()
        sys.exit()
    elif accion == "reiniciar":
        vida_jugador = 100
        vida_max_jugador = 100
        vida_visual_jugador = 100.0
        dinero = 50
        cargar_escena("intro_1")
        return
    elif accion == "reintentar_checkpoint":
        vida_jugador = 100
        vida_max_jugador = 100
        vida_visual_jugador = 100.0
        if checkpoint_actual == "pueblo_1":
            dinero = 50
        cargar_escena(checkpoint_actual)
        return

    if "efecto" in opcion:
        audio.reproducir_efecto(opcion["efecto"])

    if "dano_enemigo" in opcion:
        vida_enemigo -= opcion["dano_enemigo"]
        shake_enemigo = 0.45
        flash_color = COLOR_BLANCO
        flash_alpha = 110.0

    if "fijar_enemigo_vida" in opcion:
        vida_enemigo = opcion["fijar_enemigo_vida"]
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
        vida_max_jugador = max(vida_max_jugador, vida_jugador)
        flash_color = HP_VERDE
        flash_alpha = 110.0

    if "gastar_dinero" in opcion:
        dinero -= opcion["gastar_dinero"]

    if "resultado" in opcion:
        paginas_actuales = opcion["resultado"]
        indice_pagina = 0
        letras_visibles = 0.0
        mostrando_resultado = True
        estado_ui = "LEYENDO"

        # Verificar derrota por vida o por quedarse con menos de 10 monedas en el pueblo
        murio = vida_jugador <= 0
        sin_monedas_pueblo = (escena_actual == "pueblo_2" and dinero <= 9)

        if murio or sin_monedas_pueblo:
            mensajes_cp = {
                "jungla_1": "reintentas desde el checkpoint de la jungla...",
                "pueblo_1": "reintentas desde el checkpoint del pueblo...",
                "pinguino_1": "reintentas desde el checkpoint del castillo del Rey Pingüino...",
            }
            opciones_actuales = [{"texto": mensajes_cp[checkpoint_actual], "accion": "reintentar_checkpoint"}]
            botones_rects = construir_cuadricula_botones(opciones_actuales)
            # Al terminar de leer el mensaje de muerte, desplegar el botón de reintento
            mostrando_resultado = False
        else:
            siguiente_escena_pendiente = opcion["siguiente"]
    else:
        cargar_escena(opcion["siguiente"])

# Arrancar en la portada
cargar_escena("intro_1")

# 6. BUCLE PRINCIPAL (60 FPS)
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

        # MODO INGRESO DE NOMBRE POR TECLADO
        if estado_ui == "INGRESANDO_NOMBRE":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre_jugador.strip():
                    nombre_jugador = nombre_jugador.strip()
                    cargar_escena("stats_iniciales")
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif len(nombre_jugador) < 18 and evento.unicode.isprintable():
                    nombre_jugador += evento.unicode
            continue

        # CLIC CON RATÓN
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_ui == "LEYENDO":
                avanzar_lectura()
            elif estado_ui == "ELIGIENDO":
                for i, rect in enumerate(botones_rects):
                    if rect.collidepoint(evento.pos):
                        confirmar_opcion(i)
                        break

        # CONTROLES DE TECLADO
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

    # Actualizar animación de texto y barras HP
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

    # RENDERIZADO DE ARENA SUPERIOR
    datos_escena = obtener_escena(escena_actual, nombre_jugador, vida_jugador, dinero)
    fondo_img = obtener_imagen(datos_escena.get("fondo", ""), (ANCHO, ALTO_ARENA), es_sprite=False)

    if fondo_img:
        pantalla.blit(fondo_img, (0, 0))
    else:
        cielo, suelo = AMBIENTES[datos_escena.get("ambiente", "reino")]
        pygame.draw.rect(pantalla, cielo, (0, 0, ANCHO, ALTO_ARENA))
        pygame.draw.rect(pantalla, suelo, (0, ALTO_ARENA - 160, ANCHO, 160))

    if not datos_escena.get("solo_cinematica", False):
        pygame.draw.ellipse(pantalla, (26, 36, 50), (585, 255, 290, 62))
        pygame.draw.ellipse(pantalla, (74, 94, 122), (585, 255, 290, 62), 3)

        pygame.draw.ellipse(pantalla, (26, 36, 50), (95, 405, 330, 72))
        pygame.draw.ellipse(pantalla, (74, 94, 122), (95, 405, 330, 72), 3)

        sprite_ene = datos_escena.get("sprite_enemigo")
        if sprite_ene and (nombre_enemigo is None or vida_visual_enemigo > 0.5):
            visible_e = not (shake_enemigo > 0 and int(shake_enemigo * 30) % 2 == 0)
            if visible_e:
                off_y = math.sin(tiempo_total * 3.2) * 4
                off_x = math.sin(shake_enemigo * 55) * 10 if shake_enemigo > 0 else 0
                spr_e = obtener_imagen(sprite_ene, (210, 210), es_sprite=True)
                pantalla.blit(spr_e, (625 + off_x, 75 + off_y))

        if vida_visual_jugador > 0.5:
            visible_j = not (shake_jugador > 0 and int(shake_jugador * 30) % 2 == 0)
            if visible_j:
                off_y_j = math.sin(tiempo_total * 2.6 + 1.0) * 3
                off_x_j = math.sin(shake_jugador * 55) * 12 if shake_jugador > 0 else 0
                spr_j = obtener_imagen("caballero_espalda.png", (230, 230), es_sprite=True)
                pantalla.blit(spr_j, (145 + off_x_j, 225 + off_y_j))

        if nombre_enemigo:
            dibujar_caja_enemigo()
        if nombre_jugador:
            dibujar_caja_jugador()

    if flash_alpha > 0 and flash_color:
        overlay = pygame.Surface((ANCHO, ALTO_ARENA), pygame.SRCALPHA)
        overlay.fill((*flash_color, int(flash_alpha)))
        pantalla.blit(overlay, (0, 0))

    # RENDERIZADO DE CAJA INFERIOR
    pygame.draw.rect(pantalla, COLOR_CAJA_INFERIOR, (0, ALTO_ARENA, ANCHO, ALTO_CAJA))
    pygame.draw.rect(pantalla, COLOR_BORDE_DORADO, (8, ALTO_ARENA + 8, ANCHO - 16, ALTO_CAJA - 16), width=4, border_radius=12)

    if estado_ui == "INGRESANDO_NOMBRE":
        area = pygame.Rect(34, ALTO_ARENA + 28, ANCHO - 68, 50)
        dibujar_texto_multilinea(pantalla, paginas_actuales[0], fuente_narrativa, COLOR_BLANCO, area)

        caja_in = pygame.Rect(34, ALTO_ARENA + 88, 460, 48)
        pygame.draw.rect(pantalla, COLOR_CREMA, caja_in, border_radius=8)
        pygame.draw.rect(pantalla, COLOR_BORDE_DORADO, caja_in, width=3, border_radius=8)
        render_in = fuente_narrativa.render(nombre_jugador + "|", True, COLOR_TEXTO_OSCURO)
        pantalla.blit(render_in, (caja_in.x + 16, caja_in.y + 10))

        pista = fuente_hud.render("Escribe tu nombre y presiona ENTER para continuar", True, COLOR_BORDE_DORADO)
        pantalla.blit(pista, (34, ALTO_ARENA + 152))

    elif estado_ui == "LEYENDO":
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
        nom_caja = nombre_jugador if nombre_jugador else "el caballero"
        dibujar_texto_multilinea(
            pantalla, f"¿Qué hará\n{nom_caja}?", fuente_prompt, COLOR_BLANCO,
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