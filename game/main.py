import time

def texto_lento(texto):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(0.025)
    print()    

def p(*textos):
    texto_lento("".join(str(t) for t in textos))

texto_lento("bienvenido al primer minijuego de angelo")
print()

def nom():
    nom = input("dame tu nombre: ")
    return nom

vida = 100
dinero = 50
texto_lento("aqui tienes tus estadisticas iniciales")
print("vida inicial:", vida)
print("inventario: espada de hierro, armadura de cuero")
print("dinero:", dinero)
print()

def elegir_opcion(opciones):
    while True:
        eleccion = input("elige una opcion: ")
        print()
        if eleccion in opciones:
            return eleccion
        else:
            texto_lento("esa opcion no existe")

n = nom()
p(n, " es el mejor caballero de todo el reino")
print()
p("y le asignaron la gran mision... una mision cuyo objetivo es matar al malvado rey de los pinguinos que ha robado la gran esmeralda de la vida")
print()
p(n, " tiene que ir hasta la antartida para recuperar la joya, pero el camino no sera nada facil, estas listo para jugar??")
print()
print("1. si estoy listo")
print()
print("2. no")
print()

b = elegir_opcion(["1", "2"])
if b == "1":
    print("perfecto empezemos")
    print()
elif b == "2":
    print("esta bien :(")
    print()
    exit()
    
checkpoint = "jungla"
    
def combate_stich(vida, n):
    vidastich = 100

    p(n, " acaba de salir del reino y esta atravesando la jungla de los bambus")
    print()
    p("se escucha un ruido detras de unos bambus")
    print()
    p("detras de los bambus aparece un monstruo azul orejon de un metro que empieza a gritar")
    print()
    p("que haras??")
    print()

    print("1. atacar")
    print()
    print("2. intentar hablar con el")
    print()
    print("3. ignorarlo")
    print()

    a = elegir_opcion(["1", "2", "3"])
    if a == "1":
        vidastich -= 20
        p(n, " ataca al enemigo y le hace daño")
        print()
    elif a == "2":
        vida -= 20
        p(n, " intenta hablar con el monstruo, no quiere hablar y le tira a su mini hijo que muerde a ", n)
        print()
    elif a == "3":
        vida -= 100
        p(n, " ignora al monstruo y lo pasa de largo, el monstruo te ataca desde la espalda y te mata")
        print()

    print("vida actual:", vida, "vida del enemigo", vidastich)
    print()
    if vida <= 0:
        return vida, False
        
    p("cual es tu siguiente movimiento??")
    print()
    print("1. atacar")
    print()
    print("2. curarse")
    print()
    print("3. huir")
    print()

    g = elegir_opcion(["1", "2", "3"])

    if g == "1":
        vidastich -= 20
        p(n, " ataca al monstruo")
        print()
    elif g == "2":
        vida += 20
        p(n, " se cura la vida")
        print()
    elif g == "3":
        vida -= 100
        p(n, " intento escapar, el monstruo te ataca desde la espalda y te mata")
        print()

    print("vida actual:", vida, "vida del enemigo", vidastich)
    print()
    if vida <= 0:
        return vida, False

    p("el monstruo acaba de sacar mas de sus hijos que estan por atacarte, que haras?")    
    print()
    print("1. ignorarlos y contraatacar")
    print()
    print("2. defenderse")
    print()
    print("3. atacar a los hijos del monstruo")
    print()

    d = elegir_opcion(["1", "2", "3"])

    if d == "1":
        vida -= 30
        p(n, " contraataca pero los mini hijos lo muerden y le hacen heridas")
        print()
    elif d == "2":
        vida -= 5
        p(n, " se defiende de los mini hijos pero recibe un poco de daño")
        print()
    elif d == "3":
        vidastich -= 10
        p(n, " mata a los hijos del monstruo sin recibir daño, el monstruo recibe daño psicologico")
        print()

    print("vida actual:", vida, "vida del enemigo", vidastich)
    print()
    if vida <= 0:
        return vida, False

    p("tienes que hacer una estrategia para derrotar al monstruo, que haras?")
    print()
    print("1. atacar de frente")
    print()
    print("2. tirarle comida para que se distraiga")
    print()
    print("3. meterse detras de los arboles y atacar por sorpresa")
    print()

    t = elegir_opcion(["1", "2", "3"])

    if t == "1":
        vidastich -= 100
        vida -= 10
        p(n, " ataca de frente y aunque recibe daño mata al enemigo")
        print()
    elif t == "2":
        vida -= 100
        p(n, " le tira comida la cual el monstruo ignora y te mata")
        print()
    elif t == "3":
        vidastich -= 100
        p(n, " se pone detras de los arboles rodeandolo y lo ataca por la espalda y lo mata")
        print()

    print("vida actual:", vida, "vida del enemigo", vidastich)
    if vida <= 0:
        return vida, False
    elif vidastich <= 0:
        return vida, True

# Bucle principal de la Jungla
while True:
    if checkpoint == "jungla":
        vida, ganado = combate_stich(vida, n)
        if not ganado:
            print("reintentas desde el checkpoint de la jungla...")
            vida = 100
            continue
        else:
            checkpoint = "pueblo"
            break

p("sigues con tu aventura con ", vida, " de vida")
print()
p("inventario: espada de hierro, armadura de cuero")
print()
print("monedas:", dinero)
print()

def pueblo(vida, dinero, n):
    p("para este nivel debes de quedar con al menos 10 monedas")
    p("luego de derrotar al monstruo ", n, " pasa el bosque y se encuentra con un pueblo por lo que al ser ya casi de noche debe quedarse ahi hasta el amanecer")
    print()
    p(n, " se encuentra un hotel que vale 10 monedas, que haras?")
    print()
    print("1. pagas las 10 monedas y duermes")
    print()
    print("2. no duermes en hotel esta noche")
    print()
    f = elegir_opcion(["1", "2"])
    if f == "1":
        vida += 5
        dinero -= 10
        p("duermes en el hotel, descansas y te recuperas")
        print()
    elif f == "2":
        vida -= 200
        p("decidiste no pagar el hotel asi que dormiste en la calle, por lo que a mitad de la noche te robaron y te mataron")
        print()

    print("vida actual:", vida, "dinero actual", dinero)
    print()
    if vida <= 0:
        return vida, False
    elif dinero <= 9:
        return vida, False
    
    p("al amanecer debes ir a comprar comida, a donde compras?")
    print()
    p(n, " encuentra 3 mercados, en cual compras?")
    print()
    print("1. un lugar sucio, con ratas y muy feo, pero hay pasteles recien hechos relusientes y lindos en una cajita de cristal (valor 8 monedas)")
    print()
    print("2. un lugar decente acogedor con panes recien horneados y provisiones (valor 15 monedas)")
    print()
    print("3. un lugar muy lujoso y pulcro que vende deliciosa carne y provisiones de calidad (valor 25 monedas)")
    print()
    f = elegir_opcion(["1", "2", "3"])
    if f == "1":
        vida -= 150
        dinero -= 8
        p("el pastel y todo lo demás que compraste estaban vencidos, asi que te intoxicaste y moriste")
        print()
    elif f == "2":
        dinero -= 15
        p("el pan y todo lo demas resulta ser delicioso por lo que sobrevives con eso")
        print()
    elif f == "3":
        dinero -= 25
        p("compraste carne y provisiones que salieron muy bien, aunque gastaste bastante dinero")
        print()  

    print("vida actual:", vida, "dinero actual", dinero)
    print()    
    if vida <= 0:
        return vida, False
    elif dinero <= 9:
        return vida, False
    elif dinero >= 10:
        return vida, True

# Bucle principal del Pueblo
while True:
    if checkpoint == "pueblo":
        vida, ganado = pueblo(vida, dinero, n)
        if not ganado:
            print("reintentas desde el checkpoint del pueblo...")
            vida = 100
            dinero = 50
            continue
        else:
            checkpoint = "rey_pinguino"
            break

p("has llegado a la helada Antártida con ", vida, " de vida.")
print()


def combate_rey_pinguino(vida, n):
    vidapinguino = 200
    p("Llegas al castillo de hielo. El malvado Rey Pingüino te espera sentado en su trono sosteniendo la Gran Esmeralda de la Vida.")
    print()
    p("El Rey Pingüino te mira y se ríe burlonamente: 'Jelou, humano tonto, creíste que llegarías lejos? ¡Prepárate a congelarte!'")
    print()

    p("De repente, el rey te lanza con fuerza un enorme bloque de hielo directo al pecho. ¿Qué haces?")
    print()
    print("1. Esquivarlo hacia un lado")
    print("2. Intentar cortarlo con la espada de frente")
    print("3. Saltar sobre él")
    print()
    
    e1 = elegir_opcion(["1", "2", "3"])
    if e1 == "1":
        p(n, " da un salto lateral rápido y esquiva el bloque de hielo sin un solo rasguño.")
        print()
    elif e1 == "2":
        vida -= 300
        p(n, " intenta cortar el hielo, pero es demasiado pesado y duro; te golpea fuerte y te mata.")
        print()
    elif e1 == "3":
        vida -= 150
        p(n, " saltas que pendejo, el hielo es gigante...moriste.")
        print()

    if vida <= 0:
        return vida, False
    
    p("El Rey Pingüino se enoja, se pone furioso y se lanza a toda velocidad a embestirte con su gran panza.")
    print()
    p("¿Qué haces?")
    print()
    print("1. Esperar el momento justo para esquivar y hacerle zancadilla")
    print("2. Recibir la embestida con los brazos abiertos para bloquearlo")
    print("3. Agacharte rápidamente")
    print()

    e2 = elegir_opcion(["1", "2", "3"])
    if e2 == "1":
        vidapinguino -= 50
        p(n, " esquiva en el último segundo y le hace una zancadilla, haciendo que el rey se golpee contra el trono.")
        print()
    elif e2 == "2":
        vida -= 400
        p(n, " intenta bloquearlo pero la fuerza del rey es descomunal, mandándolo a volar contra una pared mueres.")
        print()
    elif e2 == "3":
        vidapinguino -= 20
        p(n, " se agacha a tiempo y el rey pasa de largo chocando contra una columna de hielo.")
        print()

    if vida <= 0:
        return vida, False

    p("El rey pingüino está tambaleándose. Es tu oportunidad de oro para contraatacar.")
    print()
    print("1. Darle un espadazo directo al estómago")
    print("2. Lanzarle una roca pesada")
    print("3. Tratar de quitarle la esmeralda de las manos sin pelear")
    print()

    e3 = elegir_opcion(["1", "2", "3"])
    if e3 == "1":
        vidapinguino -= 80
        p(n, " le propina un golpe limpio con su espada de hierro, debilitando enormemente al rey.")
        print()
    elif e3 == "2":
        vidapinguino -= 40
        p(n, " le lanza una roca congelada que lo aturde un buen rato.")
        print()
    elif e3 == "3":
        vida -= 50
        p(n, " intenta arrebatar la joya con descuido, pero el rey te lanza un rayo de hielo congelándote el brazo.")
        print()

    if vida <= 0:
        return vida, False


    p("Derrotado y agonizando en el suelo, el Rey Pingüino tose y empieza a echar un extraño líquido negro y viscoso por la boca, amenazando con inundar toda la sala del trono con veneno.")
    print()
    p("¿Qué haces rápido?")
    print()
    print("1. Corrir a una zona alta de la sala para salvarte y atacar")
    print("2. Intentar taparle la boca con las manos")
    print("3. Cruzar corriendo el líquido para rematarlo de una vez")
    print()

    e4 = elegir_opcion(["1", "2", "3"])
    if e4 == "1":
        p(n, " trepa ágilmente a una estatua de hielo, esquivando la inundación tóxica y saltas para rematarlo enterrando tu espada en su garganta.")
        print()
    elif e4 == "2":
        vida -= 600
        p(n, " se arriesga a taparle la boca,grave error moriste.")
        print()
    elif e4 == "3":
        vida -= 300
        p(n, " cruza corriendo el charco ácido sufriendo quemaduras en las botas y piernas mueres .")
        print()

    if vida <= 0:
        return vida, False

    p("El Rey Pingüino yace en el suelo, completamente vencido, piedad en sus pequeños ojos y temblando de frío. A su lado está la brillante Esmeralda de la Vida.")
    print()
    p("¿Qué decides hacer?")
    print()
    print("1. Perdonarle la vida, ayudarlo a levantarse y pedirle la esmeralda pacíficamente")
    print("2. Ignorarlo, agarrar la esmeralda e irte del lugar")
    print("3. Rematarlo de una vez por todas con la espada para asegurar el reino")
    print()

    e5 = elegir_opcion(["1", "2", "3"])
    if e5 == "1":
        p("¡Paila! El rey fingía estar débil, te traiciona por la espalda con un cuchillo de hielo y te mata al instante.")
        print()
        return vida - 200, False
    elif e5 == "2":
        p("Tomas la esmeralda y huyes, pero el rey se recupera y te ataca por la espalda cuando bajas la guardia. ¡Has muerto!")
        print()
        return vida - 200, False
    elif e5 == "3":
        vidapinguino = 0
        p(n, " cumple con su deber de caballero, remata al malvado rey y recupera la Esmeralda de la Vida con éxito total.")
        print()
        return vida, True

while True:
    if checkpoint == "rey_pinguino":
        vida, ganado = combate_rey_pinguino(vida, n)
        if not ganado:
            print("reintentas desde el checkpoint del castillo del Rey Pingüino...")
            vida = 100
            continue
        else:
            break

print("==================================================")
p("¡FELICIDADES ", n, "!")
p("Has derrotado al Rey Pingüino, recuperado la Esmeralda de la Vida y salvado a todo el reino.")
p("Te has convertido en una leyenda viva. ¡Fin del juego!")
print("==================================================")
