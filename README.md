# Binary Oscillator Glitch Visualizer

An experimental data audio-visualization tool that reads any arbitrary raw binary file and maps its byte streams into a real-time digital waterfall display and synthesized glitch audio. 

Unlike traditional visualizers that map predefined music to graphics, this tool treats the data files themselves (e.g., `.exe`, `.jpg`, `.pdf`) as the core automation source for a raw synthesizer.

## Features

- **No Static Noise**: Bypasses raw-byte PCM playback to completely eliminate harsh high-frequency white noise.
- **Dynamic Frequency Modulation**: Maps file bytes ($0 \sim 255$) into a clean, audible frequency range ($130\text{Hz} \sim 1500\text{Hz}$).
- **Timbral Shifting**: Alternates wave shapes between smooth **Sine waves** and sharp **Square waves** based on byte parity, producing a chiptune/IDM cyber aesthetic.
- **Phase Continuity**: Tracks the mathematical phase across buffer boundaries to eliminate jarring click artifacts.
- **Matrix Waterfall Grid**: Renders data chunks onto the screen's Green channel for a retro terminal interface look.

## Prerequisites

Make sure you have Python 3.8+ installed along with the required libraries:

```bash
pip install pygame numpy
