import json
import requests

import os


# ----- HUGGINGFACE API -----

# The model that we use for object detection.
API_URL_OBJDET = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50" 

# The model that we use for image classification.
API_URL_IMGCLASS = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

# The token we generated to connect with HuggingFace.
API_TOKEN = "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"


# Reusable function for interacting with the Hugging Face API.
def query(file_path, api_url, api_token):
    
    # Construct the header of the HTTP request that includes the API token.
    headers = {"Authorization": f"Bearer " + api_token}
    # Read the input data.
    with open(file_path, "rb") as f:
        data = f.read()
    # Make a POST request to the API with the token and input data.
    response = requests.request("POST", api_url, headers=headers, data=data)
    # Return the output from the API
    return json.loads(response.content.decode("utf-8"))
  

# ----- COUNT OBJECT FUNCTION -----
  
# Count objects using the Object Detection Model:
def count_objects(file_path, api_url, api_token, label):
  
  data = query(file_path, API_URL_OBJDET, API_TOKEN)
  count = 0
  for d in data:
      if d["label"] == label:
          count += 1
  return count


# Folder of images
dir = "data/"

# Labels to count
labels = ["car","bicycle","motorcycle","truck","person"]



# ----- FOR LOOP TO PRINT IMAGE DATA -----

# For-loop in which the AI looks at each picture for each object:
for image in sorted(os.listdir(dir)):

  # Create empty string for images to count
  image_counts = ""
  image_scores = ""

  # For each label, check how many are recognized in the image
  for label in labels:

    # Complete image path
    image_path = "data/" + image

    # Use count_objects function
    output = count_objects(image_path, API_URL_OBJDET, API_TOKEN, label)

    # If the model finds the label, add it to the string
    if output > 0:
      image_counts += (str(output) + " " + label + "s, ")

  # Generate image classification data
  image_data = query(image_path, API_URL_IMGCLASS, API_TOKEN)
  
  for i in range(3):
    # String for image label
    image_label = str(image_data[i]['label'])

    # String for scores, converted to percentages
    image_score = str(round(image_data[i]['score'] * 100, 1))

    # Add scores to the list
    image_scores += ("[ " + image_label + ": " + image_score + "% ]\n")


  # ----- PRINT DATA -----
  print(f'----- {image} -----')
    
  # Print if no objects were detected
  if image_counts == "":
    print(f'No objects were detected in image {image}.')

  # Print if objects were detected
  else:
    print(f'There are {image_counts}in image {image}.')

  # Print Image classicifation data
  print(f'\nImage Classification scores:')
  print(f'{image_scores}\n\n')
  