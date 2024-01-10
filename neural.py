from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import os


# Supondo que a pasta 'images' está no mesmo diretório que seu script
dataset_dir = 'images'  

# Carregar o modelo VGG16 pré-treinado sem a camada superior (top)
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Congelar os pesos do modelo base
for layer in base_model.layers:
    layer.trainable = False

# Adicionar novas camadas superiores para a tarefa específica
x = Flatten()(base_model.output)
x = Dense(256, activation='relu')(x)
predictions = Dense(2, activation='softmax')(x)  # Alterado para 2, já que temos 2 categorias: cat e dog

# Construir o modelo final
model = Model(inputs=base_model.input, outputs=predictions)

# Compilar o modelo
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Geradores de dados para aumentação de imagem
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, zoom_range=0.2, shear_range=0.2)
test_datagen = ImageDataGenerator(rescale=1./255)

# Preparar fluxo de dados
train_generator = train_datagen.flow_from_directory(
    os.path.join(dataset_dir, 'train'),
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    os.path.join(dataset_dir, 'validation'),
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

# Treinar o modelo
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // 32,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // 32)
