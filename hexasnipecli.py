import itertools

def hex_to_rgb(hex_color):
    if not hex_color:
        return (0, 0, 0)
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#" + "".join(f"{c:02x}" for c in rgb)

def mix_colors(colors, weights):
    total_weight = sum(weights)
    return tuple(sum(c[i] * w for c, w in zip(colors, weights)) // total_weight for i in range(3))

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def find_matching_combinations(target_hex, components, allow_duplicates, exact_count, category_rules):
    target_rgb = hex_to_rgb(target_hex)
    component_list = [(name, hex_to_rgb(color), category) for name, (color, category) in components.items()]
    best_matches = []
    min_distance = float("inf")
    
    for name, color, category in component_list:
        if rgb_to_hex(color) == target_hex:
            if exact_count == 0 or exact_count == 1:
                return [(name, color, category)]
    
    if exact_count == 1:
        for name, color, category in component_list:
            dist = color_distance(color, target_rgb)
            if dist < min_distance:
                best_matches = [(name, color, category)]
                min_distance = dist
        return best_matches
    
    for r in range(2, len(component_list) + 1):
        if exact_count and r != exact_count:
            continue
        
        combos = itertools.combinations_with_replacement(component_list, r) if allow_duplicates else itertools.combinations(component_list, r)
        for combo in combos:
            colors = [c[1] for c in combo]
            mixed_rgb = mix_colors(colors, [1] * len(colors))
            dist = color_distance(mixed_rgb, target_rgb)
            
            if category_rules:
                categories = [c[2] for c in combo]
                for cat, count in category_rules.items():
                    if categories.count(cat) != count:
                        break
                else:
                    if dist < min_distance:
                        best_matches = [combo]
                        min_distance = dist
                    elif dist == min_distance:
                        best_matches.append(combo)
            else:
                if dist < min_distance:
                    best_matches = [combo]
                    min_distance = dist
                elif dist == min_distance:
                    best_matches.append(combo)
    
    return best_matches

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
