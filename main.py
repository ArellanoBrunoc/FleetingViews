import flet as ft
import FleetingViews as fv
import time

def main(page: ft.Page):
    page.padding = ft.padding.all(0)
    # View definitions with specific configurations
    view_definitions = {
        'home': {
            'bgcolor': ft.colors.BLUE_GREY,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER
        },
        'settings': {
            'bgcolor': ft.colors.AMBER_900,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER
        },
        'projects': {
            'bgcolor': ft.colors.RED_900,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER
        }
    }

    # Create instances of FleetingViews and configure views and controls
    fleetingViews = fv.create_views(view_definitions=view_definitions, page=page)

    # Counter function to update visit count
    def counter(view):
        text = fleetingViews.views[view].controls[0].content.value
        number_of_times = int(text.split(" ")[-2])
        number_of_times += 1
        fleetingViews.views[view].controls[0].content.value = f"IM THE TEXT OF PAGE {view} {number_of_times} times"
        fleetingViews.view_go(view, duration=200, mode="top_left")



    # Set up content and buttons for the views
    fleetingViews.append("home", ft.Container(

        content=ft.Text("IM THE TEXT OF PAGE HOME 0 times", size=40),
     
        alignment=ft.alignment.center,
                expand=1
    ))

    fleetingViews.append("projects", ft.Container(

        content=ft.Text("IM THE TEXT OF PAGE PROJECTS 0 times", size=40),

        alignment=ft.alignment.center,
        expand=1
    ))

    fleetingViews.append("settings", ft.Container(

        content=ft.Text("IM THE TEXT OF SETTINGS HOME 0 times", size=40),
   
        alignment=ft.alignment.center,
                expand=1
    ))

    # Buttons with actions
    to_projects = ft.ElevatedButton("Projects", on_click=lambda _: counter("projects"))
    to_home = ft.ElevatedButton("Home", on_click=lambda _: counter("home"))
    to_settings = ft.ElevatedButton("Settings", on_click=lambda _: counter("settings"))
    back = ft.ElevatedButton("BACK!", on_click=lambda _: fleetingViews.go_back())
    back_2 = ft.ElevatedButton("BACK!", on_click=lambda _: fleetingViews.go_back())
    to_projects_2 = ft.ElevatedButton("Projects", on_click=lambda _: counter("projects"))
    to_home_2 = ft.ElevatedButton("Home", on_click=lambda _: counter("home"))
    to_settings_2 = ft.ElevatedButton("Settings", on_click=lambda _: counter("settings"))
    back_3 = ft.ElevatedButton("BACK!", on_click=lambda _: fleetingViews.go_back())

    # Append buttons to views
    fleetingViews.append("home", [to_settings, to_projects, back])
    fleetingViews.append("projects", [to_home, to_settings_2, back_2])
    fleetingViews.append("settings", [to_home_2, to_projects_2, back_3])

    # Example to get data from a view
    def get_data(e, view):
        data_in_project_view = fleetingViews.views['projects'].controls[0].content.value.split(" ")[-2]
        e.control.text = f"The {view} page has been visited {data_in_project_view} times"
        page.update()

    get_data_button = ft.ElevatedButton(text="GET DATA", on_click=lambda e: get_data(e, "projects"))
    fleetingViews.append("home", get_data_button)

    page.update()

ft.app(target=main)
