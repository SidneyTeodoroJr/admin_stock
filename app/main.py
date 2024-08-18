import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Admin Stock"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_minimizable = False
    page.window_maximizable = False
    page.scroll = ft.ScrollMode.HIDDEN

    # Armazena os dados dos itens
    items_data = []

    def add_tile_to_page(name: str, date: str, description: str):
        # Função para remover o tile
        def remove_tile(e):
            items_data.remove((tile, name, date, description))
            page.remove(tile)
            page.close(item_details_modal)
            page.update()

        # Função para exibir o modal com detalhes do item
        def show_item_details(e):
            item_details_modal = ft.AlertDialog(
                title=ft.Text(name),
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text(f"Date: {date}"),
                        ft.Text(f"Description: {description}"),
                    ],
                ),
                actions=[
                    ft.TextButton("Delete", on_click=remove_tile, style=ft.ButtonStyle(color=ft.colors.RED)),
                    ft.TextButton("Close", on_click=lambda _: page.close(item_details_modal)),
                ],
            )
            page.open(item_details_modal)

        # Cria o tile
        tile = ft.CupertinoListTile(
            additional_info=ft.Text(date),
            leading=ft.Icon(name=ft.icons.PERSON_3_SHARP),
            title=ft.Text(name),
            subtitle=ft.Text(description[:50] + '...'),  # Exibição compacta inicial
            trailing=ft.Icon(name=ft.icons.INFO_OUTLINE),
            on_click=show_item_details,
        )

        # Adiciona o tile à página
        page.add(tile)
        items_data.append((tile, name, date, description))  # Armazena dados do item
        page.update()

    def show_bottom_sheet(e):
        name_field = ft.TextField(label="Name", autofocus=True)
        description_field = ft.TextField(label="Description")

        error_message = ft.Text("", color=ft.colors.RED)
        
        def add_item(e):
            name = name_field.value.strip()
            description = description_field.value.strip()
            
            # Captura e formata a data e a hora no padrão brasileiro
            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M")
            
            if not name or not description:
                error_message.value = "Preencha os campos."
                page.update()
            else:
                add_tile_to_page(name, date, description)
                page.close(modal_user)

        modal_user = ft.BottomSheet(
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        name_field,
                        description_field,
                        error_message,
                        ft.ResponsiveRow([
                            ft.ElevatedButton("Add Item", on_click=add_item),
                            ft.ElevatedButton("Close", on_click=lambda _: page.close(modal_user)),
                        ]),
                    ],
                ),
            ),
        )
        page.open(modal_user)

    page.appbar = ft.CupertinoAppBar(
        bgcolor=ft.colors.SURFACE_VARIANT,
        middle=ft.Text("Admin List"),
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=show_bottom_sheet
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.GREEN,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.SHARE_ROUNDED, icon_color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.BAR_CHART_SHARP, icon_color=ft.colors.WHITE),
            ]
        ),
    )

    page.update()

ft.app(target=main)