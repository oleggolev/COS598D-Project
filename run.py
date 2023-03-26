import tensorflow_hub as hub
import tensorflow as tf

model = tf.saved_model.load("./model")

FILENAME = 'gs://bioacoustics-www1/sounds/Cross_02_060203_071428.d20_7.wav'

waveform, _ = tf.audio.decode_wav(tf.io.read_file(FILENAME))
waveform = tf.expand_dims(waveform, 0)  # makes a batch of size 1

pcen_spectrogram = model.front_end(waveform)
context_window = pcen_spectrogram[:, :128, :]
features = model.features(context_window)
logits = model.logits(context_window)
probabilities = tf.nn.sigmoid(logits)

print({
    'pcen_spectrogram': pcen_spectrogram,
    'features': features,
    'logits': logits,
    'probabilities': probabilities,
})
