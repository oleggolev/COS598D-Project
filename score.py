import re
import itertools
from pathlib import PurePath
from pydub import AudioSegment
from google.cloud import storage
import torchaudio
import tensorflow as tf
import tensorflow_io as tfio
from sample import get_samples

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/oleggolev/.config/gcloud/legacy_credentials/ogolev@princeton.edu/adc.json"
BUCKET = "noaa-passive-bioacoustic"
CLIENT = "COS598D-Whale"

# For each sample, download the audio file.
for sample in get_samples(1):
    # Process the filename. Since the dataset was released, the paths changed.
    # Path in the csv: gs://noaa-passive-bioacoustic/pifsc/Hawaii/Hawaii14/audio/Hawaii_K_14_121216_190000.df20.x.flac
    # Actual web path: gs://noaa-passive-bioacoustic/pifsc/audio/pipan/hawaii/pipan_hawaii_14/audio/Hawaii_K_14_121216_190000.df20.x.flac
    parts = sample['flac_compressed_xwav_object'].split("/")[3:]
    location_separated = [frag.lower() for frag in ["".join(char) for _, char in itertools.groupby(parts[2], key=str.isdigit)]]
    blob_path = "/".join([parts[0], "audio", "pipan", parts[1].lower(), "pipan_" + "_".join([parts[1].lower(),location_separated[1]]), parts[3], parts[4]])
    local_filename = parts[4]
    local_filename_path = "./samples_flac/" + local_filename
    print("Downloading", local_filename)

    # Download the sample file.
    storage_client = storage.Client(CLIENT)
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(blob_path)
    blob.download_to_filename(local_filename_path)
    print("Downloaded", local_filename)

    # Convert the flac file to wav.
    flac_audio_path = PurePath(local_filename_path)
    flac_audio = AudioSegment.from_file(flac_audio_path, flac_audio_path.suffix[1:])
    wav_audio_path = flac_audio_path.name.replace(flac_audio_path.suffix, "") + ".wav"
    flac_audio.export("samples_wav/" + wav_audio_path, format="wav")
    
    # Cut out the desired section. Save the cutout section. Delete flac and wav files.
    subchunk_start = int(sample["subchunk_index"]) * 75.0
    t1 = subchunk_start + float(sample["begin_rel_subchunk"])
    t2 = subchunk_start + float(sample["end_rel_subchunk"])
    newAudio = AudioSegment.from_wav("samples_wav/" + wav_audio_path)
    newAudio = newAudio[t1:t2]
    newAudio.export(wav_audio_path.replace("samples_wav/", "clips/")., format="wav") #Exports to a wav file in the current path.
