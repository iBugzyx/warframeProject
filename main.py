import tkinter as tk
from tkinter import Listbox, ttk
import json
import os
from PIL import Image, ImageTk
import sys
import datetime

# Setup root window
root = tk.Tk()
root.title("Warframe Index")
root.geometry("1280x720")
root.configure(bg="#1a1a1a")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#1a1a1a", borderwidth=0)
style.configure("TNotebook.Tab", background="#2a2a2a", foreground="#e0e0e0", padding=[10, 5], font=("Arial", 12, "bold"))
style.map("TNotebook.Tab", background=[("selected", "#3a3a3a")], foreground=[("selected", "#ffd700")])
style.configure("TEntry", fieldbackground="#2a2a2a", foreground="#e0e0e0", borderwidth=1, padding=5)

# Notebook setup
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab1 = ttk.Frame(notebook, style="Dark.TFrame")
tab2 = ttk.Frame(notebook, style="Dark.TFrame")
tab3 = ttk.Frame(notebook, style="Dark.TFrame")
tab4 = ttk.Frame(notebook, style="Dark.TFrame")
tab5 = ttk.Frame(notebook, style="Dark.TFrame")
tab6 = ttk.Frame(notebook, style="Dark.TFrame")
tab7 = ttk.Frame(notebook, style="Dark.TFrame")
tab8 = ttk.Frame(notebook, style="Dark.TFrame")

notebook.add(tab1, text="Warframes")
notebook.add(tab2, text="Primary Weapons")
notebook.add(tab3, text="Secondary Weapons")
notebook.add(tab4, text="Melee Weapons")
notebook.add(tab5, text="Mods")
notebook.add(tab6, text="Resources")
notebook.add(tab7, text="Arcanes")
notebook.add(tab8, text="Trackers")

style.configure("Dark.TFrame", background="#1a1a1a")

tabs = {
    "Warframes": {"frame": tab1, "items": [], "listbox": None, "details": None},
    "Primary Weapons": {"frame": tab2, "items": [], "listbox": None, "details": None},
    "Secondary Weapons": {"frame": tab3, "items": [], "listbox": None, "details": None},
    "Melee Weapons": {"frame": tab4, "items": [], "listbox": None, "details": None},
    "Mods": {"frame": tab5, "items": [], "listbox": None, "details": None},
    "Resources": {"frame": tab6, "items": [], "listbox": None, "details": None},
    "Arcanes": {"frame": tab7, "items": [], "listbox": None, "details": None},
    "Trackers": {"frame": tab8, "items": [], "listbox": None, "details": None}
}

def load_data():
    if getattr(sys, "frozen", False):
        data_dir = os.path.join(sys._MEIPASS, "data")
        pics_dir = os.path.join(sys._MEIPASS, "pics")
    else:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        pics_dir = os.path.join(os.path.dirname(__file__), "pics")

    if not os.path.exists(data_dir):
        print(f"Data directory not found: {data_dir}")
        return

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        # Use category or type for filtering
                        category = item.get("category", item.get("type", "Unknown")).title()
                        item_name = item.get("name", "Unnamed")

                        if category == "Warframes":
                            tabs["Warframes"]["items"].append(item)
                        elif category == "Primary":
                            tabs["Primary Weapons"]["items"].append(item)
                        elif category == "Secondary":
                            tabs["Secondary Weapons"]["items"].append(item)
                        elif category == "Melee":
                            tabs["Melee Weapons"]["items"].append(item)
                        elif category in ["Resources", "Gem", "Plant"]:
                            tabs["Resources"]["items"].append(item)
                        elif "Mod" in category or category == "Focus Way":
                            tabs["Mods"]["items"].append(item)
                        elif category in ["Arcanes", "Drops"]:
                            tabs["Arcanes"]["items"].append(item)
                        else:
                            print(f"Unrecognized category '{category}' for item '{item_name}' in {filename}")
                    print(f"Loaded {len(items)} items from {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    for tab_name, tab_data in tabs.items():
        print(f"{tab_name}: {len(tab_data['items'])} items")

def setup_tab(tab_name, tab_data):
    frame = tab_data["frame"]

    search_var = tk.StringVar()
    search_entry = ttk.Entry(frame, textvariable=search_var)
    search_entry.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
    
    placeholder_text = "Search items..."
    search_entry.insert(0, placeholder_text)
    search_entry.config(foreground="#b0b0b0")

    def on_focus_in(event):
        if event.type == "4" or (event.type == "9" and event.widget == search_entry and search_entry.get() == placeholder_text):
            if search_var.get() == placeholder_text:
                search_entry.delete(0, tk.END)
                search_entry.config(foreground="#e0e0e0")

    def on_focus_out(event):
        if not search_var.get():
            search_entry.insert(0, placeholder_text)
            search_entry.config(foreground="#b0b0b0")
    search_entry.bind("<Button-1>", on_focus_in)
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    # Listbox
    listbox = tk.Listbox(frame, height=30, width=35, font=("Arial", 11), bg="#2a2a2a", fg="#e0e0e0", 
                         selectbackground="#ffd700", selectforeground="#1a1a1a", borderwidth=0, highlightthickness=0)
    listbox.grid(row=1, column=0, sticky="ns", padx=(10, 0), pady=5)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky="ns", pady=5)
    tab_data["listbox"] = listbox

    # Details area
    details_frame = ttk.Frame(frame, style="Dark.TFrame")
    details_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)
    details = tk.Text(details_frame, height=30, width=50, wrap="word", font=("Arial", 10), 
                      bg="#2a2a2a", fg="#e0e0e0", borderwidth=0, highlightthickness=0)
    details.pack(side="left", fill="both", expand=True)
    details_scroll = ttk.Scrollbar(details_frame, orient="vertical", command=details.yview)
    details.config(yscrollcommand=details_scroll.set)
    details_scroll.pack(side="right", fill="y")
    tab_data["details"] = details

    # Grid config
    frame.columnconfigure(2, weight=1)
    frame.rowconfigure(1, weight=1)

    # Populate listbox
    def update_listbox(search=""):
        listbox.delete(0, tk.END)
        search_text = search_var.get() if search_var.get() != placeholder_text else ""
    
        if not search_text:  # If search is empty, show all items
            for item in tab_data["items"]:
                listbox.insert(tk.END, item["name"])
            return
        
        for item in tab_data["items"]:
            if tab_name in ["Mods", "Arcanes"]:  # Search only in levelStats for Mods and Arcanes
                if "levelStats" in item:
                    for stat in item["levelStats"]:
                        if "stats" in stat:
                            combined_text = " ".join(stat["stats"]).lower()
                            if search_text.lower() in combined_text:
                                listbox.insert(tk.END, item["name"])
                                break  # Stop searching further stats for this item
            else:  # Normal search for other tabs
                # Collect all searchable text
                search_fields = []
                search_fields.append(item.get("name", ""))
                search_fields.append(item.get("description", ""))
                search_fields.append(item.get("type", ""))
                search_fields.append(item.get("category", ""))
                search_fields.append(item.get("compatName", ""))
                # Combine and search
                combined_text = " ".join(str(f) for f in search_fields if f).lower()
                if search_text.lower() in combined_text:
                    listbox.insert(tk.END, item["name"])

    update_listbox()

    # Bindings
    search_entry.bind("<KeyRelease>", lambda event: update_listbox(search_var.get()))
    listbox.bind("<<ListboxSelect>>", lambda event: show_details(event, tab_data))

tracker_labels = {}

def setup_tracker_tab():
    pass

def show_details(event, tab_data):
    selection = tab_data["listbox"].curselection()
    if selection:
        index = [i for i, item in enumerate(tab_data["items"]) if item["name"] == tab_data["listbox"].get(selection[0])][0]
        item = tab_data["items"][index]
        details = tab_data["details"]
        details.delete(1.0, tk.END)

        # Header: Name
        details.insert(tk.END, f"Name: {item.get('name', 'N/A')}\n", "header")

        # Resource-specific fields
        if tab_data == tabs["Resources"]:
            details.insert(tk.END, "\nResource Details\n", "section")
            resource_fields = [
                ("buildPrice", "Build Price"),
                ("buildQuantity", "Build Quantity"),
                ("buildTime", "Build Time"),
                ("itemCount", "Item Count"),
                ("tradable", "Tradable"),
                ("type", "Type"),
            ]
            for field, label in resource_fields:
                if field in item:
                    value = item[field]
                    if field == "buildPrice":
                        value = f"{int(value):,} credits"
                    elif field == "buildTime":
                        value = f"{int(value) / 3600:.2f} hrs"
                    elif isinstance(value, bool):
                        value = "Yes" if value else "No"
                    details.insert(tk.END, f"  {label}: {value}\n")
            details.insert(tk.END, "\n")

            # Parents Section
            if "parents" in item and item["parents"]:
                details.insert(tk.END, "Parents\n", "section")
                for parent in item["parents"]:
                    details.insert(tk.END, f"  {parent}\n")
                details.insert(tk.END, "\n")

            # Drops Section
            if "drops" in item and item["drops"]:
                details.insert(tk.END, "Drops\n", "section")
                for drop in item["drops"]:
                    details.insert(tk.END, f"  Location: {drop.get('location', 'Unknown')}\n")
                    details.insert(tk.END, f"    Type: {drop.get('type', 'Unknown')}\n")
                    details.insert(tk.END, f"    Rarity: {drop.get('rarity', 'Unknown')}\n")
                    details.insert(tk.END, f"    Chance: {float(drop.get('chance', 0)) * 100:.2f}%\n")
                details.insert(tk.END, "\n")

        # Mod-specific fields
        if tab_data == tabs["Mods"]:
            details.insert(tk.END, "\nMod Details\n", "section")
            mod_fields = [
                ("baseDrain", "Base Drain"),
                ("compatName", "Compatible With"),
                ("fusionLimit", "Fusion Limit"),
                ("polarity", "Polarity"),
                ("rarity", "Rarity"),
                ("isAugment", "Is Augment"),
                ("isPrime", "Is Prime"),
                ("tradable", "Tradable"),
            ]
            for field, label in mod_fields:
                if field in item:
                    value = item[field]
                    if isinstance(value, bool):
                        value = "Yes" if value else "No"
                    details.insert(tk.END, f"  {label}: {value}\n")
            details.insert(tk.END, "\n")

            if "levelStats" in item and item["levelStats"]:
                details.insert(tk.END, "Level Stats\n", "section")
                for level, stats in enumerate(item["levelStats"], start=1):
                    details.insert(tk.END, f"  Level {level}:\n", "subheader")
                    for stat in stats.get("stats", []):
                        details.insert(tk.END, f"    {stat}\n")
                details.insert(tk.END, "\n")

            if "drops" in item and item["drops"]:
                details.insert(tk.END, "Drops\n", "section")
                for drop in item["drops"]:
                    details.insert(tk.END, f"  Location: {drop.get('location', 'Unknown')}\n")
                    details.insert(tk.END, f"    Type: {drop.get('type', 'Unknown')}\n")
                    details.insert(tk.END, f"    Rarity: {drop.get('rarity', 'Unknown')}\n")
                    details.insert(tk.END, f"    Chance: {float(drop.get('chance', 0)) * 100:.2f}%\n")
                details.insert(tk.END, "\n")

        # Arcane-specific fields
        if tab_data == tabs["Arcanes"]:
            details.insert(tk.END, "\nArcane Details\n", "section")
            arcane_fields = [
                ("rarity", "Rarity"),
                ("tradable", "Tradable"),
            ]
            for field, label in arcane_fields:
                if field in item:
                    value = item[field]
                    if isinstance(value, bool):
                        value = "Yes" if value else "No"
                    details.insert(tk.END, f"  {label}: {value}\n")
            details.insert(tk.END, "\n")

            if "levelStats" in item and item["levelStats"]:
                details.insert(tk.END, "Level Stats\n", "section")
                for level, stats in enumerate(item["levelStats"], start=1):
                    details.insert(tk.END, f"  Level {level}:\n", "subheader")
                    for stat in stats.get("stats", []):
                        details.insert(tk.END, f"    {stat}\n")
                details.insert(tk.END, "\n")

            if "drops" in item and item["drops"]:
                details.insert(tk.END, "Drops\n", "section")
                for drop in item["drops"]:
                    details.insert(tk.END, f"  Location: {drop.get('location', 'Unknown')}\n")
                    details.insert(tk.END, f"    Type: {drop.get('type', 'Unknown')}\n")
                    details.insert(tk.END, f"    Rarity: {drop.get('rarity', 'Unknown')}\n")
                    details.insert(tk.END, f"    Chance: {float(drop.get('chance', 0)) * 100:.2f}%\n")
                details.insert(tk.END, "\n")

        # Stats Section (for Warframes, Weapons, etc.)
        details.insert(tk.END, "\nStats\n", "section")
        stat_fields = [
            ("health", "Health"),
            ("shield", "Shield"),
            ("armor", "Armor"),
            ("energy", "Energy"),
            ("sprintSpeed", "Sprint Speed"),
            ("accuracy", "Accuracy"),
            ("criticalChance", "Critical Chance"),
            ("criticalMultiplier", "Critical Multiplier"),
            ("fireRate", "Fire Rate"),
            ("magazineSize", "Magazine Size"),
            ("reloadTime", "Reload Time"),
            ("totalDamage", "Total Damage"),
            ("procChance", "Status Chance"),
            ("trigger", "Trigger Type"),
            ("masteryReq", "Mastery Requirement"),
            ("multishot", "Multishot"),
            ("marketCost", "Market Cost"),
        ]
        for field, label in stat_fields:
            if field in item and item[field] is not None:
                value = item[field]
                if field in ["criticalChance", "criticalMultiplier", "procChance"]:
                    value = f"{float(value) * 100:.2f}%"  # Convert to percentage
                elif isinstance(value, float):
                    value = f"{value:.2f}"  # Limit floats to 2 decimal places
                elif field == "marketCost":
                    value = f"{int(value):,} platinum"
                details.insert(tk.END, f"  {label}: {value}\n")
        details.insert(tk.END, "\n")

        # Abilities Section
        if "abilities" in item:
            details.insert(tk.END, "Abilities\n", "section")
            for ability in item["abilities"]:
                details.insert(tk.END, f"  {ability.get('name', 'Unnamed Ability')}\n", "subheader")
                details.insert(tk.END, f"    {ability.get('description', 'No description available.')}\n")
            details.insert(tk.END, "\n")

        # Attacks Section (for Weapons)
        if "attacks" in item:
            details.insert(tk.END, "Attacks\n", "section")
            for attack in item["attacks"]:
                details.insert(tk.END, f"  {attack.get('name', 'Unnamed Attack')}\n", "subheader")
                attack_fields = [
                    ("crit_chance", "Critical Chance"),
                    ("crit_mult", "Critical Multiplier"),
                    ("status_chance", "Status Chance"),
                    ("damage", "Damage"),
                    ("shot_type", "Shot Type"),
                    ("speed", "Speed"),
                ]
                for field, label in attack_fields:
                    if field in attack:
                        value = attack[field]
                        if field in ["crit_chance", "crit_mult", "status_chance"]:
                            if value <= 1:  # If the value is in decimal format, convert to percentage
                                value = f"{float(value) * 100:.2f}%"
                            else:  # Otherwise, assume it's already a percentage
                                value = f"{float(value):.2f}%"
                        elif field == "damage" and isinstance(value, dict):
                            # Format damage dictionary with 2 decimal places
                            damage_str = ", ".join(f"{k.title()}: {v:.2f}" if isinstance(v, float) else f"{k.title()}: {v}" for k, v in value.items())
                            value = damage_str
                        elif isinstance(value, float):
                            value = f"{value:.2f}"  # Limit floats to 2 decimal places
                        details.insert(tk.END, f"    {label}: {value}\n")
                details.insert(tk.END, "\n")

        # Damage Section (for Weapons)
        if "damage" in item:
            details.insert(tk.END, "Damage\n", "section")
            for damage_type, value in item["damage"].items():
                if value > 0:
                    formatted_value = f"{value:.2f}" if isinstance(value, float) else value
                    details.insert(tk.END, f"  {damage_type.title()}: {formatted_value}\n")
            details.insert(tk.END, "\n")

        # Description Section
        if "description" in item and item["description"]:
            details.insert(tk.END, f"Description: {item['description']}\n\n", "subheader")

        # General Info Section
        details.insert(tk.END, "General Info\n", "section")
        general_fields = ["buildPrice", "buildTime", "skipBuildTimePrice", "tradable", "vaulted", "releaseDate"]
        for field in general_fields:
            if field in item:
                value = item[field]
                if field == "buildPrice" or field == "bpCost":
                    value = f"{int(value):,} credits"
                    label = "Build Cost"
                elif field == "skipBuildTimePrice":
                    value = f"{int(value)} platinum"
                    label = "Skip Build Time Cost"
                elif field == "buildTime":
                    value = f"{float(value) / 3600:.2f} hrs"
                    label = "Build Time"
                elif isinstance(value, bool):
                    value = "Yes" if value else "No"
                    label = field.replace('build', '').replace('Price', '').title()
                else:
                    label = field.replace('build', '').replace('Price', '').title()
                details.insert(tk.END, f"  {label}: {value}\n")
        details.insert(tk.END, "\n")

        # Components Section
        if "components" in item:
            details.insert(tk.END, "Components\n", "section")
            for component in item["components"]:
                details.insert(tk.END, f"  {component.get('name', 'N/A')}\n", "subheader")
                if "itemCount" in component:
                    details.insert(tk.END, f"    Quantity: {component['itemCount']}\n")
                if "drops" in component and component["drops"]:
                    details.insert(tk.END, "    Drops\n")
                    for drop in component["drops"]:
                        chance = float(drop.get('chance', 0)) * 100
                        details.insert(tk.END, f"      {drop.get('location', 'N/A')} - {drop.get('rarity', 'N/A')} ({chance:.2f}%)\n")
            details.insert(tk.END, "\n")

        # Formatting Tags
        details.tag_configure("header", font=("Arial", 16, "bold"), foreground="#ffd700", spacing1=5)
        details.tag_configure("subheader", font=("Arial", 12, "bold"), foreground="#e0e0e0", spacing1=3)
        details.tag_configure("section", font=("Arial", 14, "bold", "underline"), foreground="#ffd700", spacing1=5)

# Load data and setup tabs
load_data()
for tab_name, tab_data in tabs.items():
    setup_tab(tab_name, tab_data)

root.mainloop()