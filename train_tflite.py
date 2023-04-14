import tensorflow as tf
import tflite_model_maker as mm
from tflite_model_maker import audio_classifier
import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import itertools
import glob
import random

from IPython.display import Audio, Image
from scipy.io import wavfile


def train_tflite(train_data, test_data):
    train_data, validation_data = train_data.split(0.8)
    batch_size = 128
    epochs = 100
    
    spec = audio_classifier.YamNetSpec(
        keep_yamnet_and_custom_heads=True,
        frame_step=3 * audio_classifier.YamNetSpec.EXPECTED_WAVEFORM_LENGTH,
        frame_length=6 * audio_classifier.YamNetSpec.EXPECTED_WAVEFORM_LENGTH)
    model = audio_classifier.create(train_data, spec, validation_data,
                                    batch_size=batch_size,
                                    epochs=epochs)

    print('Evaluating test data: ')
    model.evaluate(test_data)

    models_path = './models'
    print(f'Exporting the TFLite model to {models_path}')

    model.export(models_path, tflite_filename='yamnet_model.tflite')
    model.export(models_path, export_format=[mm.ExportFormat.SAVED_MODEL, mm.ExportFormat.LABEL])
