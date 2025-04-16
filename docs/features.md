# Features 

## V(0.1.0)

### 1. Automatic View Creation with Customized Design: 
Quickly create views with specified settings, including background colors, alignments, and other attributes.

### 2. View History for "Back" Calls: 
Navigate back to previous views effortlessly, enhancing the user experience.

### 3. Custom Append Methods: 
Easily add controls to specific views with custom appends methods.

### 4. Clear Method: 
Reset the view history with a simple clear method.

## V(0.1.2)

### View Change Custom Animations!
Easily add transitions for any `view_go()` call with custom duration and modes.

### Customizable `page.update()` Calls for Page Building in the Background
Now you are able to add controls in the "background" without updating the page by setting update=False on `wadd()` and `append()` methods.

## V(0.1.8)

### 1. Query Parameters for Dynamic Views!
Easily pass and retrieve query parameters in your views using `get_param("param_name", "Default if not existent")` or `get_params()`. Customize views based on URL parameters for a more dynamic user experience. 🧩
Example:
```python
# Retrieve a query parameter
param = fv.get_param("param_name", default_value)

#Retrieve all parameters
params = fv.get_params()
```

### 2. Shared Data Between Views!
Share data across multiple views with a single FleetingViews instance. The shared data object can hold any values or objects that need to persist between views. Example:
```python
# Set shared data
fv.set_shared("user_info", {"name": "John", "age": 30})

# Retrieve shared data in a different view
user_info = fv.get_shared("user_info", default_value)

```

### 3. Enhanced View Navigation with URL Parameters!
The `view_go()` method now supports URL parameters, making it easier to navigate to views with specific configurations or user data embedded in the URL. Example:
```python
fv.view_go("settings?theme=dark&lang=en")
```

### 4. Improved `go_back()` Handling with Parameters!
The `go_back()` method now remembers not only the view but also any query parameters, making it easier to return to a specific state in your application.


### 5. Added Lifecycle Hooks!
FleetingViews now supports lifecycle hooks, allowing you to add custom behavior when views are mounted or unmounted. Use `on_mount` and `on_dismount` hooks to manage side effects such as fetching data, setting states, or cleaning up resources when switching between views. Example:

You can do it in the very definitions of your views:
```python
def my_on_mount_hook(ctx):
    print(f"Hello page {ctx.actual_view.route} {ctx._query_params}")
# View definitions with specific configurations
view_definitions = {
    "home": {
        "bgcolor": ft.colors.BLUE_GREY,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
        "on_mount": my_on_mount_hook
    },
    "settings": {
        "bgcolor": ft.colors.AMBER_900,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }

}
```
Or you can add more callables during execution!.
```python
def my_on_mount_hook(ctx):
    print(f"Hello page {ctx.actual_view.route} {ctx._query_params}")
# View definitions with specific configurations
view_definitions = {
    "home": {
        "bgcolor": ft.colors.BLUE_GREY,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    },
    "settings": {
        "bgcolor": ft.colors.AMBER_900,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }

}

fv = fleetingViews.create_views(view_definitions=view_definitions, page=page)

fv.add_hooks_or_guards("home", {"on_mount": my_on_mount_hook})
```
### Notes
* You can use `fv.add_hooks_or_guards()` to attach one or multiple callables to a view’s `on_mount`, `on_dismount`, or `guards` lifecycle events.  
Check the full documentation for usage examples and more details!


### 6. Missing Page Handling!
When navigating to a view that doesn’t exist, FleetingViews now handles missing pages gracefully by redirecting users to a fallback page you configure.
```python
fv.view_go("non_existent_page")
```

By default, this will automatically redirect to the special "404_not_found" view, which comes with a default error message (similar to common hosting platforms) and a button that sends the user back to the root view.

This handler is *always* created unless explicitly disabled:
```python
 fv = fleetingViews.create_views(view_definitions=view_definitions, page=page, fallback_404=False)
```

Of course, you can fully customize the "404_not_found" page just like any other view:
```python
view_definitions = {
    'home': {
        'bgcolor': ft.Colors.BLUE_GREY,
        'vertical_alignment': ft.MainAxisAlignment.CENTER,
        'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
        "appbar": appbar,
        "on_mount": my_on_mount_hook
    },
    ###EDITION OF NOT FOUND VIEW
    '404_not_found': {
        'bgcolor': ft.Colors.RED_300,
        'vertical_alignment': ft.MainAxisAlignment.CENTER,
        'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
        "controls": [                ft.Text("Oops! This page doesn't exist (404)", size=30, weight="bold", color=ft.Colors.BLACK),
            ft.Text("Please check the URL or go back to a known view.",color=ft.Colors.BLACK)],
        "appbar": appbar,
    },
}
```

### 7. Added `on_view_change` handler
You can now define an `on_view_change` callback that gets executed **every time the active view changes**, regardless of where the navigation came from.

This is useful for analytics, layout adjustments, logging, or global effects when the view changes.

> ⚠️ For maintainability reasons, only **one** `on_view_change` handler is allowed. It should be a single callable function.

Example:

```python
def my_global_view_change_handler(view_name: str, params):
    print(f"Changed to view: {view_name} with params: {params}")

fv.on_view_change = my_global_view_change_handler
```