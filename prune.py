import os
import tensorflow as tf
import numpy as np
from tensorflow_model_optimization.sparsity import keras as sparsity


def prune(model, train_ds, val_ds):
    num_train_samples = 100
    batch_size = 128
    epochs = 4
    end_step = np.ceil(1.0 * num_train_samples / batch_size).astype(np.int32) * epochs
    '''
    pruning_params = {
        'pruning_schedule': sparsity.PolynomialDecay(initial_sparsity = 0.5,
                                                     final_sparsity = 0.9,
                                                     begin_step = 0,
                                                     end_step = end_step,
                                                     frequency = 100)
    }
    pruned_model = sparsity.prune_low_magnitude(model, **pruning_params)
    pruned_model.summary()
    '''
    pruned_model = model
    log_dir = '.models'
    callbacks = [
        sparsity.UpdatePruningStep(),
        sparsity.PruningSummaries(log_dir=log_dir),
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    ]
    
    pruned_model.compile(
        loss = tf.keras.losses.binary_crossentropy,
        optimizer = 'adam',
        metrics = ['accuracy'])
    pruned_model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)
    return pruned_model
