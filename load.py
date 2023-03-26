import tensorflow as tf
import tensorflow_hub as hub

model = hub.load('https://kaggle.com/models/google/humpback-whale/frameworks/TensorFlow2/variations/humpback-whale/versions/1')
tf.saved_model.save(model, './model.pth')
