import whisper
import imageio_ffmpeg
import subprocess
import numpy as np
import soundfile as sf
import io

from translation import hindi_to_roman


print("Loading Whisper model...")

model = whisper.load_model("small")

print("Whisper model loaded successfully!")


def transcribe_audio(audio_file, language):

    print("\nTranscribing audio...")

    # Get FFmpeg bundled with imageio-ffmpeg
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

    # Read converted audio
    audio_data, sample_rate = sf.read(
        io.BytesIO(result.stdout)
    )

    audio_data = np.asarray(
        audio_data,
        dtype=np.float32
    )

    # Select Whisper language manually
    if language == "English":
        whisper_language = "en"
    else:
        whisper_language = "hi"

    # Transcribe
    result = model.transcribe(
        audio_data,
        language=whisper_language,
        task="transcribe",
        fp16=False,
        temperature=0,
        condition_on_previous_text=False
    )

    text = result["text"].strip()

    # Hindi → Roman aHindi
    if language == "Hindi":
        text = hindi_to_roman(text)

    print("\nFinal Transcript:")
    print(text)

    return text