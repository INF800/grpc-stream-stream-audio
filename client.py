import json
from datetime import datetime
import wave
from pathlib import Path
import time
import grpc
import numpy as np
import audio_stream_pb2
import audio_stream_pb2_grpc


THROTTLE_SECONDS = 15
SAMPLE_SIZE = 100

RESPONSE_CNTR = 0
TIMESTAMPS = {}


def generate_audio_chunks(audio_files_path):
    global TIMESTAMPS
    global RESPONSE_CNTR

    fps = sorted([*Path(audio_files_path).glob('**/*.wav')])
    for fp in fps:
        print(f'>>> sending ({RESPONSE_CNTR}of{SAMPLE_SIZE}):', fp)
        with wave.open(str(fp), 'rb') as wf:
            data = wf.readframes(wf.getnframes())
            TIMESTAMPS[RESPONSE_CNTR] = {'beg': datetime.now(), 'filepath': str(fp)}
            yield audio_stream_pb2.AudioChunk(data=data)
            
            time.sleep(THROTTLE_SECONDS)
            RESPONSE_CNTR+=1
            
            if RESPONSE_CNTR>SAMPLE_SIZE:
                for k in TIMESTAMPS.keys():
                    TIMESTAMPS[k]['beg'] = TIMESTAMPS[k]['beg'].isoformat()
                    if 'end' in TIMESTAMPS[k].keys():
                        TIMESTAMPS[k]['end'] = TIMESTAMPS[k]['end'].isoformat()
                        
                with open(f'benchfiles/{str(datetime.now()).replace(":", "-")}-timestamps-grpc.fasterwhisper.n{SAMPLE_SIZE}.json', 'w') as f:
                    json.dump(TIMESTAMPS, f, indent=4)

                break
            

def stream_audio(stub, audio_files_path):
    global TIMESTAMPS
    global RESPONSE_CNTR

    audio_chunks = generate_audio_chunks(audio_files_path)
    response_iterator = stub.StreamAudio(audio_chunks)
    
    for response in response_iterator:        
        TIMESTAMPS[RESPONSE_CNTR]['end'] = datetime.now()
        TIMESTAMPS[RESPONSE_CNTR]['diff'] = (TIMESTAMPS[RESPONSE_CNTR]['end'] - TIMESTAMPS[RESPONSE_CNTR]['beg']).total_seconds()
        TIMESTAMPS[RESPONSE_CNTR]['response'] = response.message
        
        print("\t<<<", "Server response:", f"({round(TIMESTAMPS[RESPONSE_CNTR]['diff'], 2)})" , response.message)


def main():
    # channel = grpc.insecure_channel('localhost:50051')
    channel = grpc.insecure_channel('8.tcp.ngrok.io:10519')
    stub = audio_stream_pb2_grpc.AudioStreamServiceStub(channel)

    audio_files_path = "/Users/clinicyantra/Desktop/projects/assemblyai-stt/chunks_intact_words/"
    stream_audio(stub, audio_files_path)

if __name__ == '__main__':
    main()
