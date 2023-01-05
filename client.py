import socket, threading
import pyaudio

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.0.0.189"
port = 5000

client.connect((host, port))
print("CLIENT CONNECTED")

p = pyaudio.PyAudio()

Format = pyaudio.paInt16
Chunks = 4096
Channels = 2
Rate = 44100

input_stream = p.open(format=Format, 
                      channels=Channels, 
                      rate=Rate,
                      input=True,
                      frames_per_buffer=Chunks)

output_stream = p.open(format=Format, 
                       channels=Channels, 
                       rate=Rate,
                       output=True,
                       frames_per_buffer=Chunks)


def send():
    while True:
        try:
            data = input_stream.read(Chunks)
            client.send(data)
        except:
            break

def recive():
    while True:
        try:
            data = client.recv(Chunks)
            output_stream.write(data)
        except:
            break

send_thread = threading.Thread(target=send)
recive_thread = threading.Thread(target=recive)

send_thread.start()
recive_thread.start()

send_thread.join()
recive_thread.join()

input_stream.stop()
input_stream.close()
output_stream.stop()
output_stream.close()
p.terminate()