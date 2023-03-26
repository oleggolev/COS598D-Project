import tensorflow as tf

model = tf.saved_model.load("./model.pth")

# FILENAME = 'gs://bioacoustics-www1/sounds/Cross_02_060203_071428.d20_7.wav'
# waveform, sample_rate = tf.audio.decode_wav(tf.io.read_file(FILENAME))

# waveform = tf.expand_dims(waveform, 0)  # makes a batch of size 1
# context_step_samples = tf.cast(sample_rate, tf.int64)
score_fn = model.signatures['score']
# scores = score_fn(waveform=waveform, context_step_samples=context_step_samples)
# print(scores)