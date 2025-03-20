import itertools
import matplotlib.pyplot as plt

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
    
    if exact_count and exact_count > len(component_list):
        allow_duplicates = True
    
    max_combinations = exact_count if exact_count else len(component_list)
    
    for r in range(2, max_combinations + 1):
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

def visualize_colors(target_hex, best_combo):
    if not best_combo:
        return
    if isinstance(best_combo[0], tuple):
        colors = [c[1] for c in best_combo]
        names = [c[0] for c in best_combo]
    else:
        colors = [best_combo[1]]
        names = [best_combo[0]]
    mixed_rgb = mix_colors(colors, [1] * len(colors))
    mixed_hex = rgb_to_hex(mixed_rgb)
    
    unique_colors = []
    color_counts = {}
    for name, color in zip(names, colors):
        color_hex = rgb_to_hex(color)
        if color_hex not in color_counts:
            color_counts[color_hex] = (name, 1)
            unique_colors.append(color)
        else:
            color_counts[color_hex] = (name, color_counts[color_hex][1] + 1)
    
    fig, ax = plt.subplots(1, len(unique_colors) + 2, figsize=(12, 3), gridspec_kw={'width_ratios': [1] * (len(unique_colors) + 2)})
    ax[0].imshow([[hex_to_rgb(target_hex)]], aspect="auto")
    ax[0].set_title(f"Target\n{target_hex}", fontsize=10)
    ax[0].axis("off")
    ax[1].imshow([[mixed_rgb]], aspect="auto")
    ax[1].set_title(f"Best Match\n{mixed_hex}", fontsize=10)
    ax[1].axis("off")
    for i, color in enumerate(unique_colors):
        color_hex = rgb_to_hex(color)
        name, count = color_counts[color_hex]
        title = f"{name}\n{color_hex}"
        if count > 1:
            title += f"\n({count}x)"
        ax[i + 2].imshow([[color]], aspect="auto")
        ax[i + 2].set_title(title, fontsize=10)
        ax[i + 2].axis("off")
        for spine in ax[i + 2].spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1.5)
    plt.subplots_adjust(wspace=0.5)
    plt.show()