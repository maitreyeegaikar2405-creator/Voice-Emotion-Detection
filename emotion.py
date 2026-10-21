import subprocess
import io
import numpy as np
import soundfile as sf
import imageio_ffmpeg
from transformers import pipeline

print("Loading cross-lingual emotion model...")

emotion_model = pipeline(
    "audio-classification",
    model="Aniemore/wav2vec2-emotion-v1-crosslingual"
)

print("Emotion model loaded successfully!")


def detect_emotion(audio_file):

    print("Analyzing audio...")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg,
        "-i", audio_file,
        "-f", "wav",
        "-ac", "1",
        "-ar", "16000",
        "pipe:1"
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(result.stderr.decode())
        raise Exception("Audio conversion failed")

    audio_data, sample_rate = sf.read(
        io.BytesIO(result.stdout)
    )

    audio_data = np.asarray(
        audio_data,
        dtype=np.float32
    )

    prediction = emotion_model({
        "raw": audio_data,
        "sampling_rate": sample_rate
    })

    print("\nEmotion Result:")

    for item in prediction:
        print(
            "Emotion:",
            item["label"],
            "Confidence:",
            round(item["score"], 3)
        )

    return prediction