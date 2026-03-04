import time
import wave
import numpy as np
import pyaudio
import webrtcvad
from openwakeword.model import Model
from faster_whisper import WhisperModel

# ---------------- CONFIG ----------------
WAKE_MODEL = "hey_jarvis"
SAMPLE_RATE = 16000
FRAME_MS = 20                      # 20 ms frames for VAD
FRAME_SIZE = int(SAMPLE_RATE * FRAME_MS / 1000)
SILENCE_TIMEOUT = 0.8              # seconds of silence to end speech
AUDIO_FILE = "/tmp/iris_input.wav"
PYAUDIO_DEVICE_INDEX = 1           # 'pulse'
# ---------------------------------------

print("Initializing Iris (conversational mode)...")

wake_model = Model(wakeword_models=[WAKE_MODEL])
vad = webrtcvad.Vad(2)  # 0–3 (higher = stricter)
whisper = WhisperModel("tiny", compute_type="int8")

pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    input_device_index=PYAUDIO_DEVICE_INDEX,
    frames_per_buffer=FRAME_SIZE
)

print("Iris idle. Say the wake word.")

listening = False
speech_frames = []
last_voice_time = 0

def write_wav(path, pcm16_frames):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(pcm16_frames))

try:
    while True:
        data = stream.read(FRAME_SIZE, exception_on_overflow=False)
        audio_i16 = np.frombuffer(data, dtype=np.int16)

        # Wake word check (always on)
        scores = wake_model.predict(audio_i16)
        if not listening and scores.get(WAKE_MODEL, 0) > 0.5:
            listening = True
            speech_frames = []
            last_voice_time = time.time()
            print("Wake word detected. Listening...")
            continue

        if listening:
            is_speech = vad.is_speech(data, SAMPLE_RATE)

            if is_speech:
                speech_frames.append(data)
                last_voice_time = time.time()
            else:
                # silence detected
                if time.time() - last_voice_time > SILENCE_TIMEOUT:
                    print("Processing speech...")
                    write_wav(AUDIO_FILE, speech_frames)

                    segments, _ = whisper.transcribe(AUDIO_FILE)
                    for seg in segments:
                        print("You said:", seg.text)

                    print("Iris idle. Say the wake word.")
                    listening = False
                    speech_frames = []

        time.sleep(0.002)  # tiny yield to keep CPU calm

except KeyboardInterrupt:
    print("Shutting down Iris.")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
