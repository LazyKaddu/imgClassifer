import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import ResNet50  # You can use other base models like InceptionV3, MobileNetV2, etc.
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Define the base model with pre-trained weights from ImageNet
base_model = ResNet50(weights='imagenet', include_top=False)  # You can change the base model as needed
num_classes=10
# Add custom layers on top of the base model
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)  # Add your own dense layers as needed
predictions = Dense(num_classes, activation='softmax')(x)  # num_classes is the number of classes in your classification problem

k=0
initial = np.zeros((1,512,512,3))
label = [-1,]
for i in DATAIMG:
  print(k)
  Data = np.load(f'/content/drive/MyDrive/imgClassifer/datanpy/data{i}.npy',allow_pickle=False)
  
  features = np.concatenate((initial,Data))
  initial = None
  initial = features
  feature = None

  for j in Data:
     label.append(k)
  k+=1
label = np.array(label)
DATASET = tf.data.Dataset.from_tensor_slices((features, label))

def stabalize(obj):
  return obj/255

DATASET = DATASET.batch(32)
DATASET = DATASET.shuffle(3, reshuffle_each_iteration=True)

model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_data, train_labels, epochs=epochs, batch_size=batch_size, validation_data=(val_data, val_labels))

test_loss, test_accuracy = model.evaluate(test_data, test_labels)
print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_accuracy}')

predictions = model.predict(test_data)

model.save_weights('modelWeights.ckpt')
