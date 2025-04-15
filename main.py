import flet as ft
import FleetingViews as fleetingViews


def main(page: ft.Page):
    
    
    
    page.padding = ft.padding.all(0)
    home_drawer = ft.NavigationDrawer(
      controls=[
          ft.Container(height=12),
          ft.NavigationDrawerDestination(
              label="IM THE HOME DRAWER",
              icon=ft.Icons.HOME,
              selected_icon_content=ft.Icon(ft.Icons.HOME_FILLED),
          )
      ]
    )
    appbar = ft.AppBar(
                        actions=[
                                ft.IconButton(icon=ft.Icons.HOME, on_click=lambda e: fv.view_go("home?id=23")),
                                ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e:fv.view_go("settings?id=24&login_key=hello_world"))
                                

                                ])

    # View definitions with specific configurations
    view_definitions = {
        'home': {
            'bgcolor': ft.Colors.BLUE_GREY,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
            "drawer":home_drawer,
            "appbar": appbar
        },
        'settings': {
            'bgcolor': ft.Colors.AMBER_900,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
            "appbar": appbar

        },
    }

    def my_callback(view, params):
        print("View_change!" ,"Params: ",view, params)
    
    # Create instances of FleetingViews and configure views and controls
    fv = fleetingViews.create_views(view_definitions=view_definitions, page=page)
    
    fv.on_view_change = my_callback


    button_home = ft.TextButton(icon=ft.Icons.DATA_ARRAY, text="Get data!",on_click=lambda e: print(fv.get_params()))

    button_settings = ft.TextButton(icon=ft.Icons.DATA_ARRAY, text="Get data!", on_click=lambda e: print(fv.get_params()))

    home_container = ft.Container(

        content=ft.Text("Im the text of page HOME", size=40),
        
     
        alignment=ft.alignment.center,
                expand=1
    )
    
    settings_container = ft.Container(

        content=ft.Text("Im the text of page SETTINGS", size=40),
        
     
        alignment=ft.alignment.center,
                expand=1
    )



    # Set up content and buttons for the views
    fv.append("home",[home_container, button_home])


    fv.append("settings", [settings_container, button_settings])


    page.update()

ft.app(target=main)
