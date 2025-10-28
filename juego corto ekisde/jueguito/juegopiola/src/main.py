import flet as ft
import random
import asyncio

async def main(page: ft.Page):
    page.title = "Atrapa el Cuadrado"
    page.window_width = 400
    page.window_height = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Estado del juego
    score = 0
    time_left = 20
    playing = False

    # Elementos visuales
    score_text = ft.Text(f"Puntaje: {score}", size=25, color="green")
    timer_text = ft.Text(f"Tiempo: {time_left}", size=25, color="red")
    status_text = ft.Text("", size=20, color="blue")

    # Cuadrado clickeable
    square = ft.Container(
        width=60,
        height=60,
        bgcolor="blue",
        border_radius=5,
        visible=False,
    )

    # Zona de juego
    game_area = ft.Stack(
        [
            ft.Container(
                width=300,
                height=300,
                bgcolor="#eeeeee",
                border=ft.border.all(2, "black"),
            ),
            square,
        ],
        width=300,
        height=300,
    )

    start_button = ft.ElevatedButton("Iniciar juego")

    page.add(
        ft.Column(
            [
                ft.Row([score_text, timer_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                game_area,
                status_text,
                start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ---------------- FUNCIONES ----------------
    def update_ui():
        score_text.value = f"Puntaje: {score}"
        timer_text.value = f"Tiempo: {time_left}"
        page.update()

    def random_position():
        """Genera una posición aleatoria dentro del área"""
        square.left = random.randint(0, 240)
        square.top = random.randint(0, 240)
        page.update()

    async def countdown():
        """Cuenta regresiva"""
        nonlocal time_left, playing
        while time_left > 0 and playing:
            await asyncio.sleep(1)
            time_left -= 1
            update_ui()
        end_game()

    def click_square(e):
        """Evento de clic sobre el cuadrado"""
        nonlocal score
        if not playing:
            return
        score += 1
        status_text.value = "¡Bien hecho!"
        random_position()
        update_ui()

    def start_game(e):
        """Inicia el juego"""
        nonlocal score, time_left, playing
        score = 0
        time_left = 20
        playing = True
        start_button.disabled = True
        square.visible = True
        status_text.value = ""
        random_position()
        update_ui()
        page.update()
        page.run_task(countdown)  # Inicia la cuenta regresiva asíncrona

    def end_game():
        """Finaliza el juego"""
        nonlocal playing
        playing = False
        square.visible = False
        start_button.disabled = False
        status_text.value = f"⏰ Fin del juego. Puntaje final: {score}"
        page.update()

    # Asigna los eventos
    start_button.on_click = start_game
    square.on_click = click_square

    page.update()

ft.app(target=main)
