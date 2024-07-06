import flet as ft


class FleetingViews:
    def __init__(self, page:ft.Page, views: dict):
        """
        Initializes an instance of FleetingViews.

        Args:
            page (ft.Page): The Flet page where views will be displayed.
            views (dict): A dictionary where keys are view names and values are instances of ft.View.

        Raises:
            ValueError: If any value in the views dictionary is not a valid ft.View instance.
        """

        for name, view in views.items():
            if not isinstance(view, ft.View):
                raise ValueError("All value elements must be a valid ft.View() instance")
        self.page = page
        self.views = views
        last_view = next(reversed(views))
        # Stablishes control variables as the last added View
        self.actual_view = views[last_view]
        self.prev_views = []


    def view_go(self, view_name:str, back: bool = False):
        """
        Changes the current displayed view.

        Args:
            view_name (str): The name of the view to display.

        Raises:
            ValueError: If the view name is not in the views dictionary.
        """
        view_name = view_name.lower()
        if view_name in self.views.keys():
            view_index = self.page.views.index(self.views[view_name])
            self.page.views.pop(view_index)
            self.page.views.append(self.views[view_name])
            if self.actual_view != self.views[view_name] and self.actual_view.route not in self.prev_views and not back:
                self.prev_views.append(self.actual_view.route)
            elif self.actual_view != self.views[view_name] and self.actual_view.route in self.prev_views and not back:
                del_index = self.prev_views.index(self.actual_view.route)
                self.prev_views.pop(del_index)
                self.prev_views.append(self.actual_view.route)
            elif back:
                self.prev_views.pop()

            self.actual_view = self.views[view_name]
            self.page.update()

            print(self.prev_views)
        else:
            raise ValueError(f"{view_name} is not a view of this FleetingViews")
        
    def go_back(self):

        """
        Changes the current displayed view to one in the past

        """
        if len(self.prev_views) > 0:
            self.view_go(self.prev_views[-1], True)
        else:
            first_view = next(iter(self.views))
            self.view_go(first_view)
            self.prev_views =[]
        
    def clear(self):
        """
        Clears back history
        """
        self.prev_views = [];
    
    def append(self, view_name, controls):
        """
        Adds a control or a list of controls to a specific view. 
        If the working view is the same as the argument, behaves like the append method.

        Args:
            view_name (str): The name of the view to add the control(s) to.
            controls (Union[Control, List[Control]]): The control or list of controls to add.

        Raises:
            ValueError: If the view name is not in the views dictionary.
        """
        view_name = view_name.lower()
        if view_name in self.views:
            if isinstance(controls, list):
                for control in controls:
                    self.views[view_name].controls.append(control)
                    self.page.update()
            else:
                self.views[view_name].controls.append(controls)
                self.page.update()
            self.page.update()
        else:
            raise ValueError(f"{view_name} is not a view of this FleetingViews")

def initialize_view(view:ft.View, page: ft.Page):
    page.views.append(view)

def create_custom_view(route, 
                       appbar: ft.AppBar = None,
                       auto_scroll: bool = True,  
                       bgcolor: str = None, 
                       controls: list = [], 
                       drawer: ft.NavigationDrawer = None,
                       end_drawer: ft.NavigationDrawer = None, 
                       floating_action_button: ft.FloatingActionButton = None, 
                       horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.START, 
                       on_scroll_interval: int = 10,
                       padding: ft.Padding = ft.padding.all(10),
                       scroll: ft.ScrollMode = None,
                        spacing: int = 10,
                        vertical_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START):
    return ft.View(
        route=route,
        auto_scroll=auto_scroll,
        appbar=appbar,
        bgcolor=bgcolor,
        controls=controls,
        drawer=drawer,
        end_drawer=end_drawer,
        floating_action_button=floating_action_button,
        horizontal_alignment=horizontal_alignment,
        on_scroll_interval=on_scroll_interval,
        scroll=scroll,
        vertical_alignment=vertical_alignment,
        padding=padding,
        spacing=spacing
    )


def create_views(view_definitions: dict, page: ft.Page):
    """
    Adds a control or a list of controls to a specific view. 
    If the working view is the same as the argument, behaves like the append method.

    Args:
        view_definitions (dict): A dictionary with keys that contains the characteristics of the desired view, note that the 1st added view will be taken as root
        Page : flet page element to initialize the views.

    Raises:
        ValueError: If there is a definition that is not an string or contains spaces // if view_definitions is not a dict.

    Returns: a FleetingViews object to manage views on the application
    """
    page.views.pop(0)

    # Verify if names are valid strings and keys are valid dictionaries.
    for view_name, view_args in view_definitions.items():
        if not isinstance(view_name, str) or ' ' in view_name:
            raise ValueError("All names of views must be strings without spaces.")
        if not isinstance(view_args, dict):
            raise ValueError("Each view definition must be a dictionary with argument names and values.")

    views_dict = {}
    for view_name, view_args in view_definitions.items():
        # Usa create_custom_view con argumentos del diccionario y valores por defecto para los no entregados
        views_dict[view_name.lower()] = create_custom_view(
            route=view_args.get('route', view_name.lower()),
            appbar=view_args.get('appbar', None),
            auto_scroll=view_args.get('auto_scroll', True),
            bgcolor=view_args.get('bgcolor', None),
            controls=view_args.get('controls', []),
            drawer=view_args.get('drawer', None),
            end_drawer=view_args.get('end_drawer', None),
            floating_action_button=view_args.get('floating_action_button', None),
            horizontal_alignment=view_args.get('horizontal_alignment', ft.CrossAxisAlignment.START),
            on_scroll_interval=view_args.get('on_scroll_interval', 10),
            padding=view_args.get('padding', ft.padding.all(10)),
            scroll=view_args.get('scroll', None),
            spacing=view_args.get('spacing', 10),
            vertical_alignment=view_args.get('vertical_alignment', ft.MainAxisAlignment.START)
        )
        initialize_view(views_dict[view_name.lower()], page)

    fv = FleetingViews(page, views_dict)
    return fv

