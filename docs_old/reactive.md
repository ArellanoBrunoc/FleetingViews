# 🔁 Reactive Observables & Two-Way Binding (v0.2)

FleetingViews introduces a built-in **reactivity system** in v0.2, allowing you to declare shared observable values and create dynamic interfaces that respond automatically to user input or programmatic changes.

---

## 📦 Observable Values

You can declare values that are shared and watched across different parts of your app.

```python
dfv.define_observable("username", "Guest")
```

Once defined, this value can be subscribed to by any number of controls or logic handlers.

---

## 👀 Subscribing to Changes

You can subscribe any control (that has a `.value`) or function to an observable key. When the value changes, all subscribers are updated.

```python
username_label = ft.Text()
dfv.subscribe("username", username_label)

# This updates the label automatically:
dfv.set_observable("username", "Bruno")
```

You can also provide a handler function:

```python
def on_username_change(value):
    print("New username:", value)

dfv.subscribe("username", handler=on_username_change)
```

Or both:

```python
dfv.subscribe("username", username_label, handler=on_username_change)
```

---

## 🔁 Two-Way Data Binding

The `bind_to_control()` method creates a reactive link **in both directions** between a control (e.g. `TextField`) and an observable key.

```python
input_name = ft.TextField()
dfv.bind_to_control("username", input_name)
```

Now:

- Changing the field updates the observable.
- Updating the observable updates the field.

You can bind multiple controls to the same key:

```python
fv.bind_to_control("email", email_input)
fv.subscribe("email", email_preview)
```

---

## 🔄 Unsubscribing and Unbinding

### Unsubscribe a control or function:

```python
dfv.unsubscribe("username", username_label)
dfv.unsubscribe("username", on_username_change)
```

### Unbind a two-way binding:

```python
dfv.unbind_control("username", input_name)
```

This removes both the subscription and the `on_change` listener from the control.

---

## 📚 Full Lifecycle Example

```python
fv.define_observable("username", "")

input_field = ft.TextField()
output_text = ft.Text()

fv.bind_to_control("username", input_field)
fv.subscribe("username", output_text)

# Result:
# Typing in the input updates the observable and the text
# Updating the observable updates both
fv.set_observable("username", "Bruno")
```

---

## 🧠 Why Use Reactive Observables?

- Clean separation of logic and presentation
- Auto-update UI from data, and vice versa
- No need to manually call `.update()` on multiple elements
- Centralized state with full reactivity

This makes it easier to build forms, settings pages, dashboards, and any interface where state and UI must stay in sync.

## 🧩 Coming Soon (v0.2.1+)

- `define_computed()` for derived values
- `watch()` and `watch_many()` to react to multiple observables
- Persistence with `enable_persistence()`

> Reactive state in FleetingViews brings frontend-like power to Python + Flet, without complexity.

