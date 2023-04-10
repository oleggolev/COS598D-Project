import re
import csv
import random
import itertools
import tensorflow as tf
import tensorflow_io as tfio

N = 10          # number of samples from all annotated audio files
SEED = 69420    # fixed seed to ensure the same sample are drawn

"""
Headers:
[0] audit_name
[1] flac_compressed_xwav_object
[2] subchunk_index
[3] label_is_strong
[4] implicit_negatives
[5] label
[6] begin_rel_subchunk
[7] end_rel_subchunk
[8] begin_utc,end_utc
"""
headers = []
data = []
with open('./detections/annotations.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in reader:
        if line_count == 0:
            headers = row
        else:
            obj = {}
            for i in range(len(headers)):
                obj[headers[i]] = row[i]
            data.append(obj)
        line_count += 1

# Sample the same N instances out of the 38857 data points
random.seed(SEED)
samples = random.sample(data, N)

# For each sample, download the audio file, and cut out the target interval.
for sample in samples:
    # Process the filename. Since the dataset was released, the paths changed.
    # Path in the csv: gs://noaa-passive-bioacoustic/pifsc/Hawaii/Hawaii14/audio/Hawaii_K_14_121216_190000.df20.x.flac
    # Actual web path: gs://noaa-passive-bioacoustic/pifsc/audio/pipan/hawaii/pipan_hawaii_14/audio/Hawaii_K_14_121216_190000.df20.x.flac
    parts = sample['flac_compressed_xwav_object'].split("/")[2:]
    location_separated = [frag.lower() for frag in ["".join(char) for _, char in itertools.groupby(parts[3], key=str.isdigit)]]
    filename = "gs://" + "/".join([parts[0], parts[1], "audio", "pipan", parts[2].lower(), "pipan_" + "_".join([parts[2].lower(),location_separated[1]]), parts[4], parts[5]])
    print("Downloading", filename)
    
    # Attempt to obtain the file. Some files may be missing.
    try:
        flac_file = tf.io.read_file(filename)
        print("Downloaded", filename)
    except Exception as e:
        print("Failed to get", filename, e)
