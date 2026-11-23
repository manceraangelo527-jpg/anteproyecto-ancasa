import sys
import pygame
from config import ANCHO, ALTO, ALTO_ARENA, ALTO_CAJA, FPS
from audio import GestorAudio
from ui import InterfazPokemon, BotonPokemon
from historia import crear_estado_inicial, obtener_escena


class JuegoPokemon:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("La Gran Esmeralda de la Vida")
        self.reloj = pygame.time.Clock()

        self.ui = InterfazPokemon()
        self.audio = GestorAudio()
        self.estado = crear_estado_inicial()

        self.escena_actual_id = "intro_1"
        self.escena_visual = {}
        self.opciones_actuales = []
        self.botones = []
        self.indice_seleccionado = 0
        self.mostrar_opciones = False
        self.input_nombre = None

        self.cargar_escena("intro_1")

    def cargar_escena(self, id_escena):
        self.escena_actual_id = id_escena
        self.mostrar_opciones = False
        self.indice_seleccionado = 0
        datos = obtener_escena(id_escena, self.estado)

        if "checkpoint" in datos:
            self.estado["checkpoint"] = datos["checkpoint"]

        if "enemigo" in datos:
            nom_e, v_e, max_e = datos["enemigo"]
            self.estado["enemigo_nombre"] = nom_e
            self.estado["enemigo_vida"] = v_e
            self.estado["enemigo_vida_max"] = max_e
            self.ui.vida_enemigo_visual = float(v_e)

        if datos.get("limpiar_enemigo"):
            self.estado["enemigo_nombre"] = None

        self.escena_visual = {
            "fondo": datos.get("fondo", "portada_reino.png"),
            "sprite_jugador": datos.get("sprite_jugador", "caballero_espalda.png"),
            "sprite_enemigo": datos.get("sprite_enemigo"),
            "solo_cinematica": datos.get("solo_cinematica", False),
        }

        if "musica" in datos:
            self.audio.reproducir_musica(datos["musica"])

        self.ui.iniciar_dialogos(datos["paginas"])

        if datos.get("pedir_nombre"):
            self.input_nombre = ""
            self.opciones_actuales = []
            self.botones = []
        else:
            self.input_nombre = None
            self.opciones_actuales = datos["opciones"]
            self.botones = self._construir_grid_botones(self.opciones_actuales)

    def _construir_grid_botones(self, opciones):
        botones = []
        x_inicio = 385
        y_inicio = ALTO_ARENA + 20
        ancho_total = ANCHO - x_inicio - 20
        alto_total = ALTO_CAJA - 40
        sep = 10

        if len(opciones) == 1:
            rect = (x_inicio, y_inicio, ancho_total, alto_total)
            return [BotonPokemon(rect, opciones[0]["texto"], 0)]

        ancho_btn = (ancho_total - sep) // 2
        alto_btn = (alto_total - sep) // 2

        for i, op in enumerate(opciones):
            col = i % 2
            fila = i // 2
            rect = (
                x_inicio + col * (ancho_btn + sep),
                y_inicio + fila * (alto_btn + sep),
                ancho_btn,
                alto_btn
            )
            botones.append(BotonPokemon(rect, op["texto"], i))
        return botones

    def procesar_opcion(self, indice):
        opcion = self.opciones_actuales[indice]
        self.mostrar_opciones = False
        self.indice_seleccionado = 0

        accion = opcion.get("accion")
        if accion == "salir":
            pygame.quit()
            sys.exit()
        elif accion == "reiniciar":
            self.estado = crear_estado_inicial()
            self.ui.vida_jugador_visual = 100.0
            self.cargar_escena("intro_1")
            return
        elif accion == "reintentar_checkpoint":
            cp = self.estado["checkpoint"]
            self.estado["vida"] = 100
            self.ui.vida_jugador_visual = 100.0
            if cp == "pueblo_1":
                self.estado["dinero"] = 50
            self.cargar_escena(cp)
            return

        if "efecto" in opcion:
            self.audio.reproducir_efecto(opcion["efecto"])

        if "dano_jugador" in opcion:
            self.estado["vida"] -= opcion["dano_jugador"]
            self.ui.activar_golpe_jugador()

        if "curar_jugador" in opcion:
            self.estado["vida"] += opcion["curar_jugador"]
            self.ui.activar_curacion()

        if "dano_enemigo" in opcion:
            self.estado["enemigo_vida"] -= opcion["dano_enemigo"]
            self.ui.activar_golpe_enemigo()

        if "fijar_enemigo_vida" in opcion:
            self.estado["enemigo_vida"] = opcion["fijar_enemigo_vida"]
            self.ui.activar_golpe_enemigo()

        if "gastar_dinero" in opcion:
            self.estado["dinero"] -= opcion["gastar_dinero"]

        if "res_paginas" in opcion:
            self.ui.iniciar_dialogos(opcion["res_paginas"])

            murio = self.estado["vida"] <= 0
            sin_monedas_pueblo = (self.escena_actual_id == "pueblo_2" and self.estado["dinero"] <= 9)

            if murio or sin_monedas_pueblo:
                cp = self.estado["checkpoint"]
                etiquetas_cp = {
                    "jungla_1": "Reintentar checkpoint de la jungla",
                    "pueblo_1": "Reintentar checkpoint del pueblo",
                    "pinguino_1": "Reintentar checkpoint del castillo"
                }
                self.opciones_actuales = [{"texto": etiquetas_cp[cp], "accion": "reintentar_checkpoint"}]
            else:
                self.opciones_actuales = [{"texto": "Continuar", "siguiente": opcion["siguiente"]}]

            self.botones = self._construir_grid_botones(self.opciones_actuales)
        else:
            self.cargar_escena(opcion["siguiente"])

    def _avanzar_interaccion(self):
        if not self.mostrar_opciones:
            terminado = self.ui.avanzar_dialogo()
            if terminado:
                self.mostrar_opciones = True
                self.indice_seleccionado = 0

    def ejecutar(self):
        while True:
            dt = self.reloj.tick(FPS) / 1000.0
            pos_mouse = pygame.mouse.get_pos()

            if self.mostrar_opciones:
                for i, boton in enumerate(self.botones):
                    if boton.rect.collidepoint(pos_mouse):
                        self.indice_seleccionado = i

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.input_nombre is not None:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN and self.input_nombre.strip():
                            self.estado["nombre"] = self.input_nombre.strip()
                            self.cargar_escena("stats_iniciales")
                        elif evento.key == pygame.K_BACKSPACE:
                            self.input_nombre = self.input_nombre[:-1]
                        elif len(self.input_nombre) < 20 and evento.unicode.isprintable():
                            self.input_nombre += evento.unicode
                    continue

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if not self.mostrar_opciones:
                        self._avanzar_interaccion()
                    else:
                        for i, boton in enumerate(self.botones):
                            if boton.rect.collidepoint(evento.pos):
                                self.procesar_opcion(i)
                                break

                if evento.type == pygame.KEYDOWN:
                    if not self.mostrar_opciones:
                        if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self._avanzar_interaccion()
                    else:
                        total = len(self.botones)
                        if evento.key in (pygame.K_RIGHT, pygame.K_DOWN):
                            self.indice_seleccionado = (self.indice_seleccionado + 1) % total
                        elif evento.key in (pygame.K_LEFT, pygame.K_UP):
                            self.indice_seleccionado = (self.indice_seleccionado - 1) % total
                        elif evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.procesar_opcion(self.indice_seleccionado)
                        elif evento.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                            idx = evento.key - pygame.K_1
                            if idx < total:
                                self.procesar_opcion(idx)

            self.ui.actualizar(dt, self.estado)
            self.ui.dibujar(
                self.pantalla,
                self.estado,
                self.escena_visual,
                self.mostrar_opciones,
                self.botones,
                self.indice_seleccionado,
                self.input_nombre
            )
            pygame.display.flip()


if __name__ == "__main__":
    JuegoPokemon().ejecutar()