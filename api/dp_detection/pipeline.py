import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class DPDetectionPipeline:
    def __init__(self, model_path="dp_detection/model"):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def predict(self, text):
        inputs = self.tokenizer(text, truncation=True, padding='max_length', max_length=128, return_tensors='pt')

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            self.model.eval()
            outputs = self.model(**inputs)
            logits = outputs.logits

        _, predicted_label = torch.max(logits, dim=1)
        predicted_label = predicted_label.item()

        return predicted_label
