import flet as ft
from engine import MemoryEngine
import asyncio


def main(page: ft.Page):
    page.title = "Memory Match Game"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # IMPORTANT: Ensure the route is explicit
    page.route = "/"

    # State variables
    selected_cards = []
    engine = MemoryEngine()

    # Maps
    num_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8"}
    alpha_map = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}
    current_mode = "NUMBERS"

    # UI Components
    heading = ft.Text("Memory Match Game", size=30, weight="bold")
    score_row = ft.Row(controls=[], alignment=ft.MainAxisAlignment.CENTER)
    grid = ft.GridView(
        expand=False,
        runs_count=4,
        max_extent=100,
        spacing=10,
        run_spacing=10,
        width=440,
        height=440
    )

    async def on_card_click(e):
        card = e.control
        if card.data in engine.matched_indices or len(selected_cards) >= 2 or card in selected_cards:
            return

        card.content.visible = True
        card.bgcolor = ft.Colors.WHITE
        card.update()
        selected_cards.append(card)

        if len(selected_cards) == 2:
            await asyncio.sleep(0.5)
            c1, c2 = selected_cards
            if engine.check_match(c1.data, c2.data):
                c1.bgcolor = ft.Colors.GREEN_200
                c2.bgcolor = ft.Colors.GREEN_200
                score_row.controls.append(ft.Icon(ft.Icons.ICECREAM, color=ft.Colors.PURPLE))
                score_row.update()
            else:
                c1.content.visible = False
                c1.bgcolor = ft.Colors.BLUE_200
                c2.content.visible = False
                c2.bgcolor = ft.Colors.BLUE_200
            c1.update()
            c2.update()
            selected_cards.clear()

    def build_grid(mode=None):
        nonlocal current_mode
        if mode: current_mode = mode

        grid.controls.clear()
        selected_cards.clear()
        score_row.controls.clear()
        engine.__init__()

        current_map = num_map if current_mode == "NUMBERS" else alpha_map

        for i, val in enumerate(engine.cards):
            card = ft.Container(
                content=ft.Text(current_map.get(val, "?"), visible=False, size=30, weight="bold"),
                bgcolor=ft.Colors.BLUE_200,
                alignment=ft.Alignment.CENTER,
                on_click=on_card_click,
                data=i,
                border_radius=10,
                width=100,
                height=100
            )
            grid.controls.append(card)
        grid.update()
        score_row.update()

    # Buttons
    mode_row = ft.Row([
        ft.ElevatedButton("Numbers", on_click=lambda e: build_grid("NUMBERS")),
        ft.ElevatedButton("Alphabets", on_click=lambda e: build_grid("ALPHABETS")),
        ft.ElevatedButton("Reset Game", on_click=lambda e: build_grid(), color=ft.Colors.RED)
    ], alignment=ft.MainAxisAlignment.CENTER)

    page.add(ft.Column([heading, mode_row, score_row, grid], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    # Initialize
    build_grid("NUMBERS")


# Pass assets_dir="assets" explicitly to ensure web builds find them
ft.app(target=main, assets_dir="assets")