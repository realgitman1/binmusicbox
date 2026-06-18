# Binary Oscillator Glitch Visualizer

An experimental data audio-visualization tool that reads any arbitrary raw binary file and maps its byte streams into a real-time digital waterfall display and synthesized glitch audio. 

> 💡 **Note**: This project was designed and developed in collaboration with **Gemini**.

Unlike traditional visualizers that map predefined music to graphics, this tool treats the data files themselves (e.g., `.exe`, `.jpg`, `.pdf`) as the core automation source for a raw synthesizer.

---
<img width="806" height="648" alt="ss" src="https://github.com/user-attachments/assets/6f42eb37-4266-44fc-a3fc-7a837ee8a392" />


## Features

- **No Static Noise**: Bypasses raw-byte PCM playback to completely eliminate harsh high-frequency white noise.
- **Dynamic Frequency Modulation**: Maps file bytes ($0 \sim 255$) into a clean, audible frequency range ($130\text{Hz} \sim 1500\text{Hz}$).
- **Timbral Shifting**: Alternates wave shapes between smooth **Sine waves** and sharp **Square waves** based on byte parity, producing a chiptune/IDM cyber aesthetic.
- **Phase Continuity**: Tracks the mathematical phase across buffer boundaries to eliminate jarring click artifacts.
- **Matrix Waterfall Grid**: Renders data chunks onto the screen's Green channel for a retro terminal interface look.

---

## Getting Started (How to Run)

You can run this application directly using the pre-compiled executable file without setting up a Python environment.

1. Navigate to the `dist` directory in this project.
2. Download or locate the executable file (e.g., `binary_player.exe` or your custom named binary).
3. Open your terminal (Command Prompt or PowerShell) inside that folder, and run the command below by passing any target file path as an argument.

### Command Execution

```bash
# Windows Command Prompt / PowerShell
binary_player.exe <path_to_target_file>

# Example: Analyzing an image file
binary_player.exe cat.jpg
```

Recommended Examples to Try
Compiled Binaries (.exe, .bin, .dll): Generates dense cyber rhythms, heavy chiptune structures, and complex visual matrices.

Compressed Images (.jpg, .png): Generates shifting tempos, sweeping melodic glitches, and sudden visual block bursts.

Controls
Close the graphical display window or press Ctrl + C in your terminal at any time to safely stop execution and exit.
