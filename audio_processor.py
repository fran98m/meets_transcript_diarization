import subprocess
import os
from pathlib import Path
import logging
import tempfile

logger = logging.getLogger('audio_processor')

def convert_video_to_audio(input_file, output_file=None):
    """Convert video to audio and save the file."""
    input_path = Path(input_file)
    if output_file is None:
        output_file = input_path.with_suffix('.wav')
    else:
        output_file = Path(output_file)

    output_file = output_file.with_suffix('.wav')  # Ensure .wav extension
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-i", str(input_path),
        "-vn",  # Disable video recording
        "-acodec", "pcm_s16le",  # Audio codec
        "-ar", "16000",  # Sample rate
        "-ac", "1",  # Number of audio channels
        "-y",  # Overwrite output file if it exists
        str(output_file)
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Successfully converted {input_file} to {output_file}")
        return str(output_file)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting file: {e}")
        logger.error(f"FFmpeg stderr: {e.stderr}")
        raise RuntimeError(f"Error converting file: {e}")

def convert_to_temp_wav(input_file):
    """Convert any audio/video file to a temporary WAV file."""
    input_path = Path(input_file)
    
    # Create a temporary file with .wav extension
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_wav_path = temp_file.name

    command = [
        "ffmpeg",
        "-i", str(input_path),
        "-vn",  # Disable video recording
        "-acodec", "pcm_s16le",  # Audio codec
        "-ar", "16000",  # Sample rate
        "-ac", "1",  # Number of audio channels
        "-y",  # Overwrite output file if it exists
        temp_wav_path
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Successfully converted {input_file} to temporary WAV file")
        return temp_wav_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting file: {e}")
        logger.error(f"FFmpeg stderr: {e.stderr}")
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
        raise RuntimeError(f"Error converting file: {e}")

def process_audio_file(file_path, save_output=False):
    """Process audio file to ensure it's in the correct format for Whisper and diarization."""
    if save_output:
        return convert_video_to_audio(file_path)
    else:
        return convert_to_temp_wav(file_path)