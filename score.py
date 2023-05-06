import re
import itertools
from pathlib import PurePath
from pydub import AudioSegment
from google.cloud import storage
import torchaudio
import tensorflow as tf
import tensorflow_io as tfio
from sample import get_data

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./abc.json"
BUCKET = "noaa-passive-bioacoustic"
CLIENT = "COS598D-Whale"

def get_filename_path(sample):
    parts = sample['flac_compressed_xwav_object'].split("/")[3:]
    location_separated = [frag.lower() for frag in ["".join(char) for _, char in itertools.groupby(parts[2], key=str.isdigit)]]
    blob_path = "/".join([parts[0], "audio", "pipan", parts[1].lower(), "pipan_" + "_".join([parts[1].lower(),location_separated[1]]), parts[3], parts[4]])
    local_filename = parts[4]
    local_filename_path = "./samples_flac/" + local_filename
    return (local_filename, blob_path, local_filename_path)

# For each sample, download the audio file.
data = get_data()
for i, sample in enumerate(data):
    # Process the filename. Since the dataset was released, the paths changed.
    # Path in the csv: gs://noaa-passive-bioacoustic/pifsc/Hawaii/Hawaii14/audio/Hawaii_K_14_121216_190000.df20.x.flac
    # Actual web path: gs://noaa-passive-bioacoustic/pifsc/audio/pipan/hawaii/pipan_hawaii_14/audio/Hawaii_K_14_121216_190000.df20.x.flac
    local_filename, blob_path, local_filename_path = get_filename_path(sample)

    # Download the sample file, if not already present.
    if not os.path.isfile(local_filename_path):
        storage_client = storage.Client(CLIENT)
        bucket = storage_client.get_bucket(BUCKET)
        blob = bucket.blob(blob_path)
        blob.download_to_filename(local_filename_path)
        print("Downloaded", local_filename)

    # Convert the flac file to wav.
    flac_audio_path = PurePath(local_filename_path)
    wav_audio_file = flac_audio_path.name.replace(flac_audio_path.suffix, "") + ".wav"
    wav_audio_path = "./samples_wav/" + wav_audio_file
    
    if not os.path.isfile(wav_audio_path):
        flac_audio = AudioSegment.from_file(flac_audio_path, flac_audio_path.suffix[1:])
        flac_audio.export(wav_audio_path, format="wav")

    # Cut out the desired section. Save the cutout section with its label.
    subchunk_start = int(sample["subchunk_index"]) * 75.0
    t1 = subchunk_start + float(sample["begin_rel_subchunk"]) - 2
    t2 = subchunk_start + float(sample["end_rel_subchunk"]) + 2
    newAudio = AudioSegment.from_wav(wav_audio_path)
    try:
        newAudio = newAudio[t1:t2]
        # Save the clip in the following format:
        # ./clips/<label>-<starting timestamp from original recording>-<name_of_file>
        clip_path = "/scratch/network/ogolev/clips/" + sample["label"] + "-" + str(t1) + "-" + wav_audio_file
        newAudio.export(clip_path, format="wav")

        # Delete flac and wav files.
        _, _, new_local_filename_path = get_filename_path(data[i+1])
        if new_local_filename_path != local_filename_path:
            os.remove(local_filename_path)
            os.remove(wav_audio_path)
    except:
        # Delete flac and wav files.
        _, _, new_local_filename_path = get_filename_path(data[i+1])
        if new_local_filename_path != local_filename_path:
            os.remove(local_filename_path)
            os.remove(wav_audio_path)
