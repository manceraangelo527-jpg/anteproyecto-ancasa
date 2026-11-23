import os

# Dimensiones de ventana y pantalla dividida
ANCHO = 1000
ALTO = 700
ALTO_ARENA = 470
ALTO_CAJA = 230
FPS = 60

# Rutas de recursos multimedia
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# Paleta estilo RPG / Batalla Pokémon
NEGRO = (24, 28, 36)
BLANCO = (248, 250, 252)
CREMA_CAJA = (244, 242, 232)
BORDE_OSCURO = (42, 48, 60)
BORDE_DORADO = (218, 178, 62)
PANEL_DIALOGO = (28, 38, 56)
BOTON_NORMAL = (244, 242, 232)
BOTON_HOVER = (255, 243, 196)
TEXTO_OSCURO = (32, 36, 44)
GRIS_SUAVE = (160, 168, 180)

# Colores de barras de vida
HP_VERDE = (56, 200, 96)
HP_AMARILLO = (242, 196, 48)
HP_ROJO = (228, 64, 64)