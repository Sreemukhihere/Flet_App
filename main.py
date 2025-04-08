import flet as ft
import subprocess
import asyncio
from MasterSession import master_session_page
from sidepannel_datatable import sidepanel_datatable
from Orderbooking import Orderbooking
from Conversion import conversion_page
from dashboardscreen import Dashboard
import json
import os

async def main(page: ft.Page):
    page.title = "Responsive Dashboard"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ALWAYS

    async def run_python_file(file_path):
        try:
            process = await asyncio.create_subprocess_exec(
                "python", file_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                return stdout.decode()
            else:
                return f"Error: {stderr.decode()}"
        except Exception as e:
            return f"Exception: {str(e)}"

    async def display_output(file_path, output_text):
        output_text.value = await run_python_file(file_path)
        output_text.update()

    # Function to toggle the side panel's visibility with sliding animation
    def toggle_side_panel(e):
        if side_panel.width == 0:
            side_panel.width = 250  # Open the side panel
        else:
            side_panel.width = 0  # Close the side panel
        page.update()

    def navigate_to_screen(index):
        screens = [
            home_screen,
            master_session_screen,
            sidepannel_datatable_screen,
            orderbooking_screen,
            conversion_screen,
        ]
        
        if index >= len(screens):  # Prevents IndexError
            index = 0  

        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Column(
                        [
                            ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
                            ft.Row(
                                [
                                    side_panel,
                                    ft.VerticalDivider(width=1, visible=side_panel.width > 0),
                                    ft.ListView([screens[index]()], expand=True, spacing=10, padding=10)
                                ],
                                expand=True,
                            )
                        ],
                        expand=True,
                    )
                ]
            )
        )
        page.update()

    # Menu button to toggle the side panel
    menu_button = ft.IconButton(icon=ft.Icons.MENU, on_click=toggle_side_panel)

    # Side panel with sliding animation and scrollable content
    side_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.NavigationRail(
                        selected_index=0,
                        label_type=ft.NavigationRailLabelType.ALL,
                        destinations=[
                            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Home"),
                            ft.NavigationRailDestination(icon=ft.Icons.CODE, label="MasterSession"),
                            ft.NavigationRailDestination(icon=ft.Icons.TABLE_CHART, label="Sidepannel Datatable"),
                            ft.NavigationRailDestination(icon=ft.Icons.SHOPPING_CART, label="Orderbooking"),
                            ft.NavigationRailDestination(icon=ft.Icons.SWAP_HORIZ, label="Conversion"),
                            ft.NavigationRailDestination(icon=ft.Icons.ACCESS_TIME, label="ABC"),
                            ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BOX, label="def"),
                            ft.NavigationRailDestination(icon=ft.Icons.ADD_HOME, label="ghi"),
                            ft.NavigationRailDestination(icon=ft.Icons.ADD_LOCATION, label="jkl"),
                            ft.NavigationRailDestination(icon=ft.Icons.ADOBE, label="mno"),
                            ft.NavigationRailDestination(icon=ft.Icons.AIRPLANEMODE_ON, label="qrs"),
                            ft.NavigationRailDestination(icon=ft.Icons.ARCHIVE, label="tuvw"),
                            ft.NavigationRailDestination(icon=ft.Icons.APPLE, label="xy"),
                            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART, label="z"),
                            ft.NavigationRailDestination(icon=ft.Icons.ACCESS_TIME, label="ABC"),
                            ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BOX, label="def"),
                            ft.NavigationRailDestination(icon=ft.Icons.ADD_HOME, label="ghi"),
                            ft.NavigationRailDestination(icon=ft.Icons.ADD_LOCATION, label="jkl"),
                            ft.NavigationRailDestination(icon=ft.Icons.ADOBE, label="mno"),
                            ft.NavigationRailDestination(icon=ft.Icons.AIRPLANEMODE_ON, label="qrs"),
                            ft.NavigationRailDestination(icon=ft.Icons.ARCHIVE, label="tuvw"),
                            ft.NavigationRailDestination(icon=ft.Icons.APPLE, label="xy"),
                            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART, label="z"),
                        ],
                        on_change=lambda e: navigate_to_screen(e.control.selected_index),
                        expand=True,  # Set expand property to true
                    ),
                    height=page.height,  # Set a fixed height for the NavigationRail container
                )
            ],
            scroll=ft.ScrollMode.ALWAYS,  # Make the Column scrollable
            expand=True,  # Make the Column expand to fill the Container
        ),
        width=0,  # Start with the side panel closed
        animate=ft.animation.Animation(300, "easeInOut"),  # Smooth sliding animation
        bgcolor=ft.Colors.BLUE_GREY_100,  # Background color for the side panel
        padding=ft.padding.only(left=10, top=20, right=10, bottom=20),  # Padding inside the side panel
    )

    # Update side_panel height dynamically when the page is resized
    def update_side_panel_height(e):
        if hasattr(page, "height"):
            side_panel.content.controls[0].height = page.height  # Update the height of the NavigationRail container
        page.update()

    # Attach the resize event handler
    page.on_resize = update_side_panel_height

    def home_screen():
        return Dashboard(page)  
    
    def master_session_screen():
        return master_session_page(page)  

    def sidepannel_datatable_screen():
        return sidepanel_datatable(page)  

    def orderbooking_screen():
        return Orderbooking(page)  

    def conversion_screen():
        return conversion_page(page)  

    # Initial view
    navigate_to_screen(0)

ft.app(target=main)