## Query Parameters (v0.1.8)

FleetingViews also allows you to pass and use **query parameters** in your views' URLs. These parameters can be used to store and retrieve dynamic information across different views.

### Example: Using Query Parameters

Let's say you want to pass some parameters like `user_id` or `theme` when navigating between views. You can easily achieve this using query strings.

#### Define Your Views with Query Parameters

You can use the `params` argument to pass query parameters. Here's an example of how to use query parameters when navigating to a specific view:

```python
# Define views with query parameters in the URL
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
    "profile": {
        "bgcolor": ft.colors.LIGHT_GREEN,
        "vertical_alignment": ft.MainAxisAlignment.CENTER,
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    },
}

# Create views
fv = fleetingviews.create_views(view_definitions=view_definitions, page=page)

# Navigate to 'profile' view with query parameters
fv.view_go("profile?user_id=123&theme=dark")
```

## Retrieving Query Parameters

Once you've navigated to a view with query parameters, you can access those parameters inside your view by using the getters on the FleetingViews instance.

```python
# Access query parameters inside the 'profile' view
    def profile_view(fv):
        user_id = fv.get_param("user_id", "guest")
        theme = fv.get_param("theme", "light")
    
    # Use the parameters in your view
    print(f"User ID: {user_id}")
    print(f"Theme: {theme}")

    # Add some controls or logic based on the parameters
    controls = [
        ft.Text(f"Welcome, {user_id}!"),
        ft.Text(f"Theme: {theme}"),
    ]
    fv.append("profile", controls)

```
### Notes
 * You can pass multiple query parameters in the URL by separating them with `&`.
 * The `get_param()` method is used to retrieve the parameters. If the parameter does not exist, you can provide a default value.
 * Query parameters are a great way to make your views more dynamic and customizable based on user input or application state.
 * FleetingViews `go_back()` method remembers not only the page and state, but also the parameters if they were given!
 * Parameters are available as soon as `view_go()` is triggered, even before guards are evaluated!
 