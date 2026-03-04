from faster_whisper import WhisperModel 

model = WhisperModel("tiny",compute_type="int8")
segments, _ = model.transcribe("bt_test.wav")

for segment in segments:
        print(segment.text)
