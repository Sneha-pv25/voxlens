import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import optimizers

# Function to handle the deprecated 'lr' argument
def update_optimizer_lr(optimizer_config):
    if 'lr' in optimizer_config:
        print("Found 'lr' parameter, changing it to 'learning_rate'.")
        optimizer_config['learning_rate'] = optimizer_config.pop('lr')
    return optimizer_config

# Path to the original model
model_path = 'D:\\Fake-speech-recognition-master\\model\\model.h5'

# Load the model with custom deserialization
def load_and_update_model(model_path):
    # Load the model without compiling first
    model = load_model(model_path, compile=False)

    # Check if the optimizer exists and update if needed
    if hasattr(model, 'optimizer') and model.optimizer:
        optimizer_config = model.optimizer.get_config()
        updated_optimizer_config = update_optimizer_lr(optimizer_config)

        # Create a new optimizer with the updated configuration
        model.optimizer = optimizers.Adam(**updated_optimizer_config)
    else:
        print("No optimizer found in the model. Using a new one.")
        # Create a new optimizer if none exists
        model.optimizer = optimizers.Adam(learning_rate=0.001)

    # Compile the model again with the updated optimizer
    model.compile(optimizer=model.optimizer, loss=model.loss, metrics=model.metrics)

    return model

# Load and update the model
updated_model = load_and_update_model(model_path)

# Save the updated model
updated_model_path = 'D:\\Fake-speech-recognition-master\\model\\model_updated.h5'
updated_model.save(updated_model_path)

print(f"Model saved successfully to {updated_model_path}")
