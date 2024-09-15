import whisper
import torch
import warnings

# Suppress the specific FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

def load_whisper_model(model_name="large"):
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the model without weights_only parameter
    model = whisper.load_model(model_name, device=device)
    
    return model

# Load the model once when the module is imported
whisper_model = load_whisper_model()

def transcribe_audio(file_path):
    try:
        result = whisper_model.transcribe(str(file_path))
        return result
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        raise