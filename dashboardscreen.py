import flet as ft
import random
import json

def Dashboard(page: ft.Page):
    page.title = "Realestates Dashboard"
    page.bgcolor = "#F8F9FA"  # Light background
    page.padding = 20
    
    # Sample JSON Data
    json_data = '''
    {
        "bookings": 320,
        "occupancy_rate": 85,
        "revenue": 150000,
        "customer_satisfaction": 92,
        "room_distribution": {
            "Single": 30,
            "Double": 50,
            "Suite": 15,
            "Deluxe": 5
        }
    }
    '''
    
    data = json.loads(json_data)
    
    # KPI Containers
    bookings_text = ft.Text(f"{data['bookings']}", size=24, color="#00796B")
    occupancy_text = ft.Text(f"{data['occupancy_rate']}%", size=24, color="#0288D1")
    revenue_text = ft.Text(f"${data['revenue']:,}", size=24, color="#7B1FA2")
    satisfaction_text = ft.Text(f"{data['customer_satisfaction']}%", size=24, color="#F57C00")
    
    kpi_section = ft.Row([
        ft.Container(ft.Column([ft.Text("Total Bookings", size=20, weight="bold", color="#424242"), bookings_text]), padding=20, bgcolor="#E0F2F1", width=220, border_radius=10),
        ft.Container(ft.Column([ft.Text("Occupancy Rate", size=20, weight="bold", color="#424242"), occupancy_text]), padding=20, bgcolor="#E3F2FD", width=220, border_radius=10),
        ft.Container(ft.Column([ft.Text("Total Revenue", size=20, weight="bold", color="#424242"), revenue_text]), padding=20, bgcolor="#F3E5F5", width=220, border_radius=10),
        ft.Container(ft.Column([ft.Text("Customer Satisfaction", size=20, weight="bold", color="#424242"), satisfaction_text]), padding=20, bgcolor="#FFE0B2", width=220, border_radius=10),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Line Chart for Revenue Trends
    line_chart = ft.LineChart(
        data_series=[ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, random.randint(100000, 200000)) for x in range(1, 13)],
            stroke_width=3, color="#00796B"
        )],
        min_y=100000, max_y=200000, 
        min_x=1, max_x=12, 
        height=250, width=600
    )
    
    line_chart_container = ft.Container(line_chart, padding=20, bgcolor="#E8F5E9", border_radius=10, expand=True)
    
    # Pie Chart for Room Distribution
    pie_chart = ft.PieChart(
        sections=[
            ft.PieChartSection(data['room_distribution']["Single"], title="Single", color="#0288D1"),
            ft.PieChartSection(data['room_distribution']["Double"], title="Double", color="#7B1FA2"),
            ft.PieChartSection(data['room_distribution']["Suite"], title="Suite", color="#F57C00"),
            ft.PieChartSection(data['room_distribution']["Deluxe"], title="Deluxe", color="#00796B"),
        ],
        expand=True,
    )
    
    pie_chart_container = ft.Container(pie_chart, padding=20, bgcolor="#FFF3E0", border_radius=10, width=300, height=300)
    
    # Layout Adjustment to Place Pie Chart on the Right
    chart_row = ft.Row([line_chart_container, pie_chart_container], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Return ft.Column instead of using page.add()
    return ft.Column([ft.Text("Welcome to Hotel Management Dashboard", size=28, weight="bold", color="#424242"),kpi_section,chart_row])
