# Aim Lab — FPS Aim Trainer

> A Pygame-based FPS aim trainer with CS2-style target modes, crosshair customization,
> hit tracking, Matplotlib charts and automatic Word report generation.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Features

- **CS2 mode** — up to 4 concurrent static targets, instant respawn, S+ to F ranking
- **8 crosshair styles** — press <kbd>C</kbd> to cycle (dot, cross, circle, T, square, diamond, triangle)
- **Target types** — normal, flick, tracking, headshot targets with distinct colors and scores
- **Particle effects** — explosion particles, combo multiplier, headshot glow, floating hit markers
- **Data analytics** — tracks every click (timestamp, coordinates, result), computes TTK, accuracy, offset
- **Visual reports** — Matplotlib heatmap, reaction-time chart, accuracy pie chart; Word report export

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| Mouse move | Aim crosshair |
| Left click | Shoot |
| <kbd>C</kbd> | Cycle crosshair style |
| <kbd>Space</kbd> | Start / return to menu |
| <kbd>Esc</kbd> | Quit |

## Project Structure

```
├── main.py               # Entry point
├── config.py             # Game constants, colors, screen settings
├── game_manager_modern.py# Modern game loop (default)
├── game_manager.py       # Classic game loop
├── target.py             # Target base class
├── target_types.py       # Flick / Tracking / Headshot targets
├── crosshair.py          # Crosshair rendering
├── particles.py          # Particle system
├── maps.py               # Map definitions
├── data_tracker.py       # Per-click data recording
├── data_analyzer.py      # Pandas analysis (TTK, accuracy, offset)
├── data_visualizer.py    # Matplotlib charts
├── report_generator.py   # Word (.docx) report generation
└── requirements.txt
```

## Architecture

The game follows an object-oriented design:

- **Inheritance & polymorphism** — `Target` base class with `FlickTarget` and `TrackingTarget` overriding `update()`
- **State pattern** — `GameState` enum switches between menu, playing, and game-over
- **Single responsibility** — `GameManager`, `DataTracker`, `DataAnalyzer`, `DataVisualizer`, `ReportGenerator` are decoupled

## Tech Stack

Python · Pygame · Pandas · Matplotlib · NumPy · python-docx

## License

MIT
