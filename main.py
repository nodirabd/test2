import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.DARK

    shopping_list = ft.Column()
    filter_type = 'all'

    bought_counter = ft.Text(value='Куплено товаров: 0', size=16, weight=ft.FontWeight.BOLD)

    # обновление счетчика купленных товаров по назваинию товара
    """def update_counter():
        completed_count = main_db.get_completed_count()
        bought_counter.value = f'Куплено товаров: {completed_count}'
        page.update()"""
    # обновление счетчика купленных товаров по количеству купленных товаров
    def update_counter():
        total_quantity = main_db.get_completed_count()
        bought_counter.value = f'Куплено товаров (всего шт.): {total_quantity}'
        page.update()

    def load_products():
        shopping_list.controls.clear()
        for product_id, product_name, quantity, completed in main_db.get_products(filter_type=filter_type):
            shopping_list.controls.append(
                view_product(
                    product_id=product_id,
                    product_name=product_name,
                    quantity=quantity,
                    completed=completed
                )
            )
        update_counter()
        page.update()

    def view_product(product_id, product_name, quantity, completed=None):
        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_product(product_id=product_id, is_completed=e.control.value)
        )

        product_text = ft.Text(
            value=f'{product_name} ({quantity} шт.)',
            expand=True,
            size=16
        )

        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED,
            on_click=lambda e: delete_product(product_id)
        )

        return ft.Row([checkbox, product_text, delete_button])

    def toggle_product(product_id, is_completed):
        main_db.update_product(product_id=product_id, completed=int(is_completed))
        load_products()

    def delete_product(product_id):
        main_db.delete_product(product_id=product_id)
        load_products()

    def add_product(e):
        if product_input.value and quantity_input.value:
            product_name = product_input.value
            quantity = quantity_input.value

            product_id = main_db.add_product(
                product_name=product_name,
                quantity=quantity
            )

            print(f'Товар {product_name} добавлен! Его ID - {product_id}')

            product_input.value = None
            quantity_input.value = None

            load_products()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_products()

    product_input = ft.TextField(
        label='Введите товар',
        expand=True,
        on_submit=add_product
    )

    quantity_input = ft.TextField(
        label='Количество',
        on_submit=add_product
    )

    #add_button = ft.Button(text='ADD',on_click=add_product)
    add_button = ft.Button("Добавить товар", on_click=add_product)

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton(
                'Все',
                on_click=lambda e: set_filter('all'),
                icon=ft.Icons.LIST
            ),
            ft.ElevatedButton(
                'Купленные',
                on_click=lambda e: set_filter('completed'),
                icon=ft.Icons.CHECK_CIRCLE,
                icon_color=ft.Colors.GREEN
            ),
            ft.ElevatedButton(
                'Некупленные',
                on_click=lambda e: set_filter('uncompleted'),
                icon=ft.Icons.RADIO_BUTTON_UNCHECKED,
                icon_color=ft.Colors.ORANGE
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    add_product_row = ft.Row([product_input, quantity_input, add_button])

    page.add(
        ft.Text('Список покупок'),
        add_product_row,
        filter_buttons,
        bought_counter,
        shopping_list
    )

    load_products()


if __name__ == "__main__":
    main_db.init_db()
    ft.run(main)
