import itertools
from utils import find_matching_combinations, mix_colors, rgb_to_hex

if __name__ == "__main__":
    modes = {1: "Simple Hexasnipe", 2: "Complex Hexasnipe"}
    print("Hexasnipe modes:")
    for key, value in modes.items():
        print(f"{key}: {value}")
    mode = input("Choose mode: ").strip()
    target_hex = input("Enter the target hex color: ").strip()
    num_components = int(input("Enter the number of available components: "))
    
    components = {}
    for _ in range(num_components):
        name = input("Component name: ").strip()
        hex_color = input("Hex color of the component: ").strip()
        if mode == "2":
            category = input("Category of the component: ").strip()
        else:
            category = None
        components[name] = (hex_color, category)
    
    allow_duplicates = False
    exact_count = None
    category_rules = {}
    
    if mode == "2":
        allow_duplicates = input("Allow duplicate components? (yes/no): ").strip().lower() == "yes"
        exact_count = int(input("Specify exact number of components in the recipe (or 0 for any): ")) or None
        num_categories = int(input("Enter the number of category rules (or 0 for none): "))
        for _ in range(num_categories):
            cat = input("Category name: ").strip()
            count = int(input(f"Number of components required from {cat}: "))
            category_rules[cat] = count
    
    matches = find_matching_combinations(target_hex, components, allow_duplicates, exact_count, category_rules)
    
    print("\nBest matching component combinations:")
    for combo in matches:
        combo_names = ", ".join(c[0] for c in combo)
        mixed_hex = rgb_to_hex(mix_colors([c[1] for c in combo], [1] * len(combo)))
        print(f"{combo_names} -> {mixed_hex}")
