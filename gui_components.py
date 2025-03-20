import tkinter as tk
from tkinter import ttk, colorchooser
from utils import find_matching_combinations, visualize_colors

class HexasnipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexasnipe GUI")
        self.root.geometry("800x600")
        
        self.mode = tk.StringVar(value="simple")
        self.allow_duplicates = tk.BooleanVar(value=False)
        self.category_rules = {}
        self.exact_count = tk.IntVar(value=0)
        self.target_color_var = tk.StringVar()
        self.categories = []
        self.components = []
        self.style_widgets()
        self.create_widgets()
    
    def style_widgets(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("Custom.TButton", background="#4CAF50", foreground="black", font=("Helvetica", 10, "bold"))
        style.configure("Custom.TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("Custom.TEntry", font=("Helvetica", 10))
        style.configure("Custom.TMenubutton", background="#4CAF50", foreground="black", font=("Helvetica", 10, "bold"))
        style.map("Colored.TEntry", fieldbackground=[("readonly", "#ffffff")])

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        mode_frame = ttk.Frame(main_frame, padding="10")
        mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        mode_frame.columnconfigure(0, weight=1)
        mode_frame.columnconfigure(1, weight=1)
        ttk.Button(mode_frame, text="Simple Mode", command=lambda: self.set_mode("simple")).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(mode_frame, text="Complex Mode", command=lambda: self.set_mode("complex")).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        target_frame = ttk.Frame(main_frame, padding="10")
        target_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        target_frame.columnconfigure(1, weight=1)
        ttk.Label(target_frame, text="Target Color: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.target_entry = ttk.Entry(target_frame, textvariable=self.target_color_var, width=10)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(target_frame, text="Pick", command=self.pick_target_color).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.options_frame = ttk.Frame(main_frame, padding="10")
        self.options_frame.grid(row=2, column=0, sticky="ew")
        self.options_frame.columnconfigure(0, weight=1)
        
        self.allow_duplicates_check = ttk.Checkbutton(self.options_frame, text="Allow Duplicates", variable=self.allow_duplicates)
        self.allow_duplicates_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.duplicate_label = ttk.Label(self.options_frame, text="", foreground="red")
        self.duplicate_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.options_frame, text="Exact Count:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.count_entry = ttk.Entry(self.options_frame, textvariable=self.exact_count, width=5)
        self.count_entry.grid(row=1, column=0, padx=(100, 5), pady=5, sticky="w")
        ttk.Button(self.options_frame, text="Set", command=self.update_exact_count).grid(row=1, column=0, padx=(150, 5), pady=5, sticky="w")
        
        self.category_canvas = tk.Canvas(main_frame, bg="#f0f0f0")
        self.category_canvas.grid(row=3, column=0, sticky="nsew")
        self.category_canvas.columnconfigure(0, weight=1)
        
        self.category_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.category_canvas.yview)
        self.category_scrollbar.grid(row=3, column=1, sticky="ns")
        
        self.category_canvas.configure(yscrollcommand=self.category_scrollbar.set)
        self.category_canvas.bind('<Configure>', lambda e: self.category_canvas.configure(scrollregion=self.category_canvas.bbox("all")))
        self.category_canvas.bind("<Enter>", lambda e: self._bind_mousewheel(self.category_canvas))
        self.category_canvas.bind("<Leave>", lambda e: self._unbind_mousewheel(self.category_canvas))
        
        self.category_frame = ttk.Frame(self.category_canvas, style="Custom.TFrame")
        self.category_canvas.create_window((0, 0), window=self.category_frame, anchor="nw")
        
        self.rule_canvas = tk.Canvas(main_frame, bg="#f0f0f0")
        self.rule_canvas.grid(row=4, column=0, sticky="nsew")
        self.rule_canvas.columnconfigure(0, weight=1)
        
        self.rule_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.rule_canvas.yview)
        self.rule_scrollbar.grid(row=4, column=1, sticky="ns")
        
        self.rule_canvas.configure(yscrollcommand=self.rule_scrollbar.set)
        self.rule_canvas.bind('<Configure>', lambda e: self.rule_canvas.configure(scrollregion=self.rule_canvas.bbox("all")))
        self.rule_canvas.bind("<Enter>", lambda e: self._bind_mousewheel(self.rule_canvas))
        self.rule_canvas.bind("<Leave>", lambda e: self._unbind_mousewheel(self.rule_canvas))
        
        self.rule_frame = ttk.Frame(self.rule_canvas, style="Custom.TFrame")
        self.rule_canvas.create_window((0, 0), window=self.rule_frame, anchor="nw")
        
        self.component_canvas = tk.Canvas(main_frame, bg="#f0f0f0")
        self.component_canvas.grid(row=3, column=1, rowspan=2, sticky="nsew")
        self.component_canvas.columnconfigure(0, weight=1)
        
        self.component_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.component_canvas.yview)
        self.component_scrollbar.grid(row=3, column=2, rowspan=2, sticky="ns")
        
        self.component_canvas.configure(yscrollcommand=self.component_scrollbar.set)
        self.component_canvas.bind('<Configure>', lambda e: self.component_canvas.configure(scrollregion=self.component_canvas.bbox("all")))
        self.component_canvas.bind("<Enter>", lambda e: self._bind_mousewheel(self.component_canvas))
        self.component_canvas.bind("<Leave>", lambda e: self._unbind_mousewheel(self.component_canvas))
        
        self.component_frame = ttk.Frame(self.component_canvas, style="Custom.TFrame")
        self.component_canvas.create_window((0, 0), window=self.component_frame, anchor="nw")
        
        self.add_component_button = ttk.Button(main_frame, text="+ Add Component", command=self.add_component)
        self.add_component_button.grid(row=5, column=1, pady=5, sticky="ew")
        
        self.run_button = ttk.Button(main_frame, text="Run Hexasnipe", command=self.run_hexasnipe)
        self.run_button.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
        
        self.result_label = ttk.Label(main_frame, text="", padding="10")
        self.result_label.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")
        
        self.set_mode("simple")
    
    def set_mode(self, mode):
        self.mode.set(mode)
        for widget in self.component_frame.winfo_children():
            widget.destroy()
        for widget in self.category_frame.winfo_children():
            widget.destroy()
        for widget in self.rule_frame.winfo_children():
            widget.destroy()
        self.components = []
        
        if mode == "complex":
            self.add_complex_options()
        else:
            self.options_frame.grid_remove()
            self.category_canvas.grid_remove()
            self.category_scrollbar.grid_remove()
            self.rule_canvas.grid_remove()
            self.rule_scrollbar.grid_remove()
        
        num_fields = 2
        for _ in range(num_fields):
            self.add_component()
    
    def add_complex_options(self):
        self.options_frame.grid()
        self.category_canvas.grid()
        self.category_scrollbar.grid()
        self.rule_canvas.grid()
        self.rule_scrollbar.grid()
        
        ttk.Button(self.category_frame, text="+ Add Category", command=self.add_category, style="Custom.TButton").pack(pady=5, fill="x")
        ttk.Button(self.rule_frame, text="+ Add Category Rule", command=self.add_category_rule, style="Custom.TButton").pack(pady=5, fill="x")

    def add_category(self):
        category_frame = ttk.Frame(self.category_frame, padding="5", style="Custom.TFrame")
        category_frame.pack(pady=5, fill="x")
        
        category_var = tk.StringVar()
        ttk.Entry(category_frame, textvariable=category_var, width=20, style="Custom.TEntry").pack(side=tk.LEFT, padx=5)
        ttk.Button(category_frame, text="Save", command=lambda: self.save_category(category_var), style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(category_frame, text="- Remove", command=lambda: self.remove_category(category_frame, category_var), style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        self.category_canvas.configure(scrollregion=self.category_canvas.bbox("all"))

    def remove_category(self, frame, category_var):
        frame.destroy()
        category = category_var.get()
        if category in self.categories:
            self.categories.remove(category)
            self.update_category_menus()
        self.category_canvas.configure(scrollregion=self.category_canvas.bbox("all"))

    def add_category_rule(self):
        rule_frame = ttk.Frame(self.rule_frame, padding="5", style="Custom.TFrame")
        rule_frame.pack(pady=5, fill="x")
        
        category_var = tk.StringVar()
        category_menu = ttk.OptionMenu(rule_frame, category_var, *self.categories, style="Custom.TMenubutton")
        category_menu.pack(side=tk.LEFT, padx=5)
        
        rule_type_var = tk.StringVar(value="Amount")
        rule_type_menu = ttk.OptionMenu(rule_frame, rule_type_var, "Amount", style="Custom.TMenubutton")
        rule_type_menu.pack(side=tk.LEFT, padx=5)
        
        rule_value_var = tk.IntVar()
        ttk.Entry(rule_frame, textvariable=rule_value_var, width=5, style="Custom.TEntry").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(rule_frame, text="Save", command=lambda: self.save_category_rule(category_var, rule_type_var, rule_value_var), style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(rule_frame, text="- Remove", command=lambda: self.remove_category_rule(rule_frame, category_var), style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        self.rule_canvas.configure(scrollregion=self.rule_canvas.bbox("all"))

    def remove_category_rule(self, frame, category_var):
        frame.destroy()
        category = category_var.get()
        if category in self.category_rules:
            del self.category_rules[category]
        self.rule_canvas.configure(scrollregion=self.rule_canvas.bbox("all"))
    
    def save_category(self, category_var):
        category = category_var.get()
        if category and category not in self.categories:
            self.categories.append(category)
            self.categories.sort()
            self.update_category_menus()
            self.update_existing_components_with_category(category)
    
    def update_category_menus(self):
        for widget in self.component_frame.winfo_children():
            if isinstance(widget, ttk.OptionMenu):
                widget['menu'].delete(0, 'end')
                for category in self.categories:
                    widget['menu'].add_command(label=category, command=tk._setit(widget['variable'], category))
    
    def update_existing_components_with_category(self, category):
        for component in self.components:
            category_menu = component[3]
            if category_menu:
                menu = category_menu['menu']
                menu.add_command(label=category, command=tk._setit(component[2], category))

    def add_component(self):
        frame = ttk.Frame(self.component_frame, padding="5", style="Custom.TFrame")
        frame.pack(pady=5, fill="x")
        name_var = tk.StringVar()
        color_var = tk.StringVar()
        category_var = tk.StringVar() if self.mode.get() == "complex" else None
        
        ttk.Label(frame, text="Name:", style="Custom.TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame, textvariable=name_var, width=10, style="Custom.TEntry").pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        ttk.Label(frame, text="Color:", style="Custom.TLabel").pack(side=tk.LEFT, padx=5)
        color_entry = ttk.Entry(frame, textvariable=color_var, width=10, style="Custom.TEntry")
        color_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        ttk.Button(frame, text="Pick", command=lambda: self.pick_color(color_var, color_entry), style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        
        category_menu = None
        if category_var is not None:
            ttk.Label(frame, text="Category:", style="Custom.TLabel").pack(side=tk.LEFT, padx=5)
            category_menu = ttk.OptionMenu(frame, category_var, *self.categories, style="Custom.TMenubutton")
            category_menu.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        self.components.append((name_var, color_var, category_var, category_menu))
        self.component_canvas.configure(scrollregion=self.component_canvas.bbox("all"))
        ttk.Button(frame, text="- Remove", command=lambda: self.remove_component(frame, (name_var, color_var, category_var, category_menu)), style="Custom.TButton").pack(side=tk.LEFT, padx=5)
    
    def remove_component(self, frame, component):
        frame.destroy()
        self.components.remove(component)
        self.component_canvas.configure(scrollregion=self.component_canvas.bbox("all"))
    
    def pick_color(self, color_var, entry):
        color = colorchooser.askcolor(title="Pick a color")[1]
        if color:
            color_var.set(color)
            style = ttk.Style()
            style.configure("Colored.TEntry", fieldbackground=color)
            entry.config(style="Colored.TEntry")
    
    def pick_target_color(self):
        color = colorchooser.askcolor(title="Pick Target Color")[1]
        if color:
            self.target_color_var.set(color)
    
    def update_exact_count(self):
        components = {c[0].get(): (c[1].get(), c[2].get() if c[2] else None) for c in self.components}
        try:
            exact_count = int(self.exact_count.get())
        except tk.TclError:
            exact_count = 0
        
        if exact_count and exact_count > len(components) + 1:
            if not self.allow_duplicates.get():
                self.allow_duplicates.set(True)
                self.duplicate_label.config(text="Automatically turned on")
            self.allow_duplicates_check.config(state=tk.DISABLED)
        else:
            self.duplicate_label.config(text="")
            self.allow_duplicates.set(False)
            self.allow_duplicates_check.config(state=tk.NORMAL)

    def run_hexasnipe(self):
        target_hex = self.target_color_var.get()
        components = {c[0].get(): (c[1].get(), c[2].get() if c[2] else None) for c in self.components}
        allow_duplicates = self.allow_duplicates.get()
        try:
            exact_count = int(self.exact_count.get())
        except tk.TclError:
            exact_count = 0
        
        best_match = find_matching_combinations(target_hex, components, allow_duplicates, exact_count, self.category_rules)
        self.result_label.config(text=f"Best Match: {best_match}")
        visualize_colors(target_hex, best_match[0] if best_match else [])

    def save_category_rule(self, category_var, rule_type_var, rule_value_var):
        category = category_var.get()
        rule_type = rule_type_var.get()
        rule_value = rule_value_var.get()
        if category and rule_type == "Amount":
            self.category_rules[category] = rule_value
            self.update_existing_components_with_category(category)

    def _bind_mousewheel(self, canvas):
        if canvas.winfo_height() < canvas.bbox("all")[3]:
            canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas))

    def _unbind_mousewheel(self, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
