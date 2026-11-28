# Ancasa Game: La Gran Esmeralda de la Vida

Videojuego de aventura y rol (RPG) desarrollado en Python. Toma el papel del mejor caballero del reino y emprende una travesía hasta la Antártida para derrotar al malvado Rey Pingüino y recuperar la Gran Esmeralda de la Vida.

---

## Punto de partida (Base actual)

Este repositorio parte de un **prototipo funcional en consola** contenido en el archivo base `legacy/main.py`. Actualmente, el proyecto opera como una aventura conversacional de elección múltiple en terminal que establece las bases narrativas y mecánicas principales del juego:

- **Narrativa interactiva:** Toma de decisiones con ramificaciones que afectan el desarrollo de la historia.
- **Sistema de combate por turnos:** Enfrentamientos básicos contra enemigos con gestión de estados y acciones.
- **Puntos de control (Checkpoints):** Lógica inicial de recuperación de progreso durante la partida en ejecución.

Este archivo base sirve como prueba de concepto y referencia funcional para validar la historia, el flujo de juego y las reglas principales antes de dar el salto hacia una arquitectura de software completa.

---

## Visión del proyecto: Hacia dónde vamos

El objetivo principal de este desarrollo es transformar el prototipo actual de terminal en un **videojuego con entorno gráfico completo**, diseñado bajo estándares y prácticas de **desarrollo de software profesional**.

### Metas de evolución técnica
1. **Migración a entorno gráfico:** Pasar de la interfaz de texto en consola a una interfaz gráfica 2D con soporte para sprites, escenarios, animaciones, menús interactivos, HUD (interfaz de usuario en pantalla) y efectos de sonido.
2. **Herramientas de guardado persistente:** Reemplazar los checkpoints temporales en memoria por un sistema de guardado y carga de partidas (mediante archivos txt), permitiendo gestionar múltiples ranuras de guardado y estadísticas.
3. **Arquitectura profesional y escalable:** Refactorizar el código monolítico inicial en una estructura modular limpia (separando lógica de negocio, interfaz gráfica, datos narrativos, persistencia y recursos multimedia), aplicando control de versiones, documentación técnica y pruebas.

---

## 👥 Equipo de Desarrollo y Créditos 
- **Arte:** **[@carlos2530]**
- Diseño y creación 100% original de los **sprites de personajes y enemigos en Pixel Art** con transparencia.
- Edición y adaptación de los **fondos de escenario**

- **Sistema de Guardado:** **[@manceraangelo527-jpg]**
- Diseño e implementación del **sistema de guardado** de partidas.

- **Diseño Narrativo y Control de Calidad (QA):** **Santiago Moreno Moreno** 
- Revisión, balanceo y **pruebas de escenarios, diálogos y rutas de decisión**. 

---

## 🎨 Atribución de Recursos y Herramientas 
- **Sprites:** Autoría original en Pixel Art por [@carlos2530]
- **Fondos de Escenario:** Generados conceptualmente con asistencia de **Google Gemini**, adaptados y optimizados manualmente para la arena visual del juego.