import flet as ft
import json

# Sample JSON data with increased rows and 8 products
json_data = {
    "products": [
        {
            "name": f"Product {i+1}",
            "data": [["1", "2", "3"]] * 20,  # 20 rows, 3 columns
            "details": [
                {"Face": f"Face {i+1}", "Area": f"Area {i+1}", "Left": f"Left {i+1}", 
                 "Right": f"Right {i+1}", "East": f"East {i+1}", "West": f"West {i+1}", "EST": f"EST {i+1}"}
                for i in range(20 * 3)  # Adjusted for increased rows
            ]
        } for i in range(8)  # 8 products
    ]
}

def create_table(data, product_name, details_panel, page):
    """Generate a scrollable data table with fixed cell sizes."""
    if not data or not data[0]:
        return ft.Text("No Data Available", size=16, weight=ft.FontWeight.BOLD)

    cell_size = 250  # Fixed size for each cell
    rows = []   

    for row_idx, row in enumerate(data):
        cells = [
            ft.Container(
                content=ft.Text(cell, size=14, weight=ft.FontWeight.BOLD, color="white"),
                alignment=ft.alignment.center,
                width=cell_size,
                height=cell_size,
                bgcolor="green" if cell == "1" else "orange" if cell == "2" else "red",
                border_radius=5,
                on_click=lambda e, r=row_idx, c=col_idx: display_details(details_panel, product_name, r, c, page)
            )
            for col_idx, cell in enumerate(row)
        ]
        rows.append(ft.Row(cells))

    # Wrapping table inside a ListView for scrolling
    scrollable_table = ft.ListView(controls=rows, expand=True, spacing=2, auto_scroll=False)

    return ft.Container(
        content=scrollable_table,
        expand=True,
        height=500,  # Fixed height to ensure scrolling is visible
        border=ft.border.all(1, "gray"),
        padding=5
    )

def display_details(details_panel, product_name, row_idx, col_idx, page):
    """Update the details panel based on the selected cell."""
    product = next(p for p in json_data["products"] if p["name"] == product_name)
    detail = product["details"][row_idx * len(product["data"][0]) + col_idx]
    details_panel.controls.clear()

    # Header for the details panel
    header = ft.Container(
        content=ft.Text(
            f"Details for {product_name} [{row_idx + 1}, {col_idx + 1}]",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="white",
        ),
        padding=15,
        bgcolor=page.theme_color,  # Use the selected theme color
        border_radius=ft.border_radius.only(top_left=10, top_right=10),  # Rounded corners only at the top
        alignment=ft.alignment.center,
    )
    
    # Details content
    details_content = ft.Column(
        [
            ft.Container(
                content=ft.Text(f"{key}: {value}", size=16, color="black"),
                padding=10,
                bgcolor="#E3F2FD",  # Light blue background for each detail
                border_radius=5,
                margin=ft.margin.symmetric(vertical=2),
            )
            for key, value in detail.items()
        ],
        spacing=5,
    )

    # Wrap the header and details in a card-like container
    details_card = ft.Container(
        content=ft.Column([header, details_content]),
        bgcolor="white",  # White background for the card
        border_radius=10,  # Rounded corners for the card
        border=ft.border.all(2, "gray"),  # Grey border for the details panel
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(2, 2),
        ),  # Subtle shadow for a lifted effect
        padding=0,  # No padding inside the card
    )

    details_panel.controls.append(details_card)
    details_panel.update()

def sidepanel_datatable(page: ft.Page):
    """Main app layout with scrolling enabled for the table."""
    # Theme color selector
    theme_colors = ["green", "blue", "pink", "orange", "purple"]
    page.theme_color = theme_colors[0]  # Default theme color

    def change_theme_color(e):
        """Change the theme color and update the UI."""
        page.theme_color = e.control.value
        header_bar.bgcolor = page.theme_color
        footer_bar.bgcolor = page.theme_color
        side_panel.bgcolor = page.theme_color
        details_panel.bgcolor = page.theme_color

        # Update the header of the details panel if it exists
        if len(details_panel.controls) > 0:
            if isinstance(details_panel.controls[0], ft.Container):  # Check if it's a details card
                details_card = details_panel.controls[0]
                if isinstance(details_card.content, ft.Column) and len(details_card.content.controls) > 0:
                    if isinstance(details_card.content.controls[0], ft.Container):  # Check if it's the header
                        details_card.content.controls[0].bgcolor = page.theme_color  # Update header color
            elif isinstance(details_panel.controls[0], ft.Container):  # Check if it's the "No item is selected" message
                details_panel.controls[0].bgcolor = page.theme_color  # Update background color

        page.update()

    # Dropdown for theme color selection
    theme_color_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(color) for color in theme_colors],
        value=page.theme_color,
        on_change=change_theme_color,
        width=150,
        text_size=16,
        color="white",
        bgcolor=page.theme_color,
        border_radius=10,
    )

    # Header Bar
    header_bar = ft.Container(
        content=ft.Row([
            ft.Text(
                "ShowDetails",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="white",
                text_align=ft.TextAlign.CENTER,
            ),
            theme_color_dropdown  # Use dropdown instead of buttons
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=page.theme_color,  # Use the selected theme color
        padding=20,
        alignment=ft.alignment.center,
        width=page.width,  # Span the entire width of the screen
    )

    # Footer Bar
    footer_bar = ft.Container(
        content=ft.Text(
            "Footer Section",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="white",
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=page.theme_color,  # Use the selected theme color
        padding=20,
        alignment=ft.alignment.center,
        width=page.width,  # Span the entire width of the screen
    )

    content_panel = ft.Container(expand=True)  # Table container (Scrollable)
    details_panel = ft.Column([], expand=True, scroll=ft.ScrollMode.AUTO)  # Details panel (Scrollable)
    
    # Initialize details panel with "No item is selected" message
    no_item_selected = ft.Container(
        content=ft.Text(
            "No item is selected",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="black",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="grey",  # Use the selected theme color
    )
    details_panel.controls.append(no_item_selected)
    
    def on_item_click(e):
        """Load selected product's data into the content panel."""
        product_name = e.control.data["name"]
        product_data = e.control.data["data"]
        content_panel.content = create_table(product_data, product_name, details_panel, page)
        page.update()
    
    # Sidebar with product selection styled as buttons
    side_panel = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(product["name"], size=16, weight=ft.FontWeight.BOLD, color="black"),
                padding=10,
                bgcolor="white",  # Button background color changed to white
                border_radius=10,  # Rounded corners for button-like appearance
                border=ft.border.all(2, "gray"),  # Border color changed to gray
                alignment=ft.alignment.center,  # Center text inside the button
                on_click=on_item_click,
                data=product,
            ) for product in json_data["products"]
        ], spacing=10),
        width=150,
        bgcolor=page.theme_color,  # Use the selected theme color
        alignment=ft.alignment.top_left  # Align content to the top
    )
    
    # Main content layout
    main_content = ft.Row([
        side_panel,
        ft.VerticalDivider(width=1),
        content_panel,  # Scrollable table container
        ft.VerticalDivider(width=1),
        ft.Container(
            content=details_panel,
            width=300,  # Increased width for the right side panel
            bgcolor="grey",  # Use the selected theme color
            padding=10,  # Add padding for better spacing
            border_radius=10,  # Rounded corners for the container
            border=ft.border.all(2, "gray"),  # Grey border for the details panel
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(2, 2),
            ),  # Subtle shadow for a lifted effect
        )
    ], expand=True)

    # Full layout with header, main content, and footer
    full_layout = ft.Column(
        [
            header_bar,  # Header bar
            main_content,  # Main content (table and details)
            footer_bar,  # Footer bar
        ],
        spacing=0,  # No spacing between sections
        expand=True,
    )

    # Return the full layout
    return full_layout