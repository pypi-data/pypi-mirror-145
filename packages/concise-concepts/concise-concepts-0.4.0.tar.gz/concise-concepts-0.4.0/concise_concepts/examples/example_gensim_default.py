import concise_concepts
import gensim
import gensim.downloader as api
import spacy

from .data import data, text

model_path = "glove-twitter-25"

nlp = spacy.blank('en')

nlp.add_pipe("concise_concepts", config={"data": data, "model_path": model_path})

doc = nlp(text)
print([(ent.text, ent.label_) for ent in doc.ents])
