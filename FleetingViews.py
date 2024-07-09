import flet as ft
import time





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
        self.working_view = views[last_view]
        self.is_executing = False  # Semaphore to control the execution of view_go and go_back()


    def view_go(self, view_name: str, back: bool = False, duration: int = 0, mode: str = "top_left"):
        """
        Changes the current displayed view.

        Args:
            view_name (str): The name of the view to display.
            back (bool): If the view_go call is intended for a back call.
            duration (int): The time for the animation in milliseconds

        Raises:
            ValueError: If the view name is not in the views dictionary.
        """
        if self.is_executing:
            return
        self.is_executing = True

        try:
            view_name = view_name.lower()
            if view_name in self.views.keys():
                if self.actual_view == self.views[view_name]:
                    return
                if duration > 0:
                    self.animation(duration, next_view_name=view_name, mode=mode)
                view_index = self.page.views.index(self.views[view_name])

                self.page.views.pop(view_index)
                self.page.views.append(self.views[view_name])

                if back:
                    self.prev_views.pop()
                else:
                    if self.actual_view.route in self.prev_views:
                        self.prev_views.remove(self.actual_view.route)
                    self.prev_views.append(self.actual_view.route)
                self.actual_view = self.views[view_name]
                self.page.update()
            else:
                raise ValueError(f"{view_name} is not a view of this FleetingViews")
        finally:
            self.is_executing = False
        
    def go_back(self, duration:int = 0, mode:str="top_left"):

        """
        Changes the current displayed view to one in the past

        """
        if self.is_executing:
            return
        if len(self.prev_views) > 0:
            self.view_go(self.prev_views[-1], back=True, duration=duration, mode=mode)
        else:
            first_view = next(iter(self.views))
            self.view_go(first_view, duration=duration, mode=mode)
            self.prev_views =[]
        
    def clear(self):
        """
        Clears back history
        """
        self.prev_views = [];
    
    def append(self, view_name:str, controls, update:bool = True):
        """
        Adds a control or a list of controls to a specific view. 
        If the working view is the same as the argument, behaves like the wadd method.

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
            else:
                self.views[view_name].controls.append(controls)
            if update: 
                self.page.update()

        else:
            raise ValueError(f"{view_name} is not a view of this FleetingViews")
        
    def wadd(self, controls, update:bool=True):
        """
        Adds a control or a list of controls to the working view. 


        Args:
            controls (Union[Control, List[Control]]): The control or list of controls to add.

        Raises:
            ValueError: If the view name is not in the views dictionary.
        """
        if isinstance(controls, list):
            for control in controls:
                self.working_view.controls.append(control)
        else:
            self.working_view.controls.append(controls)
        if update:
            self.page.update()
        
    def set_working(self, view_name):
        """
        Sets the working view for wadd calls.

        Args:
            view_name (str): The name of the view to set as working.

        Raises:
            ValueError: If the view name is not in the views dictionary or if the name is not an str.
        """
        view_name = view_name.lower()
        if isinstance(view_name, str):
            if view_name in self.views.keys():
                self.working_view = self.views[view_name]
            else:
                raise ValueError(f"{view_name} is not a view of this FleetingViews")
        else:
            raise ValueError(f"{view_name} is not a string")
        self.page.update()

    def animation(self, duration, next_view_name, mode:str="top_left"):
        """
        Creates an animation for the chaning view action

        Args:
            duration (int): The duration in miliseconds of the transition.
            next_view_name (str): The name of the traveling to view.
            mode (str): The animation mode for the view transition.

        Raises:
            ValueError: If the animation mode is not a valid key in the animation dict.
        """
        animation_modes = {"left":[0,-self.page.window.width],
                   "bottom": [self.page.window.height,0],
                   "top":[-self.page.window.height,0],
                   "right": [0,self.page.window.width],
                    "bottom_right": [self.page.window.height, self.page.window.width],
                    "bottom_left": [self.page.window.height, -self.page.window.width],
                    "top_right": [-self.page.window.height, self.page.window.width],
                    "top_left": [-self.page.window.height, -self.page.window.width],
                   }
        original_controls = self.actual_view.controls
        original_controls_next = self.views[next_view_name].controls
        original_padding =  self.actual_view.padding
        self.views[next_view_name].controls = []
        if not mode in animation_modes.keys():
            raise ValueError(f"{mode} is not a valid animation mode of FleetingViews")

        #Animation container
        envelop = ft.Stack(
                    width=self.page.window.width,
                    height=self.page.window.height,
                    controls=[ft.Container( 
                                    content=(ft.Column(
                                                    controls=original_controls_next,
                                                    alignment=self.views[next_view_name].vertical_alignment,
                                                    horizontal_alignment=self.views[next_view_name].horizontal_alignment,
                                                    spacing=self.views[next_view_name].spacing,
                                                    height=self.page.window.height-self.views[next_view_name].padding.top-self.views[next_view_name].padding.bottom,
                                                    width=self.page.window.width-self.views[next_view_name].padding.right-self.views[next_view_name].padding.left,

                                    )),
                                    width=self.page.window.width,
                                    height=self.page.window.height-self.views[next_view_name].padding.top-self.views[next_view_name].padding.bottom,
                                    bgcolor=self.views[next_view_name].bgcolor,
                                    margin=0,
                                    animate_position=ft.animation.Animation(duration-10, ft.animation.AnimationCurve.LINEAR),
                                    top=animation_modes[mode][0],
                                    left=animation_modes[mode][1],
                                    alignment=ft.alignment.center,
                                    padding=self.views[next_view_name].padding
                                    
                                    )],
                    )
        
        #Setting of the temporal phasing view
        self.actual_view.padding = 0
        self.actual_view.controls = [envelop]
        self.page.update()
        time.sleep(0.05)
        envelop.controls[0].left = -self.views[next_view_name].padding.left
        envelop.controls[0].top = -self.views[next_view_name].padding.top - self.views[next_view_name].padding.bottom
        self.page.update()
        time.sleep(duration/1000)
        self.actual_view.controls = []
        self.views[next_view_name].controls = []

        for control in original_controls_next:
            self.views[next_view_name].controls.append(control)

        #Restorationg of initial values
        self.actual_view.padding = original_padding
        self.actual_view.controls = original_controls



                    
                    

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

