import tensorflow as tf
import numpy as np

from sklearn.utils import class_weight

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model



# ==================================================
# Settings
# ==================================================

DATASET_PATH = "dataset"

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 60



# ==================================================
# Data Generator
# ==================================================

datagen = ImageDataGenerator(

    rescale=1.0 / 255,

    validation_split=0.20,

    rotation_range=20,

    width_shift_range=0.15,

    height_shift_range=0.15,

    zoom_range=0.15,

    shear_range=0.1,

    horizontal_flip=True

)



train_data = datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    subset="training",

    shuffle=True

)



val_data = datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    subset="validation",

    shuffle=False

)



# ==================================================
# Class Order
# ==================================================

print("\n==============================")
print("CLASS INDICES")
print(train_data.class_indices)
print("==============================\n")



# ==================================================
# Class Weight Calculation
# ==================================================

weights = class_weight.compute_class_weight(

    class_weight="balanced",

    classes=np.unique(train_data.classes),

    y=train_data.classes

)



class_weights = dict(

    enumerate(weights)

)



print("CLASS WEIGHTS:")
print(class_weights)



# ==================================================
# MobileNetV2
# ==================================================

base_model = MobileNetV2(

    weights="imagenet",

    include_top=False,

    input_shape=(224,224,3)

)



base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False



# ==================================================
# Build Model
# ==================================================

x = base_model.output

x = GlobalAveragePooling2D()(x)

x = Dropout(0.3)(x)



output = Dense(

    1,

    activation="sigmoid"

)(x)



model = Model(

    inputs=base_model.input,

    outputs=output

)



# ==================================================
# Compile
# ==================================================

# ==================================================
# Compile
# ==================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)



model.summary()



# ==================================================
# Train Model
# ==================================================

history = model.fit(

    train_data,

    validation_data=val_data,

    epochs=EPOCHS,

    class_weight=class_weights

)



# ==================================================
# Save Model
# ==================================================

model.save("dental_model.keras")



print("\n==============================")
print("MODEL SAVED SUCCESSFULLY")
print("TRAINING COMPLETED")
print("==============================")