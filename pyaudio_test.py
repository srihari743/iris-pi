import pyaudio

pa = pyaudio.PyAudio()

stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1600
)

print("PyAudio input OK")

stream.close()
pa.terminate()
