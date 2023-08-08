import datetime
import wave
import grpc
import numpy as np
import audio_stream_pb2
import audio_stream_pb2_grpc
from concurrent import futures
import joblib
from faster_whisper.transcribe import WhisperModel


model = WhisperModel('small.en')


def transcribe(binary_wave_data):
    audio_array = bytes_to_float_array(binary_wave_data)
    generator, _ = model.transcribe(audio_array)
    text = str([e.text for e in generator])
    return text


def bytes_to_float_array(audio_bytes):
    raw_data = np.frombuffer(
        buffer=audio_bytes, dtype=np.int16
    )
    return raw_data.astype(np.float32) / 32768.0


class AudioStreamServicer(audio_stream_pb2_grpc.AudioStreamServiceServicer):
    def StreamAudio(self, request_iterator, context):
        cntr = 0
        for audio_chunk in request_iterator:
            # Process the audio chunk here (e.g., save to a file, analyze, etc.)
            print(f"[SERVER] Received audio chunk: {len(audio_chunk.data)} bytes")
            
            beg = datetime.datetime.now()
            text = transcribe(audio_chunk.data)
            diff = datetime.datetime.now()-beg
            print("\tProcessed in:", round(diff.total_seconds(),3))

            response = audio_stream_pb2.AudioResponse(message=text)
            yield response
            cntr+=1

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_stream_pb2_grpc.add_AudioStreamServiceServicer_to_server(AudioStreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
