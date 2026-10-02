#Ancasa Game

¡Bienvenido a la aventura de **Ancasa Game**.

Este proyecto es una aventura gráfica e interactiva desarrollada en Python con la librería **Pygame**, estructurada de forma modular para un desarrollo limpio e interactivo.

---

## Características de la versión actual

- **Interfaz gráfica dividida**: Zona superior para escenarios/gráficos (800x400 px) y panel inferior para historia, opciones y estadísticas (800x200 px).
- **Nivel 1 (La Jungla)**: Enfrentamiento táctico y por decisiones contra Stitch y sus mini hijos.
- **Sistema de Checkpoint y Salud**: Control de vida en tiempo real y reinicio desde el punto de guardado en caso de derrota.

---

## Estructura del Proyecto

mision_caballero/
│
├── data.py           # Estado global y estadísticas del jugador
├── UI.py              # Gestión visual de la ventana gráfica en Pygame
├── main.py            # Bucle principal y control de eventos
├── levels/
│   └── Jungla_LV1.py      # Lógica y eventos del Nivel 1 (La Jungla)
│
├── .gitignore         # Exclusión de archivos temporales para Git
├── requirements.txt   # Lista de dependencias del proyecto
└── README.md          # Documentación del repositorio