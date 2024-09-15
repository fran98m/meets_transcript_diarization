import logging
import os
from pathlib import Path
import warnings
from path_converter import convert_windows_path_to_wsl
from audio_processor import process_audio_file
from transcriber import transcribe_audio
from diarizer import diarize_audio

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='whisper_transcription.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger('whisper_transcription')

def process_audio(file_path, num_speakers=None, save_audio=False):
    converted_file = None
    try:
        logger.info(f"Processing {file_path}")
        
        # Convert to appropriate audio format
        converted_file = process_audio_file(file_path, save_output=save_audio)
        
        # Transcribe with Whisper
        transcription = transcribe_audio(converted_file)
        
        # Perform diarization
        diarization = diarize_audio(converted_file, num_speakers)
        
        # Combine results
        final_output = []
        for segment in transcription["segments"]:
            start, end, text = segment["start"], segment["end"], segment["text"]
            # Find the corresponding speaker for this segment
            speaker_label = "Unknown"
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                if turn.start <= start < turn.end:
                    speaker_label = speaker
                    break
            final_output.append(f"[{speaker_label}] ({start:.2f}-{end:.2f}): {text}")
        
        return "\n".join(final_output)
    except Exception as e:
        logger.error(f"Error processing {file_path}: {str(e)}")
        logger.exception("Exception details:")
        return None
    finally:
        # Clean up the temporary file if it wasn't saved
        if not save_audio and converted_file and os.path.exists(converted_file):
            os.remove(converted_file)
            logger.info(f"Removed temporary file: {converted_file}")

def main():
    logger.info("Starting Whisper transcription and diarization script")
    
    while True:
        print("\nChoose an operation:")
        print("1. Process audio/video file")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == '1':
            windows_path = input("Enter the Windows path to the audio/video file: ").strip()
            wsl_path = convert_windows_path_to_wsl(windows_path)
            path = Path(wsl_path)
            
            if not path.exists():
                logger.error(f"The path {path} does not exist.")
                continue
            
            if not path.is_file():
                logger.error(f"The path {path} is not a file.")
                continue
            
            save_audio = input("Do you want to save the converted audio file? (y/n): ").strip().lower() == 'y'
            
            num_speakers = input("Enter the number of speakers (leave blank for auto-detection): ").strip()
            num_speakers = int(num_speakers) if num_speakers else None
            
            transcription = process_audio(path, num_speakers, save_audio)
            if transcription:
                output_file = path.with_suffix('.txt')
                with open(output_file, 'w') as f:
                    f.write(transcription)
                logger.info(f"Transcription with diarization saved to {output_file}")
        
        elif choice == '2':
            logger.info("Exiting script")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()