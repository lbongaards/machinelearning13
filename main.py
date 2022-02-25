
# This is the python script for the image processing module.


"""
# Import python packages.

Often you need to import packages to do fancy works.
In this tutorial, the tool (Replit) takes care of the package installation for you.
But, in the future you may find yourself having the need to install packages.
In that situation, you can use a package manager, such as pip (https://github.com/pypa/pip).
"""
import json
import requests


"""
# Specify the API URL and token of the Hugging Face API.

In this tutorial, we are going to use the Hugging Face API.
API means the Application Programming Interface, which allows computer programs to talk to each other.
API_URL is the Hugging Face API URL that points to a model that we want to use.
For more information about the model, see the following page:
- https://huggingface.co/google/vit-base-patch16-224

API_TOKEN is the Hugging Face API token for authentication.
Please do not make the API token public.
For more information about how to use the API, see the following page:
- https://api-inference.huggingface.co/docs/python/html/quicktour.html
"""
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50" #"https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
#https://api-inference.huggingface.co/models/google/facebook/detr-resnet-50
API_TOKEN = "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"


# Below is a reusable function for interacting with the Hugging Face API.
def query(file_path, api_url, api_token):
    """
    Ask the Hugging Face API to run the model and return the result.

    Attributes
    ----------
    file_path : str
        The path to the image file that we want to send to the Hugging Face API.
    api_url : str
        The API URL that points to a specific machine learning model.
    api_token : str
        The API token for authentication.
    """
    # Construct the header of the HTTP request that includes the API token.
    headers = {"Authorization": f"Bearer " + api_token}
    # Read the input data.
    with open(file_path, "rb") as f:
        data = f.read()
    # Make a POST request to the API with the token and input data.
    response = requests.request("POST", api_url, headers=headers, data=data)
    # Return the output from the API
    return json.loads(response.content.decode("utf-8"))

# Below is another resuable function for counting the number of objects in an image
def count_objects(file_path, api_url, api_token, label):
    """
    Ask the Hugging Face API to run the model and count the number of objects.

    Usage example:
        data = count_objects("data/000000039769.jpeg", API_URL, API_TOKEN, "bicycle")

    Attributes
    ----------
    file_path : str
        The path to the image file that we want to send to the Hugging Face API.
    api_url : str
        The API URL that points to a specific machine learning model.
    api_token : str
        The API token for authentication.
    label : str
        The label of the object that we want to count (e.g., "bicycle").
    """
    data = query(file_path, API_URL, API_TOKEN)
    count = 0
    for d in data:
        if d["label"] == label:
            count += 1
    return count

"""
# Use the Hugging Face API to ask a model to make predictions.

Now we use the above "query" function to ask the API to predict what is in this image.
You can replace the my_image variable with your own images.
Note that my_image is a path that points to a file.
In this case, "data/000000039769.jpeg" is a relative path.
This means that "000000039769.jpeg" is placed in the "data" folder.
And the "data" folder is placed together with the main.py script in the same folder.
"""
image_to_count = 1
photo = '.jpeg'

for i in range(18):
  if image_to_count == 11:
    image_to_count = 1
    maps = 2
  if image_to_count == 7 and maps ==2:
    photo = '.jpeg'
  #Counted object is the object that the AI counts.
  counted_object = "car"
  #Image to count
  
  my_image = f'data/{counted_object}/{image_to_count}{photo}'
  output = count_objects(my_image, API_URL, API_TOKEN, counted_object)



  """
  # Print the output of the model returned by the API.

  The output looks like below:
      [{'score': 0.937, 'label': 'Egyptian cat'}, {'score': 0.038, 'label': 'tabby, tabby cat'}, {'score': 0.014, 'label': 'tiger cat'}, {'score': 0.003, 'label': 'lynx, catamount'}, {'score': 0.001, 'label': 'Siamese cat, Siamese'}]

  The output is an array of five dictionaries that represent the top 5 predictions from the model.
  Array and dictionary are both data structures.
  An array looks like [0, 1, 2, 3], which represents a list of elements (such as numbers).
  A dictionary looks like {"key1": "value1", "key2", "value2"}, which represents pairs of keys and values.
  In this case, the first element in the array {'score': 0.937, 'label': 'Egyptian cat'} is the first prediction.
  It means that the model thinks there are Egyptian cats in the image, with 0.937 probability (which is very high).
  """


  print(f'There are {output} {counted_object}s in picture {counted_object}.{image_to_count}')
  image_to_count = image_to_count + 1



# Wow wat gaaaaaaaaaaaaaaaaaaf