import flet as ft
import FleetingViews



def main(page: ft.Page):
    logged = True
    
    page.padding = ft.padding.all(0)

    def my_on_mount_hook_dos(ctx):
        print(f"hola {ctx.actual_view.route} dos" )
    
    def my_guard(ctx, name):
        if not logged:
            return False
        return True
    
    def change(e):
        nonlocal logged
        logged = False
        fv.add_hooks_or_guards("home", {"guards": my_guard})

        
    appbar = ft.AppBar(
                        leading= ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS, on_click=lambda e: fv.remove_hooks_or_guards("home", {"guards": my_guard})),
                        actions=[
                                ft.IconButton(icon=ft.Icons.HOME, on_click=lambda e: fv.view_go("home?id=23")),
                                ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e:fv.view_go("settings?id=24&login_key=hello_world")),
                                ft.IconButton(icon=ft.Icons.SCREEN_LOCK_LANDSCAPE, on_click=lambda e:fv.view_go("projects?id=projects")),
                                ft.IconButton(icon=ft.Icons.ERROR, on_click=lambda e: fv.view_go("homses?id=23")),
                                 ft.IconButton(icon=ft.Icons.GROUP_ADD_ROUNDED, on_click=change )
                                

                                ])
    def my_on_mount_hook(ctx, name):
        print(f"hola {ctx.get_params()}")
        return True
    # View definitions with specific configurations
    view_definitions = {
        'home': {
            'bgcolor': ft.Colors.BLUE_GREY,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
            "appbar": appbar,

        },
        'settings': {
            'bgcolor': ft.Colors.AMBER_900,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
            "appbar": appbar,

        },
        'projects': {
            'bgcolor': ft.Colors.GREEN_200,
            'vertical_alignment': ft.MainAxisAlignment.CENTER,
            'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
            "appbar": appbar,
        },

    }

    # Create instances of FleetingViews and configure views and controls
    fv = FleetingViews.create_views(view_definitions=view_definitions, page=page)
    
    def my_hook(name, params):
        print(params, name)

    fv.on_view_change = my_hook
    button_home = ft.TextButton(icon=ft.Icons.DATA_ARRAY, text="Get data!",on_click=lambda e: fv.update_view("home", {"bgcolor":  ft.Colors.RED,'horizontal_alignment': ft.CrossAxisAlignment.START }))

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
