# 🔒 Hooks & Guards in FleetingViews (v0.1.8)

FleetingViews supports **lifecycle hooks** and **navigation guards** to help you manage your views' logic more dynamically and safely.

---

## 🪝 Lifecycle Hooks

You can attach functions to specific views that run **when the view is mounted or dismounted**. These functions are useful for initializing resources, fetching data, or cleaning up when navigating between views.

### Supported Hooks:
- `on_mount`: Runs **when the view is shown**.
- `on_dismount`: Runs **just before the view is hidden**.

Each of these can accept a single function or a **list of functions**, and will be executed in the order provided.

### Example

```python
def fetch_user_data(ctx):
    print("Fetching user data...")

def save_changes(ctx):
    print("Saving form changes...")

fv.add_hooks_or_guards("profile", {
    "on_mount": fetch_user_data,
    "on_dismount": save_changes,
})
```

You can also pass multiple functions:

```python
fv.add_hooks_or_guards("profile", {
    "on_mount": [func_a, func_b],
    "on_dismount": [cleanup1, cleanup2],
})

```

You can also define hooks directly inside your `view_definitions`:

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
### Notes:
* It is advised that the hooks are given a context argument to get useful information in the manager ex: `ctx._query_params` will give you the parameter, you can also use `ctx.get_params()`.
* You can't create hooks that receive more than `ctx`.

## `on_view_change` Hook:
You can now define an `on_view_change` callback that gets executed **every time the active view changes**, regardless of where the navigation came from.

This is useful for analytics, layout adjustments, logging, or global effects when the view changes.

> ⚠️ For maintainability reasons, only **one** `on_view_change` handler is allowed. It should be a single callable function.
> All guards must accept exactly two arguments: `view_name` and `params`

Example:

```python
def my_global_view_change_handler(view_name: str, params):
    print(f"Changed to view: {view_name} with params: {params}")

fv.on_view_change = my_global_view_change_handler
```


## 🛡️ Navigation Guards

Guards are functions that *run before changing to a specific view*. They determine whether or not the view transition should happen.

Each guard function must return `True` or `False`:

Return `True` to allow navigation.

Return `False` to prevent the view from being shown.

This is useful for authentication checks, permission validation, or confirming unsaved changes.

### Important
* ⚠️ If any of the guards return a `False`, the navigation is stopped and no hooks or events will be triggered.
* All guards must accept exactly two arguments: `ctx` and `name`.. `ctx` will be the `FleetingViews` manager and `name` the name of the view thats being evaluated.


### Example

```python
def is_user_logged_in(ctx, name):
    # Only allow access if the user is logged in
    return session.get("logged_in", False)

fv.add_hooks_or_guards("dashboard", {
    "guards": is_user_logged_in
})
```

As with hooks, you can add a list of them or define them in the `view_definitions`:

```python
def is_user_logged_in(ctx, name):
        # Only allow access if the user is logged in
    return session.get("logged_in", False)

# View definitions with specific configurations
view_definitions = {
    "home": {
        "bgcolor": ft.colors.BLUE_GREY,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
        "guards": is_user_logged_in
    },
    "settings": {
        "bgcolor": ft.colors.AMBER_900,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    }

}
```

### Full Lifecycle
Navigation attempt -> Run Guards -> [All True?] -> Run on_dismounts -> Change View -> Run on_mounts -> Run on_view_change