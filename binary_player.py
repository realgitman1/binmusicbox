import sys
import os
import pygame
import numpy as np

# Initialize Pygame
pygame.init()
# Standard 44100Hz audio frequency for clean signal synthesis
SAMPLE_RATE = 44100
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=1024)

# Screen configuration (Binary Matrix Waterfall Grid)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Oscillator Glitch Visualizer")

def play_binary_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Small chunk size for high-frequency oscillator updates
    chunk_size = 512 
    display_buffer = np.zeros((WIDTH, HEIGHT), dtype=np.uint8)
    clock = pygame.time.Clock()
    
    # Global phase tracker to ensure wave continuity
    global_phase = 0.0

    with open(file_path, "rb") as f:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            raw_data = f.read(chunk_size)
            if not raw_data:
                print("End of file reached.")
                break
            
            data_len = len(raw_data)
            byte_array = np.frombuffer(raw_data, dtype=np.uint8)

            # ----------------------------------------------------
            # 2. Oscillator-Based Glitch Audio Synthesis
            # ----------------------------------------------------
            if data_len > 0:
                # Extract the first byte of the chunk as the pitch controller
                current_byte = byte_array[0]
                
                # Map byte (0~255) to human audible frequency range (130Hz ~ 1500Hz)
                # Lower values generate heavy bass, higher values create piercing glitches
                target_freq = 130.0 + (float(current_byte) / 255.0) * 1370.0
            else:
                target_freq = 0.0

            # Calculate required samples for 1 video frame (~1/30 seconds)
            num_samples = 1470 
            
            if target_freq > 130.0:
                t = np.arange(num_samples) / SAMPLE_RATE
                
                # Maintain phase continuity to avoid click noises at frame boundaries
                phase = global_phase + 2.0 * np.pi * target_freq * t
                global_phase = phase[-1] % (2.0 * np.pi)

                # Generate base Sine wave
                sine_wave = np.sin(phase)
                
                # Dynamic timbral glitching: Modulate to Square wave on even byte values
                # This introduces raw, 8-bit chiptune textures
                if current_byte % 2 == 0:
                    osc_output = np.sign(sine_wave) * 0.5
                else:
                    osc_output = sine_wave * 0.7
            else:
                osc_output = np.zeros(num_samples)

            # Convert to 16-bit signed integer PCM
            audio_samples = (osc_output * 16384).astype(np.int16)

            # Map to stereo channels (2D array)
            stereo_samples = np.repeat(audio_samples[:, np.newaxis], 2, axis=1)

            # Create and play the sound burst immediately
            sound = pygame.sndarray.make_sound(stereo_samples)
            sound.play()
            # ----------------------------------------------------

            # 3. Video Rendering Pipeline
            # Scroll the buffer upwards by rolling the axis
            display_buffer = np.roll(display_buffer, -1, axis=0)
            if data_len > 0:
                # Interpolate byte values to fit the window height
                resized_data = np.interp(
                    np.linspace(0, data_len, HEIGHT), 
                    np.arange(data_len), 
                    byte_array
                ).astype(np.uint8)
                display_buffer[-1, :] = resized_data

            # 4. Display Frame Update
            # Inject data into the Green channel for a retro cyber aesthetic
            surface_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
            surface_array[:, :, 1] = display_buffer
            
            pygame.surfarray.blit_array(screen, surface_array)
            pygame.display.flip()

            # Limit to 30 FPS for aesthetic pace
            clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python binary_player.py <file_path>")
    else:
        play_binary_file(sys.argv[1])
