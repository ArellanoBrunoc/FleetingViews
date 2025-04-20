# Getting Started

## Installation

To install FleetingViews, run
```bash
pip install fleetingviews
```
To upgrade to the latest version:

```bash
pip install fleetingviews --upgrade
```

## Import
```python
import FleetingViews as fleetingviews
```
## Defining Your Views

Start by defining your views using a simple dictionary structure. Each key is a view name, and its value is a dictionary of view-specific configurations.

```python
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
    },
    "projects": {
        "bgcolor": ft.colors.BLACK,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    },
}
```
### Notes
 * This is the most basic example. We'll cover more advanced definitions later on.
 * Any omitted argument will fall back to Flet’s default values.
 * You can declare views in any order, but the first one will be treated as the root view (i.e., the default entry point of your app).

## Initializing FleetingViews

Once you’ve defined your views, create a FleetingViews object:
```python
fv = fleetingviews.create_views(view_definitions=view_definitions, page=page)
```
That’s it! One line of code and your views are ready.

## Navigating Between Views
To navigate to any registered view, simply use:

```python
fv.view_go("name_of_view")
```
For example:
```python
fv.view_go("settings")
```
### Notes
* You can set `history_debug=True` as an argument to either `view_go()` or `go_back()` to print the navigation flow and see exactly how the history is being handled in your app.
```python
fv.view_go("settings", history_debug=True)
fv.go_back(history_debug=True)
```

## Adding controls to views
FleetingViews supports two convenient methods for adding controls:

1. `append()`
    This method adds one or more controls to a specific view:

    ```python
    fv.append("view_name", controls)
    ```
    `controls` can be:

    * A single Flet control (e.g. `ft.Text("Hello")`)
    * A list of controls (e.g. `[ft.Text("Hello"), ft.ElevatedButton("Click")]`)


2. `wadd()`:

    A shorthand method to add controls to the currently active working view:



    ```python
    fv.wadd(controls)
    ```
    This is ideal for building views in sequence without repeating the view name every time.

    If you want to change the working view (for all future `wadd()` calls) use:

    ```python
    fv.set_working("view_name")
    ```
    ### Notes
    * By default, the working view is the *last declared view*.
    * Use `fv.set_working("view_name")` to change the active working view for future wadd() calls.
    * Both methods automatically trigger `page.update()`, so no need to call it manually (you can avoid this behaviour by setting `update=False` on the arguments!).


## Going back
To return to the previous view:

```python
fv.go_back()
```
FleetingViews maintains a history of visited views. Once there's no more history, calling `go_back()` will return you to the root view.

If you want to reset *navigation history*, use:
```python
fv.clean()
```
This clears the navigation stack. The next `go_back()` will always lead to the root view.
## Basic FleetingViews design
Here’s a basic conceptual diagram of FleetingViews' routing system:

![Routing image](routing.png)


## Minimal working example

```python
import flet as ft
import FleetingViews as fleetingviews

def main(page: ft.Page):
    views = {
        "home": {"bgcolor": ft.colors.BLUE},
        "about": {"bgcolor": ft.colors.GREEN},
    }

    fv = fleetingviews.create_views(view_definitions=views, page=page)
    fv.set_working("home")
    fv.wadd(ft.Text("Welcome to the home page"))
    fv.set_working("about")
    fv.wadd(ft.Text("This is the about page"))

    fv.view_go("home")

ft.app(target=main)

```