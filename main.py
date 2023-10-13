import pygame, random, math


# Inicializar Pygame
pygame.init()

# Crear la Pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

# Variables del Jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantida_enemigo = 8


for e in range(cantida_enemigo):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# Puntaje
puntaje = 0


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))
    
# Funcion disparar bala
def dispara_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# Funcion detectar coliciones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta = True
while se_ejecuta:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar Eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar tecla 
        if evento.type == pygame.KEYDOWN: 
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
        
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1

            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    bala_x = jugador_x
                    dispara_bala(bala_x, bala_y)
        
        # Evento soltar tecla 
        if evento.type == pygame.KEYUP: 
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # Mantener dentro del borde al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    
    # Modificar ubicacion del enemigo
    for e in range(cantida_enemigo):
        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro del borde al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio [e]
        elif enemigo_x[e] >= 736:
            enemigo_x[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e] 

        # Colicion
        colicion = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colicion:
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        dispara_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    

    jugador(jugador_x, jugador_y)
    

    # Actualizar
    pygame.display.update()

