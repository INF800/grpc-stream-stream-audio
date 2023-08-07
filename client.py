import wave
from pathlib import Path
import time
import grpc
import numpy as np
import audio_stream_pb2
import audio_stream_pb2_grpc


def generate_audio_chunks(audio_files_path):
    fps = sorted([*Path(audio_files_path).glob('**/*.wav')])
    for fp in fps:
        print('sending:', fp)
        with wave.open(str(fp), 'rb') as wf:
            data = wf.readframes(wf.getnframes())
            yield audio_stream_pb2.AudioChunk(data=data)
            time.sleep(3)

def stream_audio(stub, audio_files_path):
    audio_chunks = generate_audio_chunks(audio_files_path)
    response_iterator = stub.StreamAudio(audio_chunks)
    
    for response in response_iterator:
        print("Server response:", response.message)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = audio_stream_pb2_grpc.AudioStreamServiceStub(channel)

    audio_files_path = "/Users/clinicyantra/Desktop/projects/assemblyai-stt/chunks_intact_words/"
    stream_audio(stub, audio_files_path)

if __name__ == '__main__':
    main()
