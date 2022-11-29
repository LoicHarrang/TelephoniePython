import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
  
audio = pyaudio.PyAudio()
  
# Debut enregistrement
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print ("Enregistrement en cours...")

frames = []
  
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)  
print ("Fin d'enregistrement")

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
for data in frames:
    stream.write(data)

print ("Fin ")

