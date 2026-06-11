import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment

def convert_to_wav(input_path, output_path):
    """Convert any audio file to WAV format."""
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def process_wav_file(file_path, target_sr=16000):
    """Process audio file and generate spectrogram."""
    # Create a directory for spectrograms if it doesn't exist
    spec_dir = os.path.join(os.getcwd(), "static", "spectrograms")
    os.makedirs(spec_dir, exist_ok=True)
    
    # If file is not wav, convert it
    if not file_path.lower().endswith('.wav'):
        wav_path = file_path.rsplit('.', 1)[0] + '.wav'
        convert_to_wav(file_path, wav_path)
        file_path = wav_path

    try:
        # Load and preprocess audio
        audio, sr = librosa.load(file_path, sr=target_sr)
        
        # Ensure consistent length (5 seconds)
        target_length = 5 * target_sr
        if len(audio) < target_length:
            audio = np.pad(audio, (0, target_length - len(audio)))
        else:
            audio = audio[:target_length]
        
        # Generate mel spectrogram
        mel_spect = librosa.feature.melspectrogram(
            y=audio,
            sr=target_sr,
            n_mels=128,
            fmax=8000
        )
        
        # Convert to log scale
        mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)
        
        # Generate and save spectrogram image
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(
            mel_spect_db,
            sr=target_sr,
            x_axis='time',
            y_axis='mel',
            fmax=8000
        )
        plt.colorbar(format='%+2.0f dB')
        
        # Save spectrogram
        spec_path = os.path.join(spec_dir, os.path.basename(file_path).rsplit('.', 1)[0] + '_spec.png')
        plt.savefig(spec_path)
        plt.close()
        
        # Normalize the mel spectrogram for model input
        mel_spect_db = (mel_spect_db - mel_spect_db.mean()) / mel_spect_db.std()
        
        return mel_spect_db, '/static/spectrograms/' + os.path.basename(spec_path)
        
    except Exception as e:
        raise Exception(f"Error processing audio file: {str(e)}")
    
    finally:
        # Clean up temporary files
        try:
            os.remove(file_path)
        except:
            pass