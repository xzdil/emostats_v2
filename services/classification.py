import random

class ClassificationService:
    def __init__(self):
        pass

    def create_classification(self, text):
        return {"classification": random.choice([1, 2, 3]), "classification_confidence": random.uniform(0, 1)}
