import csv
import random

# Fixed seed to ensure the same sample is drawn every time.
SEED = 69420

def get_samples(n):
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
    return random.sample(data, n)