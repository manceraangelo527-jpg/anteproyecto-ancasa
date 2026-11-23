def crear_estado_inicial():
    return {
        "nombre": "",
        "vida": 100,
        "vida_max": 100,
        "dinero": 50,
        "inventario": ["espada de hierro", "armadura de cuero"],
        "checkpoint": "jungla_1",
        "enemigo_nombre": None,
        "enemigo_vida": 0,
        "enemigo_vida_max": 100,
    }


def obtener_escena(id_escena, estado):
    n = estado["nombre"]

    escenas = {
        # ================= INTRODUCCIÓN =================
        "intro_1": {
            "fondo": "portada_reino.png",
            "solo_cinematica": True,
            "musica": "tema_reino.mp3",
            "paginas": ["bienvenido al primer minijuego de ANCASA"],
            "opciones": [{"texto": "Comenzar aventura", "siguiente": "pedir_nombre"}]
        },
        "pedir_nombre": {
            "fondo": "portada_reino.png",
            "solo_cinematica": True,
            "musica": "tema_reino.mp3",
            "paginas": ["dame tu nombre:"],
            "pedir_nombre": True,
            "siguiente": "stats_iniciales"
        },
        "stats_iniciales": {
            "fondo": "fondo_reino.png",
            "sprite_jugador": "caballero_espalda.png",
            "musica": "tema_reino.mp3",
            "paginas": [
                f"aqui tienes tus estadisticas iniciales:\nvida inicial: {estado['vida']} | dinero: {estado['dinero']}\ninventario: espada de hierro, armadura de cuero",
                f"{n} es el mejor caballero de todo el reino",
                "y le asignaron la gran mision... una mision cuyo objetivo es matar al malvado rey de los pinguinos que ha robado la gran esmeralda de la vida",
                f"{n} tiene que ir hasta la antartida para recuperar la joya, pero el camino no sera nada facil, estas listo para jugar??"
            ],
            "opciones": [
                {"texto": "si estoy listo", "siguiente": "listo_si", "efecto": "inicio_aventura.wav"},
                {"texto": "no", "siguiente": "listo_no"}
            ]
        },
        "listo_si": {
            "fondo": "fondo_reino.png",
            "sprite_jugador": "caballero_espalda.png",
            "paginas": ["perfecto empezemos"],
            "opciones": [{"texto": "Ir a la jungla", "siguiente": "jungla_1"}]
        },
        "listo_no": {
            "fondo": "portada_reino.png",
            "solo_cinematica": True,
            "paginas": ["esta bien :("],
            "opciones": [{"texto": "Salir del juego", "accion": "salir"}]
        },

        # ================= CHECKPOINT 1: JUNGLA (STICH) =================
        "jungla_1": {
            "checkpoint": "jungla_1",
            "fondo": "fondo_jungla.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "stich_frente.png",
            "musica": "combate_jungla.mp3",
            "enemigo": ("Monstruo Azul", 100, 100),
            "paginas": [
                f"{n} acaba de salir del reino y esta atravesando la jungla de los bambus",
                "se escucha un ruido detras de unos bambus...",
                "detras de los bambus aparece un monstruo azul orejon de un metro que empieza a gritar",
                "que haras??"
            ],
            "opciones": [
                {
                    "texto": "atacar",
                    "dano_enemigo": 20,
                    "efecto": "espada.wav",
                    "res_paginas": [f"{n} ataca al enemigo y le hace daño"],
                    "siguiente": "jungla_2"
                },
                {
                    "texto": "intentar hablar con el",
                    "dano_jugador": 20,
                    "efecto": "mordida.wav",
                    "res_paginas": [f"{n} intenta hablar con el monstruo, no quiere hablar y le tira a su mini hijo que muerde a {n}"],
                    "siguiente": "jungla_2"
                },
                {
                    "texto": "ignorarlo",
                    "dano_jugador": 100,
                    "efecto": "derrota.wav",
                    "res_paginas": [f"{n} ignora al monstruo y lo pasa de largo, el monstruo te ataca desde la espalda y te mata"],
                    "siguiente": "jungla_2"
                }
            ]
        },
        "jungla_2": {
            "fondo": "fondo_jungla.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "stich_frente.png",
            "paginas": ["cual es tu siguiente movimiento??"],
            "opciones": [
                {
                    "texto": "atacar",
                    "dano_enemigo": 20,
                    "efecto": "espada.wav",
                    "res_paginas": [f"{n} ataca al monstruo"],
                    "siguiente": "jungla_3"
                },
                {
                    "texto": "curarse",
                    "curar_jugador": 20,
                    "efecto": "curar.wav",
                    "res_paginas": [f"{n} se cura la vida"],
                    "siguiente": "jungla_3"
                },
                {
                    "texto": "huir",
                    "dano_jugador": 100,
                    "efecto": "derrota.wav",
                    "res_paginas": [f"{n} intento escapar, el monstruo te ataca desde la espalda y te mata"],
                    "siguiente": "jungla_3"
                }
            ]
        },
        "jungla_3": {
            "fondo": "fondo_jungla.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "stich_hijos_frente.png",
            "paginas": ["el monstruo acaba de sacar mas de sus hijos que estan por atacarte, que haras?"],
            "opciones": [
                {
                    "texto": "ignorarlos y contraatacar",
                    "dano_jugador": 30,
                    "efecto": "mordida.wav",
                    "res_paginas": [f"{n} contraataca pero los mini hijos lo muerden y le hacen heridas"],
                    "siguiente": "jungla_4"
                },
                {
                    "texto": "defenderse",
                    "dano_jugador": 5,
                    "efecto": "escudo.wav",
                    "res_paginas": [f"{n} se defiende de los mini hijos pero recibe un poco de daño"],
                    "siguiente": "jungla_4"
                },
                {
                    "texto": "atacar a los hijos del monstruo",
                    "dano_enemigo": 10,
                    "efecto": "espada.wav",
                    "res_paginas": [f"{n} mata a los hijos del monstruo sin recibir daño, el monstruo recibe daño psicologico"],
                    "siguiente": "jungla_4"
                }
            ]
        },
        "jungla_4": {
            "fondo": "fondo_jungla.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "stich_frente.png",
            "paginas": ["tienes que hacer una estrategia para derrotar al monstruo, que haras?"],
            "opciones": [
                {
                    "texto": "atacar de frente",
                    "dano_enemigo": 100,
                    "dano_jugador": 10,
                    "efecto": "espada_fuerte.wav",
                    "res_paginas": [f"{n} ataca de frente y aunque recibe daño mata al enemigo"],
                    "siguiente": "jungla_victoria"
                },
                {
                    "texto": "tirarle comida para que se distraiga",
                    "dano_jugador": 100,
                    "efecto": "derrota.wav",
                    "res_paginas": [f"{n} le tira comida la cual el monstruo ignora y te mata"],
                    "siguiente": "jungla_victoria"
                },
                {
                    "texto": "meterse detras de los arboles y atacar por sorpresa",
                    "dano_enemigo": 100,
                    "efecto": "espada_fuerte.wav",
                    "res_paginas": [f"{n} se pone detras de los arboles rodeandolo y lo ataca por la espalda y lo mata"],
                    "siguiente": "jungla_victoria"
                }
            ]
        },
        "jungla_victoria": {
            "limpiar_enemigo": True,
            "fondo": "fondo_jungla.png",
            "sprite_jugador": "caballero_espalda.png",
            "musica": "tema_pueblo.mp3",
            "paginas": [
                f"sigues con tu aventura con {estado['vida']} de vida",
                f"inventario: espada de hierro, armadura de cuero | monedas: {estado['dinero']}"
            ],
            "opciones": [{"texto": "Seguir al pueblo", "siguiente": "pueblo_1"}]
        },

        # ================= CHECKPOINT 2: PUEBLO =================
        "pueblo_1": {
            "checkpoint": "pueblo_1",
            "fondo": "fondo_pueblo_noche.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "posadero_frente.png",
            "musica": "tema_pueblo.mp3",
            "paginas": [
                "para este nivel debes de quedar con al menos 10 monedas",
                f"luego de derrotar al monstruo {n} pasa el bosque y se encuentra con un pueblo por lo que al ser ya casi de noche debe quedarse ahi hasta el amanecer",
                f"{n} se encuentra un hotel que vale 10 monedas, que haras?"
            ],
            "opciones": [
                {
                    "texto": "pagas las 10 monedas y duermes",
                    "curar_jugador": 5,
                    "gastar_dinero": 10,
                    "efecto": "monedas.wav",
                    "res_paginas": ["duermes en el hotel, descansas y te recuperas"],
                    "siguiente": "pueblo_2"
                },
                {
                    "texto": "no duermes en hotel esta noche",
                    "dano_jugador": 200,
                    "efecto": "derrota.wav",
                    "res_paginas": ["decidiste no pagar el hotel asi que dormiste en la calle, por lo que a mitad de la noche te robaron y te mataron"],
                    "siguiente": "pueblo_2"
                }
            ]
        },
        "pueblo_2": {
            "fondo": "fondo_pueblo_dia.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "mercados_frente.png",
            "paginas": [
                "al amanecer debes ir a comprar comida, a donde compras?",
                f"{n} encuentra 3 mercados, en cual compras?"
            ],
            "opciones": [
                {
                    "texto": "lugar sucio con ratas, pasteles relusientes (8 monedas)",
                    "dano_jugador": 150,
                    "gastar_dinero": 8,
                    "efecto": "veneno.wav",
                    "res_paginas": ["el pastel y todo lo demás que compraste estaban vencidos, asi que te intoxicaste y moriste"],
                    "siguiente": "llegada_antartida"
                },
                {
                    "texto": "lugar decente con panes recien horneados (15 monedas)",
                    "gastar_dinero": 15,
                    "efecto": "monedas.wav",
                    "res_paginas": ["el pan y todo lo demas resulta ser delicioso por lo que sobrevives con eso"],
                    "siguiente": "llegada_antartida"
                },
                {
                    "texto": "lugar muy lujoso con deliciosa carne (25 monedas)",
                    "gastar_dinero": 25,
                    "efecto": "monedas.wav",
                    "res_paginas": ["compraste carne y provisiones que salieron muy bien, aunque gastaste bastante dinero"],
                    "siguiente": "llegada_antartida"
                }
            ]
        },
        "llegada_antartida": {
            "fondo": "fondo_antartida.png",
            "sprite_jugador": "caballero_espalda.png",
            "musica": "jefe_pinguino.mp3",
            "paginas": [f"has llegado a la helada Antártida con {estado['vida']} de vida."],
            "opciones": [{"texto": "Entrar al castillo", "siguiente": "pinguino_1"}]
        },

        # ================= CHECKPOINT 3: REY PINGÜINO =================
        "pinguino_1": {
            "checkpoint": "pinguino_1",
            "fondo": "fondo_castillo_hielo.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "rey_pinguino_frente.png",
            "musica": "jefe_pinguino.mp3",
            "enemigo": ("Rey Pingüino", 200, 200),
            "paginas": [
                "Llegas al castillo de hielo. El malvado Rey Pingüino te espera sentado en su trono sosteniendo la Gran Esmeralda de la Vida.",
                "El Rey Pingüino te mira y se ríe burlonamente: 'Jelou, humano tonto, creíste que llegarías lejos? ¡Prepárate a congelarte!'",
                "De repente, el rey te lanza con fuerza un enorme bloque de hielo directo al pecho. ¿Qué haces?"
            ],
            "opciones": [
                {
                    "texto": "Esquivarlo hacia un lado",
                    "efecto": "esquivar.wav",
                    "res_paginas": [f"{n} da un salto lateral rápido y esquiva el bloque de hielo sin un solo rasguño."],
                    "siguiente": "pinguino_2"
                },
                {
                    "texto": "Intentar cortarlo con la espada de frente",
                    "dano_jugador": 300,
                    "efecto": "hielo_golpe.wav",
                    "res_paginas": [f"{n} intenta cortar el hielo, pero es demasiado pesado y duro; te golpea fuerte y te mata."],
                    "siguiente": "pinguino_2"
                },
                {
                    "texto": "Saltar sobre él",
                    "dano_jugador": 150,
                    "efecto": "hielo_golpe.wav",
                    "res_paginas": [f"{n} saltas que pendejo, el hielo es gigante...moriste."],
                    "siguiente": "pinguino_2"
                }
            ]
        },
        "pinguino_2": {
            "fondo": "fondo_castillo_hielo.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "rey_pinguino_frente.png",
            "paginas": [
                "El Rey Pingüino se enoja, se pone furioso y se lanza a toda velocidad a embestirte con su gran panza.",
                "¿Qué haces?"
            ],
            "opciones": [
                {
                    "texto": "Esquivar y hacerle zancadilla",
                    "dano_enemigo": 50,
                    "efecto": "golpe_trono.wav",
                    "res_paginas": [f"{n} esquiva en el último segundo y le hace una zancadilla, haciendo que el rey se golpee contra el trono."],
                    "siguiente": "pinguino_3"
                },
                {
                    "texto": "Recibir la embestida con los brazos abiertos",
                    "dano_jugador": 400,
                    "efecto": "derrota.wav",
                    "res_paginas": [f"{n} intenta bloquearlo pero la fuerza del rey es descomunal, mandándolo a volar contra una pared mueres."],
                    "siguiente": "pinguino_3"
                },
                {
                    "texto": "Agacharte rápidamente",
                    "dano_enemigo": 20,
                    "efecto": "golpe_trono.wav",
                    "res_paginas": [f"{n} se agacha a tiempo y el rey pasa de largo chocando contra una columna de hielo."],
                    "siguiente": "pinguino_3"
                }
            ]
        },
        "pinguino_3": {
            "fondo": "fondo_castillo_hielo.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "rey_pinguino_aturdido.png",
            "paginas": ["El rey pingüino está tambaleándose. Es tu oportunidad de oro para contraatacar."],
            "opciones": [
                {
                    "texto": "Darle un espadazo directo al estómago",
                    "dano_enemigo": 80,
                    "efecto": "espada_fuerte.wav",
                    "res_paginas": [f"{n} le propina un golpe limpio con su espada de hierro, debilitando enormemente al rey."],
                    "siguiente": "pinguino_4"
                },
                {
                    "texto": "Lanzarle una roca pesada",
                    "dano_enemigo": 40,
                    "efecto": "roca.wav",
                    "res_paginas": [f"{n} le lanza una roca congelada que lo aturde un buen rato."],
                    "siguiente": "pinguino_4"
                },
                {
                    "texto": "Quitarle la esmeralda sin pelear",
                    "dano_jugador": 50,
                    "efecto": "rayo_hielo.wav",
                    "res_paginas": [f"{n} intenta arrebatar la joya con descuido, pero el rey te lanza un rayo de hielo congelándote el brazo."],
                    "siguiente": "pinguino_4"
                }
            ]
        },
        "pinguino_4": {
            "fondo": "fondo_castillo_hielo.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "rey_pinguino_veneno.png",
            "paginas": [
                "Derrotado y agonizando en el suelo, el Rey Pingüino tose y empieza a echar un extraño líquido negro y viscoso por la boca, amenazando con inundar toda la sala del trono con veneno.",
                "¿Qué haces rápido?"
            ],
            "opciones": [
                {
                    "texto": "Corrir a una zona alta y atacar",
                    "fijar_enemigo_vida": 10,
                    "efecto": "espada_fuerte.wav",
                    "res_paginas": [f"{n} trepa ágilmente a una estatua de hielo, esquivando la inundación tóxica y saltas para rematarlo enterrando tu espada en su garganta."],
                    "siguiente": "pinguino_5"
                },
                {
                    "texto": "Intentar taparle la boca con las manos",
                    "dano_jugador": 600,
                    "efecto": "veneno.wav",
                    "res_paginas": [f"{n} se arriesga a taparle la boca,grave error moriste."],
                    "siguiente": "pinguino_5"
                },
                {
                    "texto": "Cruzar corriendo el líquido",
                    "dano_jugador": 300,
                    "efecto": "veneno.wav",
                    "res_paginas": [f"{n} cruza corriendo el charco ácido sufriendo quemaduras en las botas y piernas mueres ."],
                    "siguiente": "pinguino_5"
                }
            ]
        },
        "pinguino_5": {
            "fondo": "fondo_castillo_hielo.png",
            "sprite_jugador": "caballero_espalda.png",
            "sprite_enemigo": "rey_pinguino_vencido.png",
            "paginas": [
                "El Rey Pingüino yace en el suelo, completamente vencido, piedad en sus pequeños ojos y temblando de frío. A su lado está la brillante Esmeralda de la Vida.",
                "¿Qué decides hacer?"
            ],
            "opciones": [
                {
                    "texto": "Perdonarle la vida y pedir la esmeralda",
                    "dano_jugador": 200,
                    "efecto": "traicion.wav",
                    "res_paginas": ["¡Paila! El rey fingía estar débil, te traiciona por la espalda con un cuchillo de hielo y te mata al instante."],
                    "siguiente": "victoria_final"
                },
                {
                    "texto": "Ignorarlo, agarrar la esmeralda e irte",
                    "dano_jugador": 200,
                    "efecto": "traicion.wav",
                    "res_paginas": ["Tomas la esmeralda y huyes, pero el rey se recupera y te ataca por la espalda cuando bajas la guardia. ¡Has muerto!"],
                    "siguiente": "victoria_final"
                },
                {
                    "texto": "Rematarlo de una vez por todas con la espada",
                    "fijar_enemigo_vida": 0,
                    "efecto": "victoria.wav",
                    "res_paginas": [f"{n} cumple con su deber de caballero, remata al malvado rey y recupera la Esmeralda de la Vida con éxito total."],
                    "siguiente": "victoria_final"
                }
            ]
        },

        # ================= FINAL =================
        "victoria_final": {
            "limpiar_enemigo": True,
            "fondo": "cinematica_victoria_final.png",
            "solo_cinematica": True,
            "musica": "fanfarria_victoria.mp3",
            "paginas": [
                f"¡FELICIDADES {n}!",
                "Has derrotado al Rey Pingüino, recuperado la Esmeralda de la Vida y salvado a todo el reino.",
                "Te has convertido en una leyenda viva. ¡Fin del juego!"
            ],
            "opciones": [
                {"texto": "Jugar de nuevo", "accion": "reiniciar"},
                {"texto": "Salir", "accion": "salir"}
            ]
        }
    }

    return escenas[id_escena]