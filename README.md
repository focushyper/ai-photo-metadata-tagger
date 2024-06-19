# Automated AI Keyword Tagging Metadata Script for Photographers

[Diginaat](https://www.diginaat.com)

Welcome to the Automated AI Keyword Tagging Metadata Script! This tool is designed specifically for photographers to help streamline the process of adding relevant keywords to their photos. By leveraging AI models, this script automatically generates and updates the metadata of your images with appropriate tags.


## Features
- **AI-Powered Tagging**: Uses pre-trained AI models to automatically generate keywords for your photos.
- **Supports Hugging Face Models**: Option to use custom Hugging Face models for more tailored keyword tagging.
- **Interactive Command-Line Interface**: Easy-to-use interactive CLI for configuring your settings.
- **Batch Processing**: Processes all images in a specified directory and updates their metadata.
- **Customizable Keywords**: Supports custom allowed and fixed keywords.

## Prerequisites
- Python 3.8 or newer
- Pip (Python package installer)



## Setup Guide

### Step 1: Download and Install Python
If you don't have Python installed, download and install Python 3.8 or newer from [python.org](https://www.python.org/downloads/).


### Step 2: Clone the Repository
Clone this repository or download the files to your local machine.


### Step 3: Prepare the Directory
Ensure you have the following files in the same directory:
- `script.py` (main script)
- `requirements.txt` (list of required Python packages)
- `run_script.bat` (batch file to run the script)
- `allowed_tags.json` (file with allowed tags)
- `fixed_keywords.json` (file with fixed keywords)
- `custom_models.json` (file with custom Hugging Face models)


### Step 4: Add Images
Create a directory named `Content` in the same location as the above files. Add the images you want to process (with `.jpg` extension) to this directory.



### Step 5: Run the Batch File
Double-click the `run_script.bat` file. This will:
1. Check if Python and Pip are installed.
2. Install the required Python packages listed in `requirements.txt`.
3. Run the `script.py` script.



## How to Use the Script

When you run the batch file, you will be prompted to make several choices:

1. **Choose Model Type**: You can choose to use a Hugging Face model or the default ResNet50 model.
2. **Enter Image Directory**: Specify the directory containing your `.jpg` files (default is `Content`).
3. **Select Model**: If you choose to use a Hugging Face model, select a model from the list of custom models defined in `custom_models.json`.
4. **Use Allowed Keywords**: Decide whether to use the allowed keywords defined in `allowed_tags.json`.
5. **Use Fixed Keywords**: Decide whether to use the fixed keywords defined in `fixed_keywords.json`.



### Example Interaction

Welcome to the Image Classification and Tagging Script!
Do you want to use a Hugging Face model? [Y/n] y
Enter the directory path containing .jpg files [Content]:
Select a model to use:
[1] ViT Model
[2] ResNet Model
Choose a model: 1
Do you want to use allowed keywords? [Y/n] y
Do you want to use fixed keywords? [Y/n] y


The script will then process each image in the specified directory, predict tags, and update the image metadata with the predicted tags.

## Understanding the Script

### script.py
- **Dependencies**: The script uses `transformers`, `torch`, `Pillow`, `inquirer`, `termcolor`, and `tensorflow`.
- **Functions**:
  - `load_allowed_tags()`: Loads allowed tags from `allowed_tags.json`.
  - `load_fixed_keywords()`: Loads fixed keywords from `fixed_keywords.json`.
  - `load_custom_models()`: Loads custom models from `custom_models.json`.
  - `recognize_objects_resnet(image_path, model, top_n=5)`: Uses ResNet50 to predict image tags.
  - `recognize_objects_vit(image_path, processor, model, allowed_tags, top_n=5)`: Uses Hugging Face models to predict image tags.
  - `truncate_keywords(keywords, max_length=64)`: Truncates keywords to fit the IPTC length limit.
  - `main()`: The main function that runs the script and handles user interactions.

### requirements.txt
Lists all the required Python packages to be installed.

### run_script.bat
A batch file that:
1. Checks if Python and Pip are installed.
2. Installs the required packages.
3. Runs the `script.py` script.

### allowed_tags.json
A JSON file containing the allowed tags to be used in the metadata.


### fixed_keywords.json
A JSON file containing fixed keywords to be added to every image's metadata.


### custom_models.json
A JSON file allowing users to specify custom Hugging Face models and processors.


## Contributing
Feel free to submit issues or pull requests if you have any suggestions or improvements.

## License
This project is licensed under the MIT License.

---

For more information, visit [Diginaat](https://www.diginaat.com).
