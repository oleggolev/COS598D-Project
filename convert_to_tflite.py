import tensorflow as tf

def convert_to_tflite(model):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tfl_model = converter.convert()
    with open('model/saved_model.tflite', 'wb') as f:
        f.write(tfl_model)
