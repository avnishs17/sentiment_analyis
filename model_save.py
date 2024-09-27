import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'
save_directory = 'model/model_cache'

# Ensure the directory exists
os.makedirs(save_directory, exist_ok=True)

print(f"Downloading model: {model_name}")
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

print(f"Saving model to: {save_directory}")
try:
    model.save_pretrained(save_directory)
    print("Model saved successfully.")
except Exception as e:
    print(f"Error saving model: {e}")

print(f"Saving tokenizer to: {save_directory}")
try:
    tokenizer.save_pretrained(save_directory)
    print("Tokenizer saved successfully.")
except Exception as e:
    print(f"Error saving tokenizer: {e}")

# Verify files were saved
print("\nChecking saved files:")
for root, dirs, files in os.walk(save_directory):
    for file in files:
        print(os.path.join(root, file))

if not os.listdir(save_directory):
    print(f"Warning: {save_directory} is empty!")
else:
    print(f"\nFiles successfully saved to {save_directory}")

# Check write permissions
if os.access(save_directory, os.W_OK):
    print(f"Write permission is granted on {save_directory}")
else:
    print(f"No write permission on {save_directory}")