from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from io import BytesIO

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class captionModel:
    def __init__(self) -> None:
        self.model =  load_model("best_model.h5", compile=False)
        self.f_model =  self.feature_Model()
        self.captions =  self.get_captions()
        self.max_length = max(len(caption.split()) for caption in self.captions)
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(self.captions)
        self.vocab_size = len(self.tokenizer.word_index) + 1

    def feature_Model(self) -> Model:
        model = VGG16()
        model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
        return model

    async def get_features(self, image) -> np.ndarray:
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        feature = await self.f_model.predict(image, verbose=0)
        return feature

    def clean(self, mapping) -> None:
        for _, captions in mapping.items():
            for i in range(len(captions)):
                caption = captions[i]
                caption = caption.lower()
                caption = caption.replace('[^A-Za-z]', '')
                caption = caption.replace('\s+', ' ')
                caption = 'startseq ' + " ".join([word for word in caption.split() if len(word) > 1]) + ' endseq'
                captions[i] = caption

    def get_captions(self) -> list:
        with open("captions.txt", "r") as data:
            next(data)
            data = data.read()

        mapping = {}
        for line in data.split('\n'):
            tokens = line.split(',')
            if len(line) < 2:
                continue
            image_id, caption = tokens[0], tokens[1:]
            image_id = image_id.split('.')[0]
            caption = " ".join(caption)
            if image_id not in mapping:
                mapping[image_id] = []
            mapping[image_id].append(caption)

        self.clean(mapping)

        all_captions = []
        for key in mapping:
            for caption in mapping[key]:
                all_captions.append(caption)

        return all_captions

    def idx_to_word(self, integer):
        for word, index in self.tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    async def predict(self, img):
        in_text = 'startseq'
        for i in range(self.max_length):
            sequence = self.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], self.max_length)
            image = await self.get_features(img)
            yhat = await self.model.predict([image, sequence], verbose=0)
            yhat = np.argmax(yhat)
            word = self.idx_to_word(yhat)
            if word is None:
                break
            in_text += " " + word
            if word == 'endseq':
                break
        return in_text[9:-7].capitalize()

model = captionModel()

async def read_imagefile(file) -> np.ndarray:
    image = await load_img(BytesIO(file), target_size=(224, 224))
    return image

@app.post("/predict")
async def main(file: UploadFile = File(...)):
    try:
        image = read_imagefile(await file.read())
        prediction = await model.predict(image)
        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
