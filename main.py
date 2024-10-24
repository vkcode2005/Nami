import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import cohere

# Global recognizer initialization
r = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "api key"
cohere_api_key = "api key "  # Cohere API key

# Speech synthesis with Google Text-to-Speech (gTTS)
def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')   

        # Initialize the Pygame mixer
        pygame.mixer.init()

        # Load the MP3 file
        pygame.mixer.music.load("temp.mp3")

        # Play the MP3 file
        pygame.mixer.music.play()

        # Keep the program running so the music can play fully
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Stop the mixer and remove the temp file
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print(f"Error in speaking: {e}")

# Function to send a question to Cohere API
def ask_question(api_key, question):
    try:
        # Initialize the Cohere client
        co = cohere.Client(api_key)
        
        # Send the question to the Cohere generate model
        response = co.generate(
            model="command-r-plus",
            prompt=question,
            max_tokens=100,  # Customize max tokens as per your need
            temperature=0.7   # Customize temperature for randomness
        )
        
        # Return the model's response
        return response.generations[0].text.strip()  # Access the response correctly
    except Exception as e:
        print(f"Error in asking Cohere: {e}")
        return "I couldn't get a response from Cohere."

# Process user commands
def processcommand(c):
    global r  # Tell Python to use the global variable `r`
    command = c.lower().strip()
    print(f"Command received: '{command}'")
    
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]  # Assumes the song name is the second word
        link = musicLibrary.music.get(song)  # Use .get to avoid KeyError
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the music library.")
    elif "news" in command:
        try:
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                if articles:
                    for article in articles:
                        speak(article['title'])
                else:
                    speak("No news articles found.")
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            speak(f"Error fetching news: {e}")
    elif "ok" in command:
        speak("What would you like to ask?")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
                question = r.recognize_google(audio).lower()
                cohere_response = ask_question(cohere_api_key, question)
                speak("Cohere says: " + cohere_response)
            except sr.UnknownValueError:
                speak("Sorry, I could not understand your question.")
            except sr.RequestError as e:
                speak(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                speak(f"An error occurred: {e}")
    else:
        speak("Command not recognized.")

# Main loop for the voice assistant
if __name__ == "__main__":
    speak("Initializing Nami...")
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
                print("Recognizing...")
                
                # Recognize speech using Google Web Speech API
                command = r.recognize_google(audio).lower()
                print(f"You said: {command}")
                
                if command.lower() == "nami":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        audio = r.listen(source, timeout=15, phrase_time_limit=10)
                        command = r.recognize_google(audio).lower()
                        processcommand(command)

            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                speak(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                speak(f"An error occurred: {e}")
