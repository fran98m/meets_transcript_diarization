from pyannote.audio import Pipeline
from config import HF_AUTH_TOKEN
import logging
import torch

logger = logging.getLogger('diarizer')

# Check if CUDA is available and set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the pipeline
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                                use_auth_token=HF_AUTH_TOKEN)

# Move the pipeline to the appropriate device
diarization_pipeline.to(device)

def diarize_audio(file_path, num_speakers=None):
    try:
        logger.info(f"Diarizing audio file: {file_path}")
        logger.info(f"Using device: {device}")
        diarization = diarization_pipeline(str(file_path), num_speakers=num_speakers)

        # Extract labels from the tuples returned by itertracks
        detected_speakers = len(set(segment[-1] for segment in diarization.itertracks(yield_label=True))) 

        if num_speakers and detected_speakers < num_speakers:
            logger.warning(f"Detected {detected_speakers} speakers, but {num_speakers} were expected.")

        return diarization
    except Exception as e:
        logger.error(f"Error in diarization: {str(e)}\n{traceback.format_exc()}") 
        raise