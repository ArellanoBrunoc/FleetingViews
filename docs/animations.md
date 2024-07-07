# Animations

## Availible from V0.1.1

This version of FleetingViews now enables view transitions with customizable position and duration for every 'view_go' and "go_back" call.

For example, let's initialize some views in our project:

```python
    # View definitions with specific configurations
    view_definitions = {
            'home': {
                'bgcolor': ft.colors.RED,
                'vertical_alignment': ft.MainAxisAlignment.CENTER,
                'horizontal_alignment': ft.CrossAxisAlignment.CENTER
            },
            'projects': {
                'bgcolor': ft.colors.PURPLE,
            }
        }

    fv = fleetingviews.create_views(view_definitions=view_definitions, page=page)
```

Now, all that is left is to call one of the methods as follows:

```python
    fv.view_go("projects", duration=300)
```

By adding the duration parameter with a value above 0, FleetingViews will know that the call is intended to have an animation that lasts `duration` milliseconds.

You can also declare the animation mode that you prefer from the options below:

### 1. top_left (default)
### 2. top
### 3. top_right
### 4. right
### 5. bottom_right
### 6. bottom
### 7. bottom_left
### 8. left

```python
    #For example
    fv.view_go("projects", duration=300, mode="right")
```