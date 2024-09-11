# Import necessary libraries
from openai import OpenAI
from config import api_key
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from lazypredict.Supervised import LazyClassifier 

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

# Load the dataset into a pandas DataFrame
data = pd.read_csv("/path/to/your/file/.csv")  # Replace with the actual path to your CSV file

def get_embedding(text):
    """
    Function to generate embeddings for a given text using OpenAI's 'text-embedding-ada-002' model.
    
    Args:
    text (str): The text for which the embedding is to be generated.
    
    Returns:
    list: A list containing the embedding for the input text.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"  # Use OpenAI's ada model for text embeddings
    )
    return response.data[0].embedding  # Return the embedding for the input text

# Generate embeddings for all texts in the 'Text' column of the data
embeddings = np.array([get_embedding(text) for text in list(data['Text'])])

# Save the embeddings to a file for future use
np.save("text_embeddings.npy", embeddings)

# Load previously saved embeddings from the file (if needed)
embeddings = np.load("text_embeddings.npy")

# Extract target labels from the DataFrame
labels = np.array(data['Target'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)

# Initialize the LazyClassifier
clf = LazyClassifier(verbose=0,  # Suppresses detailed output during fitting
                     ignore_warnings=True,  # Ignores warnings related to classifiers
                     custom_metric=None)  # No custom metric is defined, so default metrics are used

# Fit the LazyClassifier on the training data and generate predictions for the test set
models, predictions = clf.fit(X_train, X_test, y_train, y_test)

# Print out the model performance metrics
print(models)
