import os
import math
import pygame
from config import (
    ANCHO, ALTO, ALTO_ARENA, ALTO_CAJA, IMG_DIR,
    BLANCO, CREMA_CAJA, BORDE_OSCURO, BORDE_DORADO,
    PANEL_DIALOGO, BOTON_NORMAL, BOTON_HOVER, TEXTO_OSCURO, GRIS_SUAVE,
    HP_VERDE, HP_AMARILLO, HP_ROJO
)


class BotonPokemon:
    def __init__(self, rect, texto, indice):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.indice = indice

    def dibujar(self, superficie, fuente, seleccionado):
        color_fondo = BOTON_HOVER if seleccionado else BOTON_NORMAL
        color_borde = BORDE_DORADO if seleccionado else BORDE_OSCURO

        pygame.draw.rect(superficie, color_fondo, self.rect, border_radius=8)
        pygame.draw.rect(superficie, color_borde, self.rect, width=3, border_radius=8)

        prefijo = "▶ " if seleccionado else "   "
        etiqueta = f"{prefijo}{self.texto}"
        area = pygame.Rect(self.rect.x + 12, self.rect.y + 8, self.rect.width - 24, self.rect.height - 16)
        dibujar_texto_multilinea(superficie, etiqueta, fuente, TEXTO_OSCURO, area)


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
    alto_linea = fuente.get_linesize()
    for linea in lineas:
        if y + alto_linea > rect.bottom:
            break
        render = fuente.render(linea, True, color)
        superficie.blit(render, (rect.x, y))
        y += alto_linea


class InterfazPokemon:
    def __init__(self):
        self.fuente_nombre = pygame.font.SysFont("segoeui", 19, bold=True)
        self.fuente_hud = pygame.font.SysFont("segoeui", 15, bold=True)
        self.fuente_narrativa = pygame.font.SysFont("segoeui", 22, bold=True)
        self.fuente_prompt = pygame.font.SysFont("segoeui", 21, bold=True)
        self.fuente_opcion = pygame.font.SysFont("segoeui", 16, bold=True)
        self.cache_imagenes = {}

        # Cola de páginas de diálogo
        self.paginas = [""]
        self.indice_pagina = 0
        self.caracteres_visibles = 0.0
        self.velocidad_texto = 55.0

        # Barras de vida suavizadas
        self.vida_jugador_visual = 100.0
        self.vida_enemigo_visual = 100.0

        # Temporizadores de animación
        self.tiempo = 0.0
        self.shake_jugador = 0.0
        self.shake_enemigo = 0.0
        self.flash_color = None
        self.flash_alpha = 0.0

    def iniciar_dialogos(self, lista_paginas):
        self.paginas = lista_paginas if lista_paginas else [""]
        self.indice_pagina = 0
        self.caracteres_visibles = 0.0

    def texto_actual(self):
        return self.paginas[self.indice_pagina]

    def pagina_terminada(self):
        return int(self.caracteres_visibles) >= len(self.texto_actual())

    def en_ultima_pagina(self):
        return self.indice_pagina >= len(self.paginas) - 1

    def avanzar_dialogo(self):
        if not self.pagina_terminada():
            self.caracteres_visibles = float(len(self.texto_actual()))
            return False
        if not self.en_ultima_pagina():
            self.indice_pagina += 1
            self.caracteres_visibles = 0.0
            return False
        return True

    def activar_golpe_jugador(self):
        self.shake_jugador = 0.45
        self.flash_color = HP_ROJO
        self.flash_alpha = 120.0

    def activar_golpe_enemigo(self):
        self.shake_enemigo = 0.45
        self.flash_color = BLANCO
        self.flash_alpha = 110.0

    def activar_curacion(self):
        self.flash_color = HP_VERDE
        self.flash_alpha = 110.0

    def actualizar(self, dt, estado):
        self.tiempo += dt

        texto = self.texto_actual()
        if self.caracteres_visibles < len(texto):
            self.caracteres_visibles = min(
                float(len(texto)),
                self.caracteres_visibles + self.velocidad_texto * dt
            )

        objetivo_j = max(0.0, float(estado["vida"]))
        self.vida_jugador_visual += (objetivo_j - self.vida_jugador_visual) * min(1.0, dt * 8.0)

        objetivo_e = max(0.0, float(estado["enemigo_vida"]))
        self.vida_enemigo_visual += (objetivo_e - self.vida_enemigo_visual) * min(1.0, dt * 8.0)

        if self.shake_jugador > 0:
            self.shake_jugador = max(0.0, self.shake_jugador - dt)
        if self.shake_enemigo > 0:
            self.shake_enemigo = max(0.0, self.shake_enemigo - dt)
        if self.flash_alpha > 0:
            self.flash_alpha = max(0.0, self.flash_alpha - 360.0 * dt)

    def _cargar_imagen(self, nombre_archivo, tamano, es_sprite=False):
        clave = (nombre_archivo, tamano)
        if clave in self.cache_imagenes:
            return self.cache_imagenes[clave]

        ruta = os.path.join(IMG_DIR, nombre_archivo)
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            img = pygame.transform.smoothscale(img, tamano)
        else:
            img = pygame.Surface(tamano, pygame.SRCALPHA)
            if es_sprite:
                pygame.draw.rect(img, (48, 62, 88, 220), (15, 15, tamano[0] - 30, tamano[1] - 30), border_radius=18)
                pygame.draw.rect(img, BORDE_DORADO, (15, 15, tamano[0] - 30, tamano[1] - 30), width=2, border_radius=18)
                txt = self.fuente_hud.render(nombre_archivo, True, BLANCO)
                img.blit(txt, txt.get_rect(center=(tamano[0] // 2, tamano[1] // 2)))
            else:
                img.fill((34, 48, 68))
                pygame.draw.rect(img, (46, 66, 92), (0, ALTO_ARENA - 160, ANCHO, 160))
                txt = self.fuente_hud.render(f"[ Fondo: {nombre_archivo} ]", True, GRIS_SUAVE)
                img.blit(txt, (24, ALTO_ARENA - 34))

        self.cache_imagenes[clave] = img
        return img

    def _color_barra(self, porcentaje):
        if porcentaje > 0.5:
            return HP_VERDE
        elif porcentaje > 0.22:
            return HP_AMARILLO
        return HP_ROJO

    def dibujar(self, pantalla, estado, escena_visual, mostrar_opciones, botones, indice_seleccionado, texto_input=None):
        fondo = self._cargar_imagen(escena_visual["fondo"], (ANCHO, ALTO_ARENA), es_sprite=False)
        pantalla.blit(fondo, (0, 0))

        if not escena_visual.get("solo_cinematica", False):
            # Plataformas ovaladas de batalla
            pygame.draw.ellipse(pantalla, (28, 36, 48), (585, 255, 290, 62))
            pygame.draw.ellipse(pantalla, (70, 86, 110), (585, 255, 290, 62), 3)

            pygame.draw.ellipse(pantalla, (28, 36, 48), (95, 405, 330, 72))
            pygame.draw.ellipse(pantalla, (70, 86, 110), (95, 405, 330, 72), 3)

            # Sprite enemigo (arriba derecha)
            if escena_visual.get("sprite_enemigo"):
                visible_e = not (self.shake_enemigo > 0 and int(self.shake_enemigo * 30) % 2 == 0)
                if visible_e:
                    off_y = math.sin(self.tiempo * 3.2) * 4
                    off_x = math.sin(self.shake_enemigo * 55) * 10 if self.shake_enemigo > 0 else 0
                    spr_e = self._cargar_imagen(escena_visual["sprite_enemigo"], (210, 210), es_sprite=True)
                    pantalla.blit(spr_e, (625 + off_x, 75 + off_y))

            # Sprite jugador (abajo izquierda)
            sprite_j = escena_visual.get("sprite_jugador", "caballero_espalda.png")
            visible_j = not (self.shake_jugador > 0 and int(self.shake_jugador * 30) % 2 == 0)
            if visible_j:
                off_y_j = math.sin(self.tiempo * 2.6 + 1.0) * 3
                off_x_j = math.sin(self.shake_jugador * 55) * 12 if self.shake_jugador > 0 else 0
                spr_j = self._cargar_imagen(sprite_j, (230, 230), es_sprite=True)
                pantalla.blit(spr_j, (145 + off_x_j, 225 + off_y_j))

            if estado["enemigo_nombre"]:
                self._dibujar_caja_enemigo(pantalla, estado)
            if estado["nombre"]:
                self._dibujar_caja_jugador(pantalla, estado)

        if self.flash_alpha > 0 and self.flash_color:
            overlay = pygame.Surface((ANCHO, ALTO_ARENA), pygame.SRCALPHA)
            overlay.fill((*self.flash_color, int(self.flash_alpha)))
            pantalla.blit(overlay, (0, 0))

        self._dibujar_panel_inferior(pantalla, estado, mostrar_opciones, botones, indice_seleccionado, texto_input)

    def _dibujar_caja_enemigo(self, pantalla, estado):
        caja = pygame.Rect(38, 32, 370, 86)
        pygame.draw.rect(pantalla, CREMA_CAJA, caja, border_top_left_radius=14, border_bottom_right_radius=14)
        pygame.draw.rect(pantalla, BORDE_OSCURO, caja, width=4, border_top_left_radius=14, border_bottom_right_radius=14)

        nom = self.fuente_nombre.render(estado["enemigo_nombre"], True, TEXTO_OSCURO)
        pantalla.blit(nom, (caja.x + 18, caja.y + 10))

        hp_actual = int(round(self.vida_enemigo_visual))
        hp_max = estado["enemigo_vida_max"]
        txt_hp = self.fuente_hud.render(f"HP {hp_actual}/{hp_max}", True, TEXTO_OSCURO)
        pantalla.blit(txt_hp, (caja.right - txt_hp.get_width() - 18, caja.y + 14))

        barra = pygame.Rect(caja.x + 18, caja.y + 48, caja.width - 36, 18)
        pygame.draw.rect(pantalla, BORDE_OSCURO, barra, border_radius=6)
        pct = max(0.0, min(1.0, self.vida_enemigo_visual / hp_max))
        if pct > 0:
            relleno = pygame.Rect(barra.x + 3, barra.y + 3, int((barra.width - 6) * pct), barra.height - 6)
            pygame.draw.rect(pantalla, self._color_barra(pct), relleno, border_radius=4)

    def _dibujar_caja_jugador(self, pantalla, estado):
        caja = pygame.Rect(555, 336, 408, 112)
        pygame.draw.rect(pantalla, CREMA_CAJA, caja, border_top_left_radius=14, border_bottom_right_radius=14)
        pygame.draw.rect(pantalla, BORDE_OSCURO, caja, width=4, border_top_left_radius=14, border_bottom_right_radius=14)

        nom = self.fuente_nombre.render(estado["nombre"], True, TEXTO_OSCURO)
        pantalla.blit(nom, (caja.x + 18, caja.y + 8))

        oro = self.fuente_hud.render(f"Monedas: {estado['dinero']}", True, (165, 115, 10))
        pantalla.blit(oro, (caja.right - oro.get_width() - 18, caja.y + 12))

        barra = pygame.Rect(caja.x + 18, caja.y + 42, caja.width - 36, 18)
        pygame.draw.rect(pantalla, BORDE_OSCURO, barra, border_radius=6)
        hp_max = estado["vida_max"]
        pct = max(0.0, min(1.0, self.vida_jugador_visual / hp_max))
        if pct > 0:
            relleno = pygame.Rect(barra.x + 3, barra.y + 3, int((barra.width - 6) * pct), barra.height - 6)
            pygame.draw.rect(pantalla, self._color_barra(pct), relleno, border_radius=4)

        hp_num = int(round(self.vida_jugador_visual))
        txt_hp = self.fuente_hud.render(f"Vida: {hp_num} / {hp_max}", True, TEXTO_OSCURO)
        pantalla.blit(txt_hp, (caja.x + 18, caja.y + 66))

        inv_txt = self.fuente_hud.render("Espada de hierro | Armadura de cuero", True, (85, 92, 105))
        pantalla.blit(inv_txt, (caja.x + 18, caja.y + 86))

    def _dibujar_panel_inferior(self, pantalla, estado, mostrar_opciones, botones, indice_seleccionado, texto_input):
        panel = pygame.Rect(0, ALTO_ARENA, ANCHO, ALTO_CAJA)
        pygame.draw.rect(pantalla, PANEL_DIALOGO, panel)
        pygame.draw.rect(pantalla, BORDE_DORADO, (8, ALTO_ARENA + 8, ANCHO - 16, ALTO_CAJA - 16), width=4, border_radius=12)

        if texto_input is not None:
            area = pygame.Rect(34, ALTO_ARENA + 28, ANCHO - 68, 60)
            dibujar_texto_multilinea(pantalla, self.texto_actual(), self.fuente_narrativa, BLANCO, area)

            caja_in = pygame.Rect(34, ALTO_ARENA + 95, 460, 48)
            pygame.draw.rect(pantalla, CREMA_CAJA, caja_in, border_radius=8)
            pygame.draw.rect(pantalla, BORDE_DORADO, caja_in, width=3, border_radius=8)
            render_in = self.fuente_narrativa.render(texto_input + "|", True, TEXTO_OSCURO)
            pantalla.blit(render_in, (caja_in.x + 16, caja_in.y + 10))

            pista = self.fuente_hud.render("Escribe tu nombre y presiona ENTER", True, BORDE_DORADO)
            pantalla.blit(pista, (34, ALTO_ARENA + 158))
            return

        if mostrar_opciones:
            caja_izq = pygame.Rect(20, ALTO_ARENA + 20, 350, ALTO_CAJA - 40)
            pygame.draw.rect(pantalla, (20, 28, 42), caja_izq, border_radius=10)
            pygame.draw.rect(pantalla, BLANCO, caja_izq, width=2, border_radius=10)

            nombre = estado["nombre"] if estado["nombre"] else "el caballero"
            pregunta = f"¿Qué hará\n{nombre}?"
            dibujar_texto_multilinea(
                pantalla, pregunta, self.fuente_prompt, BLANCO,
                pygame.Rect(caja_izq.x + 22, caja_izq.y + 42, caja_izq.width - 44, caja_izq.height - 60)
            )

            for i, boton in enumerate(botones):
                boton.dibujar(pantalla, self.fuente_opcion, i == indice_seleccionado)
            return

        texto_parcial = self.texto_actual()[:int(self.caracteres_visibles)]
        area_texto = pygame.Rect(34, ALTO_ARENA + 28, ANCHO - 68, ALTO_CAJA - 68)
        dibujar_texto_multilinea(pantalla, texto_parcial, self.fuente_narrativa, BLANCO, area_texto)

        if self.pagina_terminada() and int(self.tiempo * 3) % 2 == 0:
            flecha = self.fuente_narrativa.render("▼  [Clic / Espacio]", True, BORDE_DORADO)
            pantalla.blit(flecha, (ANCHO - flecha.get_width() - 32, ALTO - 46))