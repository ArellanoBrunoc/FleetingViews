# FleetingViews - Custom 404 Page Handling

## Missing Page Handling (404)

FleetingViews now gracefully handles missing pages by redirecting users to a fallback **404** page that you can configure. When a user attempts to navigate to a page that doesn't exist, FleetingViews automatically redirects to a 404 view.

### Default Behavior

If you try to navigate to a view that doesn’t exist, FleetingViews will automatically redirect to the `404_not_found` view, showing a standard error message and a button to return to the root view:

```python
fv.view_go("non_existent_page")
```

## Missing Page Handling (404)
You can fully customize the `404_not_found` view just like any other view. Here's an example of how to configure a 404 page with a message and a button to go back to the home page.

*Example of 404 View Definition*

```python
view_definitions = {
    'home': {
        'bgcolor': ft.Colors.BLUE_GREY,
        'vertical_alignment': ft.MainAxisAlignment.CENTER,
        'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
        "appbar": appbar,
    },
    # Customization of the 404 View
    '404_not_found': {
        'bgcolor': ft.Colors.RED_300,
        'vertical_alignment': ft.MainAxisAlignment.CENTER,
        'horizontal_alignment': ft.CrossAxisAlignment.CENTER,
        "controls": [
            ft.Text("Oops! This page doesn't exist (404)", size=30, weight="bold", color=ft.Colors.BLACK),
            ft.Text("Please check the URL or go back to a known view.", color=ft.Colors.BLACK),
            ft.ElevatedButton("Go to Home", on_click=lambda e: fv.view_go("home"))
        ],
        "appbar": appbar,
    },
}

```

*Creating the Views*
When creating the views, you can enable or disable the missing page handler with the fallback_404 parameter. If enabled, FleetingViews will automatically redirect to the `404_not_found` view when trying to access a non-existing page:

```python
fv = fleetingviews.create_views(view_definitions=view_definitions, page=page) #Fallback is true by default

```

If you prefer to disable the automatic 404 handling, simply set `fallback_404=False`:

```python
fv = fleetingviews.create_views(view_definitions=view_definitions, page=page, fallback_404=False)

```

## Important Note
If you disable the automatic 404 handler, attempting to navigate to a non-existent view will raise a `ValueError`:

```python
ValueError(f"{name} is not a view of this FleetingViews")
```

This ensures you are aware that the requested view is not valid.

This way, you can fully control how missing pages are handled in your application.