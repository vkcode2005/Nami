import os
import requests

# Function to configure and send the request
def ask_question(api_key, question):
    # Define the API endpoint URL (you would need to get the correct URL from Gemini's API docs)
    url = "https://api.gemini.com/v1/ask"  # Replace this with the actual Gemini API endpoint
    
    # Set up headers with your API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Set up the data payload (the question to ask)
    data = {
        "prompt": question,
        "model": "gemini-1"  # Example, change based on the model version you want to use
    }

    # Send the POST request to the API
    response = requests.post(url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and get the answer
        answer = response.json().get("answer")
        print(f"Answer: {answer}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    try:
        # Get the API key from environment or use the hardcoded one
        api_key = os.environ.get("API_KEY", "AIzaSyBxz2VE212GiJUJqyiiCtkxEoV8bAfsbG4")  # Replace with your key

        # Ask a question
        question = "What is the capital of France?"
        ask_question(api_key, question)
    
    except KeyError:
        print("Error: API key not found in environment variables.")

if __name__ == "__main__":
    main()
