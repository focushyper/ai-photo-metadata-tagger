import subprocess
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch
import os
import json
import inquirer
from termcolor import colored
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

MAX_KEYWORDS_LENGTH = 64  # Maximum length for the Keywords field

# Function to load allowed tags
def load_allowed_tags():
    with open('allowed_tags.json', 'r') as f:
        allowed_tags = json.load(f)
    return allowed_tags

# Function to load fixed keywords
def load_fixed_keywords():
    with open('fixed_keywords.json', 'r') as f:
        fixed_keywords = json.load(f)
    return fixed_keywords

# Function for recognizing objects and classifying images using ResNet50
def recognize_objects_resnet(image_path, model, top_n=5):
    # Load and process the image
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img = np.array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    # Predict the class of the object in the image
    predictions = model.predict(img)
    decoded_predictions = decode_predictions(predictions, top=top_n)[0]

    # Get the class labels
    class_labels = [class_name for _, class_name, _ in decoded_predictions]

    return class_labels

# Function for recognizing objects and classifying images using Hugging Face models
def recognize_objects_vit(image_path, processor, model, allowed_tags, top_n=5):
    # Load and process the image
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    
    # Predict the class of the object in the image
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    
    # Get the top N predictions
    top_n_predictions = torch.topk(logits, top_n).indices.squeeze(0).tolist()
    
    # Get the class labels
    class_labels = [model.config.id2label[idx] for idx in top_n_predictions]
    
    # Flatten the allowed tags into a single list
    all_allowed_tags = [item for sublist in allowed_tags.values() for item in sublist]
    
    # Filter the class labels to include only allowed tags
    filtered_labels = [label for label in class_labels if label in all_allowed_tags]
    
    return filtered_labels

# Function to truncate keywords to fit the maximum length
def truncate_keywords(keywords, max_length=MAX_KEYWORDS_LENGTH):
    truncated_keywords = []
    current_length = 0

    for keyword in keywords:
        if current_length + len(keyword) + 2 > max_length:  # +2 for ', ' separator
            break
        truncated_keywords.append(keyword)
        current_length += len(keyword) + 2

    return truncated_keywords

def main():
    print(colored("Welcome to the Image Classification and Tagging Script!", 'green'))
    
    # Check for Content directory
    content_dir = 'Content'
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)
        print(colored(f"Created a folder named '{content_dir}'. Please add your .jpg files to this folder.", 'yellow'))
        return
    
    # Interactive menu for selecting options
    questions = [
        inquirer.Confirm('use_vit', message="Do you want to use a Hugging Face model?", default=False),
        inquirer.Path('image_dir', message="Enter the directory path containing .jpg files", default=content_dir)
    ]

    answers = inquirer.prompt(questions)
    
    image_dir = answers['image_dir']
    if not os.path.exists(image_dir):
        print(colored(f"The directory '{image_dir}' does not exist.", 'red'))
        return

    if answers['use_vit']:
        questions.extend([
            inquirer.Text('model_name', message="Enter the Hugging Face model name (e.g., 'google/vit-base-patch16-224')"),
            inquirer.Text('processor_name', message="Enter the Hugging Face processor name (e.g., 'google/vit-base-patch16-224')"),
            inquirer.Confirm('use_allowed_keywords', message="Do you want to use allowed keywords?", default=True),
            inquirer.Confirm('use_fixed_keywords', message="Do you want to use fixed keywords?", default=True)
        ])
        answers = inquirer.prompt(questions)

        # Load the processor and model
        processor = ViTImageProcessor.from_pretrained(answers['processor_name'])
        model = ViTForImageClassification.from_pretrained(answers['model_name'])
        
        # Load allowed tags and fixed keywords
        allowed_tags = load_allowed_tags() if answers['use_allowed_keywords'] else {}
        fixed_keywords = load_fixed_keywords() if answers['use_fixed_keywords'] else []

        # Get a list of .jpg files in the specified directory
        image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.jpg')]

        # Process each image
        for image_file in image_files:
            image_path = os.path.abspath(image_file)
            results = recognize_objects_vit(image_path, processor, model, allowed_tags)

            # Combine fixed keywords and recognized keywords
            all_keywords = fixed_keywords + results
            
            # Truncate the list of keywords to fit the maximum length
            truncated_keywords = truncate_keywords(all_keywords)
            
            # Convert the list of class labels to a comma-separated string
            classes_str = ', '.join(truncated_keywords)
            
            # Write metadata using ExifTool
            subprocess.run(['exiftool', '-overwrite_original', f'-Keywords={classes_str}', image_path])
    else:
        # Use the default ResNet50 model
        model = ResNet50(weights='imagenet')

        # Load allowed tags and fixed keywords
        allowed_tags = load_allowed_tags() if inquirer.prompt([inquirer.Confirm('use_allowed_keywords', message="Do you want to use allowed keywords?", default=True)])['use_allowed_keywords'] else {}
        fixed_keywords = load_fixed_keywords() if inquirer.prompt([inquirer.Confirm('use_fixed_keywords', message="Do you want to use fixed keywords?", default=True)])['use_fixed_keywords'] else []

        # Get a list of .jpg files in the specified directory
        image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.jpg')]

        # Process each image
        for image_file in image_files:
            image_path = os.path.abspath(image_file)
            results = recognize_objects_resnet(image_path, model)

            # Combine fixed keywords and recognized keywords
            all_keywords = fixed_keywords + results
            
            # Truncate the list of keywords to fit the maximum length
            truncated_keywords = truncate_keywords(all_keywords)
            
            # Convert the list of class labels to a comma-separated string
            classes_str = ', '.join(truncated_keywords)
            
            # Write metadata using ExifTool
            subprocess.run(['exiftool', '-overwrite_original', f'-Keywords={classes_str}', image_path])

    print(colored("Processing completed. Metadata updated.", 'green'))

if __name__ == "__main__":
    main()
