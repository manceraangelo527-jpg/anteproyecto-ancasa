import pygame
import sys
import data
from UI import Interface_User
from levels.Jungla_LV1 import NivelJungla


def main():
	interfaz = Interface_User()
	jugador = data.player
	nivel = NivelJungla(jugador)
	reloj = pygame.time.Clock()
	ejecutando = True

	try:
		while ejecutando:
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT:
					ejecutando = False
				elif evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_1:
						nivel.procesar_eleccion(1)
					elif evento.key == pygame.K_2:
						nivel.procesar_eleccion(2)
					elif evento.key == pygame.K_3:
						nivel.procesar_eleccion(3)

			texto_historia, opciones = nivel.obtener_escena()
			interfaz.draw(texto_historia, opciones, jugador)
			reloj.tick(30)
	finally:
		pygame.quit()


if __name__ == "__main__":
	main()
