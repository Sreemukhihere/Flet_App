import flet as ft
import json
import os

# JSON data for Country, State, and City
countries = ["USA", "India", "Canada"]
states = {
    "USA": ["California", "Texas", "New York"],
    "India": ["Maharashtra", "Karnataka", "Delhi"],
    "Canada": ["Ontario", "Quebec", "British Columbia"]
}
cities = {
    "California": ["Los Angeles", "San Francisco", "San Diego"],
    "Texas": ["Houston", "Dallas", "Austin"],
    "New York": ["New York City", "Buffalo", "Rochester"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Karnataka": ["Bangalore", "Mysore", "Mangalore"],
    "Delhi": ["New Delhi", "Noida", "Gurgaon"],
    "Ontario": ["Toronto", "Ottawa", "Mississauga"],
    "Quebec": ["Montreal", "Quebec City", "Laval"],
    "British Columbia": ["Vancouver", "Victoria", "Kelowna"]
}

def master_session_page(page: ft.Page):
    # Title
    title = ft.Container(
        content=ft.Text(
            "Master Session (MS)",
            size=30,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor=ft.Colors.WHITE,
        padding=15,
        alignment=ft.alignment.center,
    )

    # Input fields
    all_fields = ["Master ID", "Master Name", "Address", "Address 2"]
    inputs = {
        field: ft.TextField(label=field, bgcolor=ft.Colors.WHITE, border_radius=5)
        for field in all_fields
    }

    # Dropdowns
    country_dropdown = ft.Dropdown(
        label="Select Country",
        options=[ft.dropdown.Option(c) for c in countries],
        on_change=lambda e: update_states(),
    )
    state_dropdown = ft.Dropdown(
        label="Select State",
        options=[],
        on_change=lambda e: update_cities(),
    )
    city_dropdown = ft.Dropdown(
        label="Select City",
        options=[],
    )
    branch_dropdown = ft.Dropdown(
        label="Select Branch",
        options=[ft.dropdown.Option("Branch 1"), ft.dropdown.Option("Branch 2")],
    )

    # Function to update states based on selected country
    def update_states():
        selected_country = country_dropdown.value
        state_dropdown.options = [ft.dropdown.Option(s) for s in states.get(selected_country, [])]
        state_dropdown.value = None
        city_dropdown.options = []
        city_dropdown.value = None
        page.update()

    # Function to update cities based on selected state
    def update_cities():
        selected_state = state_dropdown.value
        city_dropdown.options = [ft.dropdown.Option(c) for c in cities.get(selected_state, [])]
        city_dropdown.value = None
        page.update()

    # Function to handle dropdown enabling/disabling
    def update_dropdowns(e):
        selected_type = master_type_dropdown.value

        # Enable all dropdowns first
        country_dropdown.disabled = False
        state_dropdown.disabled = False
        city_dropdown.disabled = False
        branch_dropdown.disabled = False

        # Disable dropdowns based on selected master type
        if selected_type == "City":
            city_dropdown.disabled = True
            city_dropdown.value = None
        elif selected_type == "State":
            state_dropdown.disabled = True
            state_dropdown.value = None
        elif selected_type == "Country":
            country_dropdown.disabled = True
            country_dropdown.value = None
        elif selected_type == "Branch":
            branch_dropdown.disabled = True
            branch_dropdown.value = None

        page.update()

    # Function to reset form
    def reset_form():
        master_type_dropdown.value = None
        country_dropdown.value = None
        country_dropdown.options = [ft.dropdown.Option(c) for c in countries]
        state_dropdown.value = None
        state_dropdown.options = []
        city_dropdown.value = None
        city_dropdown.options = []
        branch_dropdown.value = None

        # Reset all text fields
        for field in all_fields:
            inputs[field].value = ""
            inputs[field].error_text = ""

        # Enable all dropdowns
        country_dropdown.disabled = False
        state_dropdown.disabled = False
        city_dropdown.disabled = False
        branch_dropdown.disabled = False

        page.update()

    # Function to save data
    def save_data(e):
        first_empty_field = None
        required_fields = ["Master ID", "Master Name", "Address", "Address 2"]

        if master_type_dropdown.value in ["City", "State", "Country", "Branch"]:
            required_fields.extend([f for f in ["Country", "State", "City", "Branch"] if f != master_type_dropdown.value])
        else:
            required_fields.extend(["Country", "State", "City", "Branch"])

        if not master_type_dropdown.value:
            master_type_dropdown.error_text = "This field is required"
            first_empty_field = master_type_dropdown
        else:
            master_type_dropdown.error_text = ""

        for field in required_fields:
            if field in inputs and not inputs[field].value.strip():
                inputs[field].error_text = "This field is required"
                if not first_empty_field:
                    first_empty_field = inputs[field]

        for dropdown in [country_dropdown, state_dropdown, city_dropdown, branch_dropdown]:
            if dropdown.label in required_fields and not dropdown.value and not dropdown.disabled:
                dropdown.error_text = "This field is required"
                if not first_empty_field:
                    first_empty_field = dropdown

        page.update()

        if first_empty_field:
            first_empty_field.focus()
            return

        # Prepare data to save
        data = {
            "Master Type": master_type_dropdown.value,
            "Country": country_dropdown.value,
            "State": state_dropdown.value,
            "City": city_dropdown.value,
            "Branch": branch_dropdown.value,
            **{field: inputs[field].value for field in all_fields}
        }

        # Save data to a JSON file based on Master Type
        master_type = master_type_dropdown.value.lower().replace(" ", "_")
        filename = f"{master_type}_data.json"

        # Check if the file already exists
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Append new data to the existing data
        existing_data.append(data)

        # Save the updated data back to the file
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)

        print(f"Data saved to {filename}")

        # Reset form after saving
        reset_form()

    # Master Type Dropdown
    master_type_dropdown = ft.Dropdown(
        label="Master Type",
        options=[
            ft.dropdown.Option("Customer"),
            ft.dropdown.Option("Supplier"),
            ft.dropdown.Option("General List"),
            ft.dropdown.Option("City"),
            ft.dropdown.Option("State"),
            ft.dropdown.Option("Country"),
            ft.dropdown.Option("Branch")
        ],
        bgcolor=ft.Colors.WHITE,
        border_radius=5,
        on_change=update_dropdowns
    )

    # Save Button
    save_button = ft.ElevatedButton(
        "Save",
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        on_click=save_data,
    )

    # Form Layout
    form = ft.Column(
        controls=[
            master_type_dropdown,
            *inputs.values(),
            country_dropdown,
            state_dropdown,
            city_dropdown,
            branch_dropdown,
            ft.Row([save_button], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        scroll="auto",
    )

    # Form Container
    form_container = ft.Container(
        content=form,
        padding=30,
        bgcolor=ft.Colors.GREY_100,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        width=600,
        alignment=ft.alignment.center,
    )

    # Return the entire layout as a Column
    return ft.Column(
        [
            ft.Container(content=title, bgcolor=ft.Colors.BLUE_300, padding=15),
            ft.Row([form_container], alignment=ft.MainAxisAlignment.CENTER),
        ],
        expand=True,
    )