![FleetingViews Logo](logo.png)

# Welcome to FleetingViews 👋

**FleetingViews** is a lightweight but powerful utility class that simplifies **view management** in [Flet](https://flet.dev) applications.  
Inspired by modern frontend routing systems, FleetingViews provides tools to **create, switch, animate, and control** views with ease—no boilerplate, no fuss.

---

## ✨ Features (v0.1.8)

- 🚀 Easy view declaration and dynamic navigation
- 🧭 Built-in navigation history with `go_back()`
- 🧱 Add controls dynamically from views
- 🎭 Animated transitions between views
- 🧩 Lifecycle hooks (`on_mount`, `on_dismount`, `on_view_change`)
- 🛡️ Guard functions to protect certain views
- 🧃 Support for drawers, FABs, AppBars.
- 🧩 Easy to modularize view definitions and logic
- 🌐 Easily pass and handle query parameters in views with FleetingViews
- 🔄 Seamlessly share data across views and components with FleetingViews

✨ Features (v0.2)

    ⚡ Reactive Observables with define_observable() and subscribe()

    🔁 Two-Way Data Binding with bind_to_control()
    Easily sync TextField, Dropdown, and similar inputs with shared state

    🔂 unsubscribe() and unbind_control() to fully detach views or handlers

    🧠 Mix UI and logic: auto-update controls, trigger functions, or both

    🧪 Clean reactive flow: write once, update everywhere

    🔧 Prepares ground for computed values, watchers, and persistence (coming soon)
---

## 📦 Installation

```bash
pip install fleetingviews
```
## ❓ Why FleetingViews?

Managing multiple views in a Flet app can quickly get messy.  
**FleetingViews** helps you:

- 🧹 Organize your views declaratively
- 🔄 Handle transitions and user navigation easily
- 🧠 Inject custom behavior with guards and hooks
- 🧑‍💻 Focus on your app logic, not view plumbing

> “With FleetingViews, you think about *what* your app does not *how* to juggle UI blocks.”


#### [Repository](https://github.com/ArellanoBrunoc/FleetingViews)