# Hexasnipe

Hexasnipe is a WIP Python-based tool that helps users find the best combinations of colors to match a target color. It provides both a graphical user interface (GUI) and a command-line interface (CLI).

## Features

- **Graphical User Interface (GUI):**
  - Supports simple and complex modes.
  - User-Friendly Intuitive input fields,   buttons, and color visualization.

- **Command-Line Interface (CLI):**
  - Supports simple and complex modes.
  - Efficient Text-Based Input.

## Installation

1. Clone the repository and change directory:
    ```bash
    git clone https://github.com/StivoMix/Hexasnipe
    cd hexasnipe
    ```
2. Install dependencies:
    ```bash
    pip install matplotlib
    ```
3. Run the GUI application:
    ```bash
    python hexasnipegui.py
    ```
    Run the CLI application:
    ```bash
    python hexasnipecli.py
    ```

## Usage

### GUI
1. Run the GUI application:
    ```bash
    python hexasnipegui.py
    ```
2. Use the interface to:
   - Select a mode (simple or complex).
   - Add components and categories.
   - Pick colors using the color picker.
   - Run Hexasnipe to find the best matches.
   - Visualize the results.

### CLI
1. Run the CLI application:
    ```bash
    python hexasnipecli.py
    ```
2. Follow the prompts to:
   - Choose a mode (simple or complex).
   - Enter the target color and components.
   - Define rules for categories (in complex mode).
3. View the best matching combinations in the terminal.

## Project Structure

```
hexasnipe/
├── gui_components.py  # Core GUI components and logic
├── hexasnipegui.py    # Entry point for the GUI application
├── utils.py           # Utility functions for color processing
├── hexasnipecli.py          # Command-line interface for Hexasnipe
└── README.md    # README file
```

## Contact

For questions or feedback, please contact StivoMix on discord.
