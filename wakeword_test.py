import time
import numpy as np
import pyaudio
from openwakeword.model import Model

model = Model(wakeword_models=["hey_jarvis"])

pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1600
)

print("Listening for wake word: 'hey jarvis' (Ctrl+C to stop)")

last_print = 0

try:
    while True:
        data = stream.read(1600, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16)

        scores = model.predict(audio)
        score = scores.get("hey_jarvis", 0)

        now = time.time()
        if score > 0.5 and now - last_print > 1.5:
            print("Wake word detected")
            last_print = now

        time.sleep(0.01)  # 🔒 CPU guard
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
