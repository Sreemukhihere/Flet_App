4
import flet as ft
import json  # Import the json module to format the output

def Orderbooking(page: ft.Page):
    # Theme color selection
    theme_colors = {
        "Blue": "#ADD8E6",
        "Green": "#90EE90",
        "Pink": "#FFB6C1",
        "Orange": "#FFA07A",
        "Purple": "#D8BFD8"
    }

    outer_container = ft.Ref[ft.Container]()

    def change_theme(e):
        outer_container.current.bgcolor = theme_colors[e.control.value]
        page.bgcolor = theme_colors[e.control.value]  # Update the page background color
        page.update()

    theme_dropdown = ft.Dropdown(
        label="Theme Color",
        options=[ft.dropdown.Option(k) for k in theme_colors.keys()],
        on_change=change_theme,
        width=300
    )

    # Input fields with increased width
    date_picker = ft.TextField(label="Date", read_only=True, width=300)
    order_id = ft.TextField(label="Order ID", width=300)
    customer_id = ft.TextField(label="Customer ID", width=300)
    customer_name = ft.TextField(label="Customer Name", read_only=True, width=300)
    project = ft.TextField(label="Project", width=300)
    plot = ft.TextField(label="Plot", width=300)
    order_value = ft.TextField(label="Order Value (₹)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    advance_payment = ft.TextField(label="Advance / Down Payment (₹)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    handover_date = ft.TextField(label="Handover Date", read_only=True, width=300)
    mode = ft.Dropdown(
        label="Mode",
        options=[
            ft.dropdown.Option("Cost"),
            ft.dropdown.Option("PE"),
            ft.dropdown.Option("IMP2")
        ],
        width=300
    )

    # Date Pickers
    date_picker_dialog = ft.DatePicker()
    handover_date_picker_dialog = ft.DatePicker()

    def update_date(field, e):
        if e.data:
            # Extract only the date part (YYYY-MM-DD) from the date string
            selected_date = e.data.split("T")[0]
            field.value = selected_date
            page.update()

    date_picker_dialog.on_change = lambda e: update_date(date_picker, e)
    handover_date_picker_dialog.on_change = lambda e: update_date(handover_date, e)

    def pick_date(e):
        page.dialog = date_picker_dialog
        date_picker_dialog.open = True
        page.update()

    def pick_handover_date(e):
        page.dialog = handover_date_picker_dialog
        handover_date_picker_dialog.open = True
        page.update()

    date_picker.suffix = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=pick_date)
    handover_date.suffix = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=pick_handover_date)

    # Function to handle the "Order" button click
    def submit_order(e):
        # Collect all the data into a dictionary
        order_data = {
            "date": date_picker.value,
            "order_id": order_id.value,
            "customer_id": customer_id.value,
            "customer_name": customer_name.value,
            "project": project.value,
            "plot": plot.value,
            "order_value": order_value.value,
            "advance_payment": advance_payment.value,
            "handover_date": handover_date.value,
            "mode": mode.value
        }

        # Convert the dictionary to a JSON string
        order_json = json.dumps(order_data, indent=4)

        # Print the JSON string to the console
        print("Order Data (JSON):")
        print(order_json)

    # Order form container with increased height and width
    order_container = ft.Container(
        bgcolor="white",
        padding=20,
        border_radius=10,
        alignment=ft.alignment.center,
        height=650,  # Increased height to accommodate the button
        width=500,  # Increased width for better visibility
        content=ft.Column(
            [
                date_picker,
                order_id,
                customer_id,
                customer_name,
                project,
                plot,
                order_value,
                advance_payment,
                handover_date,
                mode,
                ft.ElevatedButton(  # Add the "Order" button
                    text="Order",
                    on_click=submit_order,  # Call the submit_order function
                    width=300,
                    height=40,
                    style=ft.ButtonStyle(  
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE,
                    )
                )
            ],
            scroll=ft.ScrollMode.AUTO,  # Enable both vertical and horizontal scrolling
            spacing=10
        )
    )

    # Return the main layout as a Flet control
    return ft.Column([
        ft.Text("OrderBooking", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Row([
            theme_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Container(
            ref=outer_container,
            bgcolor="#ADD8E6",  # Match background color with theme
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [order_container],
                scroll=ft.ScrollMode.AUTO  # Enable scrolling inside the column
            )
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)