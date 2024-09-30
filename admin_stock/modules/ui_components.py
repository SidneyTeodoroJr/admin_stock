import flet as ft
from datetime import datetime
from urllib.request import urlopen
import importlib.util  # Importação do importlib para carregar módulos dinamicamente

def import_db_utils():
    db_utils_url = "https://raw.githubusercontent.com/SidneyTeodoroJr/admin_stock/main/admin_stock/modules/db_utils.py"
    source_code = urlopen(db_utils_url).read().decode('utf-8')
    module_name = "db_utils"
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(source_code, module.__dict__)
    return module

db_utils = import_db_utils()

def create_modal_button(text, on_click, color):
    return ft.TextButton(text, on_click=on_click, style=ft.ButtonStyle(color=color))

def create_list_tile(item, on_view_details, on_confirm_delete):
    return ft.CupertinoListTile(
        additional_info=ft.Text(item['date_added']),
        leading=ft.Icon(name=ft.icons.PERSON_3_SHARP),
        title=ft.Text(item['name']),
        subtitle=ft.Text(item['description'][:50] + '...'),
        trailing=ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED,
            on_click=lambda e: on_confirm_delete(item)
        ),
        on_click=lambda e: on_view_details(item)
    )

def create_item_details_modal(item, on_remove, page):
    def show_confirmation_modal(e):
        confirmation_modal = create_confirmation_modal(item, on_remove, page)
        page.open(confirmation_modal)

    item_modal = ft.AlertDialog(
        title=ft.Text(item['name'], size=24),
        content=ft.Column(
            tight=True,
            controls=[
                ft.Text(f"Date: {item['date_added']}", size=16),
                ft.Text(f"Description: {item['description']}", size=16),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            create_modal_button("Delete", show_confirmation_modal, ft.colors.RED),
            create_modal_button("Close", lambda e: page.close(item_modal), ft.colors.GREEN),
        ],
    )
    return item_modal

def create_confirmation_modal(item, on_remove, page):
    def confirm_delete(e):
        try:
            on_remove(item)
            page.close(confirmation_modal)
        except Exception as ex:
            print(f"Error removing item: {ex}")

    confirmation_modal = ft.AlertDialog(
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this item?"),
        actions=[
            create_modal_button("Yes", confirm_delete, ft.colors.RED),
            create_modal_button("No", lambda e: page.close(confirmation_modal), ft.colors.GREEN),
        ],
    )
    return confirmation_modal

def create_add_item_modal(add_item_callback, page):
    name_field = ft.TextField(label="Name", autofocus=True)
    description_field = ft.TextField(label="Description")
    error_message = ft.Text("", color=ft.colors.RED)

    def add_item(e):
        name = name_field.value.strip()
        description = description_field.value.strip()

        now = datetime.now()
        date_added = now.strftime("%d/%m/%Y %H:%M")

        if not name or not description:
            error_message.value = "Please fill in all fields."
            page.update()
        else:
            try:
                db_utils.add_item_to_db(name, date_added, description)
                item = db_utils.get_items_from_db()[-1]
                add_item_callback(item)
                page.close(modal_user)
            except Exception as ex:
                error_message.value = f"Error adding item: {ex}"
                page.update()

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
                        create_modal_button("Add Item", add_item, ft.colors.GREEN),
                        create_modal_button("Close", lambda e: page.close(modal_user), ft.colors.RED),
                    ]),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.all(10),
        ),
    )
    return modal_user

def create_export_confirmation_modal(page):
    export_confirmation_modal = ft.AlertDialog(
        title=ft.Text("Export Successful"),
        content=ft.Text("The file has been saved to Downloads as 'inventory_export.xlsx'."),
        actions=[
            create_modal_button("Close", lambda e: page.close(export_confirmation_modal), ft.colors.GREEN),
        ],
    )
    return export_confirmation_modal
