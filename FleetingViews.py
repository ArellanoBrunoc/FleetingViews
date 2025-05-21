import flet as ft
import time
import json
import urllib



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
        self._query_params = {}
        self.shared_data = {}
        self.guards = {}
        self.on_view_change = None
        self.fallback_404 = False
        
    def update_view(self, view_name: str, param, value=None, update: bool = True):
        """
        Sets one or more parameters for a given view.

        Args:
            view_name (str): The name of the view to modify.
            param (str | dict): A single parameter name as string, or a dictionary of parameter-value pairs.
            value: The value to assign if a single parameter is passed.
            update (bool): Whether to trigger a page update after setting the parameter(s). Default is True.

        Raises:
            ValueError: If the view does not exist or any parameter is invalid.

        Example:
            views.set_view_param('home', 'bgcolor', ft.Colors.RED)
            views.set_view_param('home', {'bgcolor': ft.Colors.RED, 'appbar': my_appbar})
        """
        if view_name not in self.views:
            raise ValueError(f"View '{view_name}' does not exist.")

        view = self.views[view_name]

        if isinstance(param, dict):
            for key, val in param.items():
                if not hasattr(view, key):
                    raise ValueError(f"Invalid parameter '{key}' for view '{view_name}'.")
                setattr(view, key, val)
        else:
            if not hasattr(view, param):
                raise ValueError(f"Invalid parameter '{param}' for view '{view_name}'.")
            setattr(view, param, value)

        if update:
            self.page.update()

    def get_all_views(self):
        """
        Returns a list of all view names currently defined in the FleetingViews instance.

        Returns:
            list: A list of view names (strings) that are currently registered.

        Example:
            all_views = views.get_all_views()
            print(all_views)
        
        Returns a list of strings representing the names (routes) of all defined views.
        """
        return list(self.views.keys())

    def get_actual_view_name(self):
        """
        Retrieves the name of the current view being displayed.

        This method accesses the `route` property of the current `actual_view` and returns it,
        which can be useful to track or log the current view in the application.

        Returns:
            str: The route (name) of the current view.

        Example:
            current_view_name = views.get_actual_view_name()
            print(current_view_name)
        
        Returns the name of the active view, which corresponds to the route associated with it.
        """
        return self.actual_view.route

    def get_shared(self, key: str, default=None):
        """
        Retrieves the value associated with the given key from the shared data.

        If the key is not found in the shared data, a KeyError is raised, and a custom message is printed.
        If the key is not found, the method returns the default value provided.

        Args:
            key (str): The key to look up in the shared data.
            default: The value to return if the key is not found. Defaults to None.

        Returns:
            The value associated with the given key, or the default value if the key is not found.

        Example:
            shared_value = views.get_shared('user_data', default='No data')
            print(shared_value)
        
        Prints a custom message in case of a missing key, and returns the default value.
        """
        try:
            return self.shared_data[key]
        except KeyError:
            print(f"KeyError {key} is not a valid key in this FleetingViews shared data")
            return default

    def set_shared(self, key: str, value):
        """
        Sets the value for the specified key in the shared data.

        This method allows you to store data globally accessible across views within the application.

        Args:
            key (str): The key to associate with the value.
            value: The value to store under the provided key.

        Example:
            views.set_shared('user_data', {'name': 'John', 'age': 30})
        
        Stores the data for 'user_data' in the shared data.
        """
        self.shared_data[key] = value

    def save_data_to_json(self, path="shared_data.json"):
        """
        saves shared states in a json
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.shared_data, f, ensure_ascii=False, indent=4)

    def load_data_from_json(self, path="shared_data.json"):
        """
        saves shared states of an specific data.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.shared_data = json.load(f)
        except FileNotFoundError:
            self.shared_data = {}

    def get_param(self, key, default=None):
        """
        Returns the value of a query parameter or default if not found.
        """
        return self._query_params.get(key, default)

    def get_params(self):
        """
        Returns the full dictionary of current query parameters.
        """
        return self._query_params.copy()
    
    def remove_hooks_or_guards(self, view_name: str, hooks_or_guards: dict) -> None:
        """
        Removes specified hooks or guards from an existing view.

        Parameters:
            view_name (str): The name of the view from which hooks or guards should be removed.
            hooks_or_guards (dict): A dictionary where keys can be 'on_mount', 'on_dismount', or 'guards',
                                    and values can be a single function or a list of functions to remove.
        """
        view = self.views.get(view_name.lower())
        if not view:
            raise ValueError(f"View '{view_name}' not found.")

        def _remove_from_attr(attr_name: str, funcs_to_remove):
            current = getattr(view, attr_name, [])
            if not isinstance(current, list):
                current = [current] if callable(current) else []

            if not isinstance(funcs_to_remove, list):
                funcs_to_remove = [funcs_to_remove]

            filtered = [f for f in current if f not in funcs_to_remove]
            setattr(view, attr_name, filtered)

        valid_keys = {
            "on_mount": "__on_mount__",
            "on_dismount": "__on_dismount__",
            "guards": "__guards__"
        }

        for key, funcs in hooks_or_guards.items():
            if key not in valid_keys:
                raise ValueError(f"Invalid hook/guard key: '{key}'. Must be one of {list(valid_keys.keys())}.")
            _remove_from_attr(valid_keys[key], funcs)

    def add_hooks_or_guards(self, view_name: str, hooks_or_guards: dict) -> None:
        """
        Adds additional hooks or guards to the existing view.

        Parameters:
            view_name (str): The name of the view to which hooks or guards should be added.
            hooks_or_guards (dict): A dictionary containing the hooks or guards to be added. 
                                    Keys can be 'on_mount', 'on_dismount', or 'guards'.
                                    Values can be a single function or a list of functions.
        """
        view = self.views.get(view_name.lower())
        if not view:
            raise ValueError(f"View '{view_name}' not found.")

        def _extend_attr(attr_name: str, new_funcs):
            existing = getattr(view, attr_name, [])
            if not isinstance(existing, list):
                existing = [existing] if callable(existing) else []
            if not isinstance(new_funcs, list):
                new_funcs = [new_funcs]
            existing.extend(new_funcs)
            setattr(view, attr_name, existing)

        valid_keys = {
            "on_mount": "__on_mount__",
            "on_dismount": "__on_dismount__",
            "guards": "__guards__"
        }

        for key, funcs in hooks_or_guards.items():
            if key not in valid_keys:
                raise ValueError(f"Invalid hook/guard key: '{key}'. Must be one of {list(valid_keys.keys())}.")
            _extend_attr(valid_keys[key], funcs)



    
    def _run_hook(self, hook, context=None):
        """
        Parameters:

        hook (Callable or List[Callable]):
        A single function or a list of functions to be executed. Each function should accept a Context object as its only argument.
        If None is passed, the function does nothing.

        ctx (Context):
        The context object that provides information about the current view state, including parameters, view route, and more.

        Behavior:

        If hook is None, the function returns immediately.

        If hook is a list, it runs all functions in order, passing ctx to each one.

        If hook is a single function, it is simply called with ctx.
        """
        try:

            if hook is None:
                return  
            
            if isinstance(hook, list):
 
                if not all(callable(fn) for fn in hook):
                    raise TypeError(f"Todos los elementos de la lista 'hook' deben ser funciones. Se encontró un valor no callable.")
                

                for fn in hook:
                    self._run_hook(fn, context) 


            elif callable(hook):

                if hook.__code__.co_argcount == 0:
                    hook() 
                else:
                    hook(context)  
            else:

                raise TypeError(f"'hook' value must be a function or a list of functions. Found: {type(hook)}")

        except Exception as e:
            print(f"[FleetingViews] Error en hook: {e}")



    def _run_guards(self, name: str) -> bool:
        if name not in self.views:
            return True
        
        guards = getattr(self.views[name], "__guards__", None)
        if not guards:
            return True

        if callable(guards):
            guard_name = getattr(guards, "__name__", str(guards))
            if not guards(self, name):
                print(f"Guard '{guard_name}' blocked navigation to {name}")
                return False

        elif isinstance(guards, list):
            for guard_func in guards:
                if not callable(guard_func):
                    raise TypeError(f"Each guard must be a callable function. Found: {type(guard_func)}")
                guard_name = getattr(guard_func, "__name__", str(guard_func))
                if not guard_func(self, name):
                    print(f"Guard '{guard_name}' blocked navigation to {name}")
                    return False

        else:
            raise TypeError(f"'__guards__' must be a callable or a list of callables. Found: {type(guards)}")

        return True


    def view_go(self, view_name: str, back: bool = False, duration: int = 0, mode: str = "top_left", history_debug:bool = False):
        if self.is_executing:
            return
        self.is_executing = True

        
        try:

            if '?' in view_name:
                name, query = view_name.split('?', 1)
                self._query_params = dict(urllib.parse.parse_qsl(query))
            else:
                name = view_name
                self._query_params = {}

            name = name.lower()
            
            if not self._run_guards(name):
                self.is_executing = False
                return
            
            if name in self.views:
    

                next_view = self.views[name]

                if self.actual_view == next_view:
                    return
                
                if hasattr(self.actual_view, "__on_dismount__"):
                    self._run_hook(getattr(self.actual_view, "__on_dismount__"), self)

                if duration > 0:
                    self.animation(duration, next_view_name=name, mode=mode)

                try:
                    view_index = self.page.views.index(next_view)
                    self.page.views.pop(view_index)
                except ValueError:

                    pass

                self.page.views.append(next_view)


                
                if not back and self.actual_view:
                    actual_route = self.actual_view.route if self.actual_view else None
                    next_route = next_view.route

                   
                    self.prev_views = [view for view in self.prev_views if view["view_name"] != next_route]


                    is_actual_in_history = any(view["view_name"] == actual_route for view in self.prev_views)

                    if not is_actual_in_history and actual_route and actual_route != "404_not_found":
                        self.prev_views.append({
                            "view_name": actual_route,
                            "params": self._query_params,
                        })
                    if history_debug:
                        print("🔙 Updated history:", self.prev_views)

                self.actual_view = next_view
                self.page.update()

                if hasattr(next_view, "__on_mount__"):
                    self._run_hook(getattr(next_view, "__on_mount__"), self)

                if callable(self.on_view_change):
                    self.on_view_change(name, self._query_params)
            else:
                if not "404_not_found" in self.views:
                    raise ValueError(f"{name} is not a view of this FleetingViews")
                else:
                    self.is_executing = False
                    self.view_go("404_not_found")
        finally:
            self.is_executing = False
       
    def go_back(self, duration: int = 0, mode: str = "top_left", history_debug:bool= False):
        """
        Navega a la vista anterior usando el historial.
        Si no hay historial, va a la primera vista registrada.
        """
        if self.is_executing:
            return

        if len(self.prev_views) > 0:
            last_view = self.prev_views.pop()  
            if history_debug:
                print("⏪ Going back to:", last_view)

            view_name = last_view["view_name"]
            params = last_view.get("params", {})
            if params:
                query_string = "&".join([f"{key}={value}" for key, value in params.items()])
                view_name = f"{view_name}?{query_string}"

            self.view_go(view_name, back=True, duration=duration, mode=mode)
        else:
            
            first_view = next(iter(self.views))
            self.prev_views = []  
            self.view_go(first_view, duration=duration, mode=mode)


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

    def open_drawer(self, drawer, position: str = "start"):
        """
        Opens the specified drawer on the given position ('start' or 'end') of the current view.

        Args:
            drawer: The drawer component (start or end) to open.
            position (str): Position of the drawer ('start' or 'end').

        Raises:
            ValueError: If the provided position is invalid.
        """
        if position == "start":
            if self.actual_view.drawer is None or self.actual_view.drawer != drawer:
                self.actual_view.drawer = drawer

            drawer.open = True
            self.page.update()

        elif position == "end":
            if self.actual_view.end_drawer is None or self.actual_view.end_drawer != drawer:
                self.actual_view.end_drawer = drawer

            drawer.open = True
            self.page.update()
        else:
            raise ValueError("Drawer position must be 'start' or 'end'.")

    def close_drawer(self, drawer, position: str = "start"):
        """
        Closes the specified drawer on the given position ('start' or 'end') of the current view.

        Args:
            drawer: The drawer component (start or end) to close.
            position (str): Position of the drawer ('start' or 'end').

        Raises:
            ValueError: If the provided position is invalid.
        """
        if position == "start":
            if self.actual_view.drawer is None or self.actual_view.drawer != drawer:
                self.actual_view.drawer = drawer

            drawer.open = False
            self.page.update()

        elif position == "end":
            if self.actual_view.end_drawer is None or self.actual_view.end_drawer != drawer:
                self.actual_view.end_drawer = drawer

            drawer.open = False
            self.page.update()
        else:
            raise ValueError("Drawer position must be 'start' or 'end'.")

    def toggle_drawer(self, drawer, position: str = "start"):
        """
        Toggles the state of the specified drawer (open if closed, closed if open) on the given position ('start' or 'end') of the current view.

        Args:
            drawer: The drawer component (start or end) to toggle.
            position (str): Position of the drawer ('start' or 'end').

        Raises:
            ValueError: If the provided position is invalid.
        """
        if position == "start":
            if self.actual_view.drawer is None or self.actual_view.drawer != drawer:
                self.actual_view.drawer = drawer

            # Toggle drawer state
            drawer.open = not drawer.open
            self.page.update()

        elif position == "end":
            if self.actual_view.end_drawer is None or self.actual_view.end_drawer != drawer:
                self.actual_view.end_drawer = drawer

            # Toggle drawer state
            drawer.open = not drawer.open
            self.page.update()
        else:
            raise ValueError("Drawer position must be 'start' or 'end'.")

                    
                    

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


def create_views(view_definitions: dict, page: ft.Page, fallback_404: bool = True, direct = True):
    """
    Adds a control or a list of controls to a specific view. 
    If the working view is the same as the argument, behaves like the append method.

    Args:
        view_definitions (dict): Diccionario de definiciones para cada vista.
        page (flet.Page): Página Flet donde se montan las vistas.
        fallback_404 (bool): Si es True, añade una vista por defecto para rutas no encontradas ('404_not_found').

    Returns:
        FleetingViews: Objeto para gestionar la navegación y ciclo de vida de las vistas.
    """
    page.views.pop(0)

    # Validación
    for view_name, view_args in view_definitions.items():
        if not isinstance(view_name, str) or ' ' in view_name:
            raise ValueError("All names of views must be strings without spaces.")
        if not isinstance(view_args, dict):
            raise ValueError("Each view definition must be a dictionary with argument names and values.")

    views_dict = {}
    for view_name, view_args in view_definitions.items():
        # Extraer hooks si están definidos
        on_mount = view_args.pop("on_mount", None)
        on_dismount = view_args.pop("on_dismount", None)
        guards = view_args.pop("guards", None)

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

        # Hooks y guards
        if on_mount:
            setattr(views_dict[view_name.lower()], "__on_mount__", on_mount)
        if on_dismount:
            setattr(views_dict[view_name.lower()], "__on_dismount__", on_dismount)
        if guards:
            setattr(views_dict[view_name.lower()], "__guards__", guards)

    button_back =  ft.IconButton(icon=ft.Icons.ARROW_CIRCLE_LEFT_ROUNDED, icon_size=30, icon_color=ft.Colors.BLACK, on_click=lambda e: fv.view_go(next(iter(fv.views))))
    # Vista 404 por defecto si se solicita
    if fallback_404 and "404_not_found" not in views_dict:
        
        views_dict["404_not_found"] = create_custom_view(
            route="404_not_found",
            bgcolor=ft.Colors.RED_100,
            controls=[
                ft.Text("Oops! This page doesn't exist (404)", size=30, weight="bold", color=ft.Colors.BLACK),
                ft.Text("Please check the URL or go back to a known view.",color=ft.Colors.BLACK),
                button_back
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            auto_scroll=True,
            spacing=20,
            padding=ft.padding.all(40),
        )
        initialize_view(views_dict["404_not_found"], page)


            
    fv = FleetingViews(page, views_dict)
    first_view = next(iter(fv.views))
    if direct:
        fv.view_go(first_view)
    
    if fallback_404:
        button_back.on_click = lambda e: fv.view_go(first_view)
    

    fv.prev_views = []
    return fv

