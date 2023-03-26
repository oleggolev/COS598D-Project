import tensorflow_hub as hub
import tensorflow as tf

model = hub.load('https://tfhub.dev/google/humpback_whale/1')
tf.saved_model.save(model, "./model")
