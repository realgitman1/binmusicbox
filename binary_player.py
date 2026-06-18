import sys
import os
import pygame
import numpy as np

# 초기화
pygame.init()
# 깨끗한 사운드 합성을 위해 표준 44100Hz로 설정
SAMPLE_RATE = 44100
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=1024)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Oscillator Glitch Visualizer")

def play_binary_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} 파일을 찾을 수 없습니다.")
        return

    # 오실레이터의 주파수를 자주 업데이트하기 위해 청크 사이즈를 작게 조절
    chunk_size = 512 
    display_buffer = np.zeros((WIDTH, HEIGHT), dtype=np.uint8)
    clock = pygame.time.Clock()
    
    # 오실레이터 위상(Phase) 추적 변수
    global_phase = 0.0

    with open(file_path, "rb") as f:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            raw_data = f.read(chunk_size)
            if not raw_data:
                print("파일 끝에 도달했습니다.")
                break
            
            data_len = len(raw_data)
            byte_array = np.frombuffer(raw_data, dtype=np.uint8)

            # ----------------------------------------------------
            # [핵심] 2. 오실레이터 주파수 변조 (FM / Pitch Modulation)
            # ----------------------------------------------------
            # 1) 현재 바이너리 청크의 대표값(예: 평균값 또는 중간값) 추출
            if data_len > 0:
                current_byte = byte_array[0] # 청크의 첫 바이트 혹은 np.mean(byte_array)
                
                # 2) 바이트(0~255)를 가청 주파수(130Hz ~ 1500Hz) 대역으로 매핑
                # 0x00에 가까우면 묵직한 베이스, 0xFF에 가까우면 찌르는 소리
                target_freq = 130.0 + (float(current_byte) / 255.0) * 1370.0
            else:
                target_freq = 0.0

            # 3) 합성할 오디오 샘플 수 계산 (비디오 1프레임 분량에 맞춤: 대략 1/30초 -> ~1470 샘플)
            num_samples = 1470 
            
            if target_freq > 130.0:
                # 시간 배열 생성
                t = np.arange(num_samples) / SAMPLE_RATE
                
                # 위상 연속성을 보장하여 뚝뚝 끊기는 노이즈(Click Noise) 방지
                phase = global_phase + 2.0 * np.pi * target_freq * t
                global_phase = phase[-1] % (2.0 * np.pi) # 마지막 위상 저장

                # 기본 오실레이터: 사인파(Sine) 합성 (부드러운 소리)
                sine_wave = np.sin(phase)
                
                # 글리치 텍스처 가공: 특정 조건(예: 바이트가 짝수일 때)에서 사각파(Square)로 변조
                # 사각파는 '뿅뿅'거리는 칩튠/레트로 글리치 느낌을 줍니다.
                if current_byte % 2 == 0:
                    osc_output = np.sign(sine_wave) * 0.5  # 사각파 변환
                else:
                    osc_output = sine_wave * 0.7  # 사인파 유지
            else:
                osc_output = np.zeros(num_samples)

            # 4) 16비트 정수형으로 변환
            audio_samples = (osc_output * 16384).astype(np.int16)

            # 스테레오 채널(2차원) 매핑
            stereo_samples = np.repeat(audio_samples[:, np.newaxis], 2, axis=1)

            # 사운드 생성 및 즉시 재생
            sound = pygame.sndarray.make_sound(stereo_samples)
            sound.play()
            # ----------------------------------------------------

            # 3. 비디오 렌더링
            display_buffer = np.roll(display_buffer, -1, axis=0)
            if data_len > 0:
                resized_data = np.interp(
                    np.linspace(0, data_len, HEIGHT), 
                    np.arange(data_len), 
                    byte_array
                ).astype(np.uint8)
                display_buffer[-1, :] = resized_data

            # 4. 화면에 그리기
            surface_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
            surface_array[:, :, 1] = display_buffer
            
            pygame.surfarray.blit_array(screen, surface_array)
            pygame.display.flip()

            clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python binary_player.py <파일경로>")
    else:
        play_binary_file(sys.argv[1])
