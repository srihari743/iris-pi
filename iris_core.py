import time
import subprocess
import numpy as np
import os
import pyaudio
from openwakeword.model import Model
from faster_whisper import WhisperModel

WAKE_MODEL = "hey_jarvis"
AUDIO_FILE = "/tmp/iris_input.wav"

print("Initializing Iris...")

if os.path.exists(AUDIO_FILE):
	os.remove(AUDIO_FILE)

# Wake word model
wake_model = Model(wakeword_models=[WAKE_MODEL])

# Whisper model (tiny for now)
whisper = WhisperModel("tiny", compute_type="int8")

# Audio stream for wake detection
pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1600
)

DEVICE_INDEX = 1  # pulse

stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=1600
)
print("Iris is idle. Say the wake word.")

last_trigger = 0

try:
    while True:
        data = stream.read(1600, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16)

        scores = wake_model.predict(audio)
        score = scores.get(WAKE_MODEL, 0)

        now = time.time()
        if score > 0.5 and now - last_trigger > 3:
            last_trigger = now
            print("Wake word detected. Listening...")

            # Record user speech
            subprocess.run([
		"timeout", "5",
                "parecord",
                "--device=bluez_input.F8_AB_E5_F2_ED_6A.0",
                "--rate=16000",
                "--channels=1",
               AUDIO_FILE
            ])

            print("Processing speech...")

            segments, _ = whisper.transcribe(AUDIO_FILE)
            for segment in segments:
                print("You said:", segment.text)

            print("Iris idle. Say wake word again.")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Shutting down Iris.")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
