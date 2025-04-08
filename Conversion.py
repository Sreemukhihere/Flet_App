import flet as ft
import json
import base64
import tempfile
import webbrowser

def conversion_page(page: ft.Page):
    page.title = "Convertion"
    page.bgcolor = "#5B9BD5"  # Specific sky blue color
    page.padding = 0  # Remove default padding
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Center content vertically
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Center content horizontally

    
      # White background header bar with titleTitle
    header = ft.Container(
        content=ft.Text(
            "Conversion",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=ft.Colors.WHITE,  # White background for the header
        padding=20,  # Padding inside the header
        alignment=ft.alignment.center,  # Center the title text
        width=page.width,  # Span the entire width of the screen
    )

    # PDF file picker
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            pdf_name.value = selected_file.name
            pdf_path.value = selected_file.path
            page.update()

    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(file_picker)

    # PDF details display
    pdf_name = ft.Text("No PDF selected", color=ft.Colors.BLACK)
    pdf_path = ft.Text(visible=False)  # Hidden field to store the file path

    # Dropdown for document types
    document_types = [
        "Aadhaar card",
        "Driving license",
        "PAN card",
        "Birth Certificate",
        "Ration Card",
        "Voter ID",
        "Passport",
    ]
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(doc) for doc in document_types],
        hint_text="Select document type",
        width=300,
    )

    # DataTable to display selected files
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("S.No")),
            ft.DataColumn(ft.Text("File Name")),
            ft.DataColumn(ft.Text("View")),
        ],
        rows=[],
    )

    # Function to handle PDF conversion
    def convert_pdf(e):
        if not pdf_path.value:
            pdf_name.value = "Please select a PDF file first!"
            page.update()
            return

        # Read PDF file as binary
        try:
            with open(pdf_path.value, "rb") as pdf_file:
                binary_data = pdf_file.read()

            # Convert binary data to JSON
            json_data = {
                "filename": pdf_name.value,
                "binary_data": base64.b64encode(binary_data).decode("utf-8"),  # Convert binary to base64 for JSON
            }

            # Print JSON data to the console
            print("JSON Data:")
            print(json.dumps(json_data, indent=4))  # Pretty-print JSON

            # Add the file to the DataTable
            serial_number = len(data_table.rows) + 1
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(serial_number))),
                        ft.DataCell(ft.Text(pdf_name.value)),
                        ft.DataCell(
                            ft.ElevatedButton(
                                "View",
                                on_click=lambda e, json_data=json_data: view_pdf(json_data),
                            )
                        ),
                    ]
                )
            )

            # Show success message
            pdf_name.value = "PDF converted successfully! Check the console for JSON output."
            page.update()

        except Exception as ex:
            pdf_name.value = f"Error: {str(ex)}"
            page.update()

    # Function to view PDF
    def view_pdf(json_data):
        try:
            # Convert base64 back to binary
            binary_data = base64.b64decode(json_data["binary_data"])

            # Save binary data to a temporary PDF file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(binary_data)
                temp_pdf_path = temp_pdf.name

            # Open the PDF file in the default PDF viewer
            webbrowser.open(temp_pdf_path)

        except Exception as ex:
            print(f"Error viewing PDF: {ex}")

    # Buttons inside a styled container
    buttons_container = ft.Container(
        content=ft.Column(
            [
                dropdown,  # Dropdown for document types
                ft.ElevatedButton(
                    "Import PDF",
                    on_click=lambda _: file_picker.pick_files(
                        allowed_extensions=["pdf"]
                    ),
                    bgcolor=ft.Colors.GREY_300,
                    color=ft.Colors.BLACK,
                ),
                ft.ElevatedButton(
                    "Submit",
                    on_click=convert_pdf,
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE,
                ),
                pdf_name,  # Display selected file name
                ft.Container(
                    content=data_table,
                    padding=20,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.WHITE,  # Container background color
        padding=40,  # Increased padding inside the container
        border_radius=10,  # Rounded corners
        width=600,  # Set a fixed width for the container
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.BLACK12,
        ),  # Add a shadow effect
    )

    # Return the entire layout as a Column
    return ft.Column(
        [
            header,  # Header bar with title
            ft.Container(
                content=buttons_container,
                padding=20,  # Add padding around the container
            ),
        ],
        spacing=0,  # No spacing between header and container
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )