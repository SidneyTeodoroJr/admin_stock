import flet as ft
from modules.db_utils import *
from modules.excel_utils import *
from modules.ui_components import *

def main(page: ft.Page):
    page.title = "Stock Management"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.HIDDEN

    create_table()

    items_data = []

    def remove_item(item):
        try:
            delete_item_from_db(item['id'])
            items_data[:] = [i for i in items_data if i['id'] != item['id']]
            page.controls = [search_field] + [create_list_tile(i, show_item_details, show_confirmation_modal) for i in items_data]
            page.update()
        except Exception as ex:
            print(f"Error removing item: {ex}")

    def remove_all_items(e):
        def confirm_delete_all(e):
            try:
                delete_all_items_from_db()
                items_data.clear()
                page.controls = [search_field]
                page.close(confirmation_modal)
                page.update()
            except Exception as ex:
                print(f"Error deleting all items: {ex}")

        confirmation_modal = ft.AlertDialog(
            title=ft.Text("Confirm Delete All"),
            content=ft.Text("Are you sure you want to delete all items?"),
            actions=[
                create_modal_button("Yes", confirm_delete_all, ft.colors.RED),
                create_modal_button("No", lambda e: page.close(confirmation_modal), ft.colors.GREEN),
            ],
        )
        page.open(confirmation_modal)

    def show_item_details(item):
        item_modal = create_item_details_modal(item, remove_item, page)
        page.open(item_modal)

    def show_confirmation_modal(item):
        confirmation_modal = create_confirmation_modal(item, remove_item, page)
        page.open(confirmation_modal)

    def add_item_to_page(item):
        items_data.append(item)
        page.controls = [search_field] + [create_list_tile(i, show_item_details, show_confirmation_modal) for i in items_data]
        page.update()

    def show_bottom_sheet(e):
        modal_user = create_add_item_modal(add_item_to_page, page)
        page.open(modal_user)

    def search_items(e):
        search_term = search_field.value.strip().lower()
        filtered_items = [item for item in items_data if search_term in item['name'].lower() or search_term in item['description'].lower()]
        page.controls = [search_field] + [create_list_tile(i, show_item_details, show_confirmation_modal) for i in filtered_items]
        page.update()

    def export_data_to_excel(e):
        try:
            items = get_items_from_db()
            export_to_excel(items)
            confirmation_modal = create_export_confirmation_modal(page)
            page.open(confirmation_modal)
        except Exception as ex:
            print(f"Error exporting data: {ex}")

    search_field = ft.TextField(
        hint_text="Search items...",
        prefix_icon=ft.icons.SEARCH,
        border_radius=ft.border_radius.all(30),
        on_change=search_items,
    )

    page.appbar = ft.CupertinoAppBar(
        bgcolor=ft.colors.GREEN,
        middle=ft.Text("Stock Management", color=ft.colors.WHITE),
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=show_bottom_sheet
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.GREEN_700,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.REDO_OUTLINED, icon_color=ft.colors.WHITE, on_click=export_data_to_excel),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.DELETE_SWEEP_ROUNDED, icon_color=ft.colors.WHITE, on_click=remove_all_items),
            ]
        ),
    )

    # Carregar itens do banco de dados e exibi-los
    items_data[:] = get_items_from_db()
    page.controls = [search_field] + [create_list_tile(i, show_item_details, show_confirmation_modal) for i in items_data]
    page.update()

ft.app(target=main)