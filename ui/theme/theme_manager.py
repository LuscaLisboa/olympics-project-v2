import tkinter as tk
from tkinter import ttk

from ui.theme.themes import ThemeType
from ui.theme.themes import THEMES

"""
Theme system for App
Support multiples themes & permit easy customization
"""


class ThemeManager:
    """Centralized theme manager"""

    def __init__(self, root: tk.Tk, initial_theme: ThemeType = "light"):
        self.root = root
        self.current_theme: ThemeType = initial_theme
        self.observers = []
        self._setup_ttk_style()
        self.apply_theme(initial_theme)

    def _setup_ttk_style(self):
        """TTK personalized style config"""
        self.style = ttk.Style()

        available_themes = self.style.theme_names()
        if "clam" in available_themes:
            self.style.theme_use("clam")
        elif "alt" in available_themes:
            self.style.theme_use("alt")

    def apply_theme(self, theme_name: ThemeType):
        """Apply theme to app"""
        self.current_theme = theme_name
        colors = THEMES[theme_name]

        #   root
        self.root.configure(bg=colors["bg"])

        #   TTK configs
        self.style.configure(
            ".",
            background=colors["bg"],
            foreground=colors["text_primary"],
            bordercolor=colors["border"],
            darkcolor=colors["surface_hover"],
            lightcolor=colors["surface"],
            troughcolor=colors["surface"],
            selectbackground=colors["primary"],
            selectforeground=colors["text_on_primary"],
            fieldbackground=colors["surface"],
        )

        #   Frame
        self.style.configure("TFrame", background=colors["bg"])
        self.style.configure("Card.TFrame", background=colors["bg"], borderwidth=1, relief="flat")

        #   Label
        self.style.configure("TLabel", background=colors["bg"], foreground=colors["text_primary"], font=("Segoe UI", 20, "bold"))
        self.style.configure("Title.TLabel", background=colors["bg"], foreground=colors["text_primary"], font=("Segoe UI", 20, "bold"))
        self.style.configure("Subtitle.TLabel", background=colors["bg"], foreground=colors["text_primary"], font=("Segoe UI", 10, "bold"))
        self.style.configure("Card.TLabel", background=colors["bg"], foreground=colors["text_primary"])
        self.style.configure("CardTitle.TLabel", background=colors["bg"], foreground=colors["text_primary"], font=("Segoe UI", 12, "bold"))
        self.style.configure("Info.TLabel", background=colors["bg"], foreground=colors["text_primary"], font=("Segoe UI", 9))

        #   Button
        self.style.configure("TButton",
            background=colors["surface"],
            foreground=colors["text_primary"],
            borderwidth=0,
            focuscolor=colors["surface_hover"],
            font=("Segoe UI", 9),
            padding=(16, 8)
        )
        self.style.map("TButton",
            background=[
                ("active", colors["surface_hover"]),
                ("disabled", colors["secondary"]),
            ],
            foreground=[
                ("disabled", colors["text_secondary"]),
            ],
        )
        self.style.configure("Secondary.TButton",
            background=colors["surface"],
            foreground=colors["text_primary"],
            borderwidth=1,
        )
        self.style.map("Secondary.TButton",
            background=[
                ("active", colors["surface_hover"]),
            ],
        )

        #   Treeview
        self.style.configure("Treeview",
            background=colors["table_row_even"],
            foreground=colors["text_primary"],
            fieldbackground=colors["surface"],
            borderwidth=0,
            font=("Segoe UI", 9),
        )
        self.style.configure("Treeview.Heading",
            background=colors["table_header"],
            foreground=colors["text_primary"],
            borderwidth=1,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
        )
        self.style.map("Treeview",
            background=[("selected", colors["primary"])],
            foreground=[("selected", colors["text_on_primary"])],
        )
        self.style.map("Treeview.Heading",
            background=[("active", colors["surface_hover"])],
        )

        # Notebook
        self.style.configure("TNotebook",
            background=colors["bg"],
            borderwidth=0,
        )
        self.style.configure("TNotebook.Tab",
            background=colors["surface"],
            foreground=colors["text_primary"],
            padding=(20, 10),
            borderwidth=0,
        )
        self.style.map("TNotebook.Tab",
            background=[
                ("selected", colors["primary"]),
                ("active", colors["surface_hover"]),
            ],
            foreground=[
                ("selected", colors["text_on_primary"]),
            ],
        )

        #   Scrollbar
        self.style.configure("Vertical.TScrollbar",
            background=colors["surface"],
            troughcolor=colors["bg"],
            borderwidth=0,
            arrowcolor=colors["text_secondary"],
        )
        self.style.configure("Horizontal.TScrollbar",
            background=colors["surface"],
            troughcolor=colors["bg"],
            borderwidth=0,
            arrowcolor=colors["text_secondary"],
        )

        self._notify_observers()

    def get_color(self, color_key: str) -> str:
        return THEMES[self.current_theme].get(color_key, "#000000")

    def get_all_colors(self) -> dict:
        return THEMES[self.current_theme].copy()

    def add_observer(self, callback):
        self.observers.append(callback)

    def _notify_observers(self):
        """Notify all observers"""
        for callback in self.observers:
            try:
                callback(self.current_theme)
            except Exception as e:
                print(f"Error notifying observers: {e}")

    def cycle_theme(self):
        """Cycle theme"""
        themes = list(THEMES.keys())
        current_idx = themes.index(self.current_theme)
        next_idx = (current_idx + 1) % len(themes)
        self.apply_theme(themes[next_idx])
