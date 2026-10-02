class NivelJungla:
	def __init__(self, jugador):
		self.jugador = jugador
		self.vida_stich = 100
		self.paso = 1
		self.completado = False
		self.game_over = False
		self.mensaje_resultado = ""

	def obtener_escena(self):
		nombre = self.jugador["name"]

		if self.game_over:
			texto = (
				"¡HAS MUERTO!\n"
				f"{self.mensaje_resultado}\n"
				"Presiona 1 para reiniciar desde el checkpoint."
			)
			return texto, ["1. Reintentar desde el checkpoint"]

		if self.completado:
			texto = (
				f"¡Felicidades, {nombre}! Derrotaste al monstruo de la jungla.\n"
				f"{self.mensaje_resultado}\n"
				"Presiona 1 para continuar hacia el Pueblo."
			)
			return texto, ["1. Avanzar al siguiente nivel"]

		if self.paso == 1:
			texto = (
				f"{nombre} sale del reino y atraviesa la jungla de bambús.\n"
				"Escuchas un ruido y aparece un monstruo azul orejón de un metro (Stitch).\n"
				"¿Qué harás?"
			)
			opciones = ["1. Atacar", "2. Intentar hablar con él", "3. Ignorarlo"]
		elif self.paso == 2:
			texto = (
				f"Vida de Stitch: {self.vida_stich} HP\n"
				"¿Cuál es tu siguiente movimiento?"
			)
			opciones = ["1. Atacar", "2. Curarse (+20 HP)", "3. Huir"]
		elif self.paso == 3:
			texto = (
				f"Vida de Stitch: {self.vida_stich} HP\n"
				"El monstruo acaba de sacar más de sus hijos que están por atacarte. ¿Qué harás?"
			)
			opciones = [
				"1. Ignorarlos y contraatacar",
				"2. Defenderse",
				"3. Atacar a los hijos del monstruo",
			]
		else:
			texto = (
				f"Vida de Stitch: {self.vida_stich} HP\n"
				"Tienes que hacer una estrategia para derrotar al monstruo. ¿Qué harás?"
			)
			opciones = [
				"1. Atacar de frente",
				"2. Tirarle comida para distraerlo",
				"3. Atacar por sorpresa desde los árboles",
			]

		if self.mensaje_resultado:
			texto = f"{self.mensaje_resultado}\n{texto}"
		return texto, opciones

	def procesar_eleccion(self, opcion):
		nombre = self.jugador["name"]

		if self.game_over:
			if opcion == 1:
				self.jugador["life"] = 100
				self.vida_stich = 100
				self.paso = 1
				self.game_over = False
				self.mensaje_resultado = "Has reintentado la batalla."
			return

		if self.completado:
			return

		if self.paso == 1:
			if opcion == 1:
				self.vida_stich -= 20
				self.mensaje_resultado = f"{nombre} ataca al enemigo y le hace daño."
				self.paso = 2
			elif opcion == 2:
				self.jugador["life"] -= 20
				self.mensaje_resultado = (
					f"{nombre} intenta hablar, pero el monstruo le tira a su mini hijo que lo muerde."
				)
				self.paso = 2
			elif opcion == 3:
				self.jugador["life"] -= 100
				self.mensaje_resultado = (
					f"{nombre} ignora al monstruo. Te ataca por la espalda y te mata."
				)

		elif self.paso == 2:
			if opcion == 1:
				self.vida_stich -= 20
				self.mensaje_resultado = f"{nombre} ataca al monstruo."
				self.paso = 3
			elif opcion == 2:
				self.jugador["life"] += 20
				self.mensaje_resultado = f"{nombre} se cura la vida (+20 HP)."
				self.paso = 3
			elif opcion == 3:
				self.jugador["life"] -= 100
				self.mensaje_resultado = (
					f"{nombre} intentó escapar, pero el monstruo lo atacó por la espalda y lo mató."
				)

		elif self.paso == 3:
			if opcion == 1:
				self.jugador["life"] -= 30
				self.mensaje_resultado = (
					f"{nombre} contraataca, pero los mini hijos lo muerden y le hacen heridas."
				)
				self.paso = 4
			elif opcion == 2:
				self.jugador["life"] -= 5
				self.mensaje_resultado = (
					f"{nombre} se defiende de los mini hijos pero recibe un poco de daño."
				)
				self.paso = 4
			elif opcion == 3:
				self.vida_stich -= 10
				self.mensaje_resultado = (
					f"{nombre} mata a los hijos del monstruo sin recibir daño. "
					"Stitch recibe daño psicológico."
				)
				self.paso = 4

		elif self.paso == 4:
			if opcion == 1:
				self.vida_stich -= 100
				self.jugador["life"] -= 10
				self.mensaje_resultado = (
					f"{nombre} ataca de frente y, aunque recibe daño, mata al enemigo."
				)
			elif opcion == 2:
				self.jugador["life"] -= 100
				self.mensaje_resultado = (
					f"{nombre} le tira comida, la cual el monstruo ignora y te mata."
				)
			elif opcion == 3:
				self.vida_stich -= 100
				self.mensaje_resultado = (
					f"{nombre} se pone detrás de los árboles y ataca por la espalda al monstruo, matándolo."
				)

		if self.jugador["life"] <= 0:
			self.game_over = True
		elif self.vida_stich <= 0:
			self.completado = True
			self.jugador["checkpoint"] = "Pueblo"
