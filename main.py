import re
import os
import wave
import numpy as np
import sounddevice as sd
import pyttsx3
import webbrowser
import pywhatkit as kit
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import faster_whisper  # For offline speech recognition
import time  # For timing transcription
import requests  # For weather API
from googleapiclient.discovery import build
import subprocess
from fuzzywuzzy import process
import json
import sys
import struct

# Initialize text-to-speech engine (optimize for speed if needed)
engine = pyttsx3.init()  # You can tweak voice rate: engine.setProperty('rate', 150)

# API Credentials
GOOGLE_API_KEY = ""
GOOGLE_CSE_ID = ""
OPENWEATHERMAP_API_KEY = ""  # Replace with your OpenWeatherMap API key

# Spotify Credentials
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Contacts dictionary
CONTACTS = {
    "nilesh": "+91(Your Number with country code)",
    "neil": "+91(Your Number with country code)",
    "niles": "+91(Your Number with country code)",
    "nielsen": "+91(Your Number with country code)",
    "mani": "+91(Your Number with country code)",
    "money": "+91(Your Number with country code)",
    "many": "+91(Your Number with country code)",
    "dad": "+91(Your Number with country code)",
    "john": "+91(Your Number with country code)"
}

name_mapping = {
    "nilish": "nilesh",
    "neilish": "nilesh",
    "nelish": "nilesh",
    "niles": "nilesh",
    "neal": "nilesh",
    "neil": "nilesh",
    "knee leash": "nilesh",
    "kneel ish": "nilesh",
    "knee lish": "nilesh",
    "niley": "nilesh",
    "nylish": "nilesh",
    "money": "mani",
    "many": "mani",
    "munny": "mani",
    "maani": "mani",
    "moni": "mani",
    "monee": "mani",
}

def find_closest_contact(name):
    name = name.lower().strip()
    print(f"Searching for closest match to: '{name}'")
    if name in CONTACTS:
        return name
    
    all_names = list(CONTACTS.keys()) + list(set(name_mapping.values()))
    best_match, score = process.extractOne(name, all_names)
    
    if score >= 80:
        print(f"Matched '{name}' to '{best_match}' with score {score}")
        return name_mapping.get(best_match, best_match)
    else:
        print(f"No close match found for '{name}' (best: '{best_match}', score: {score})")
        return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

LAST_DEVICE_ID = None

def transfer_playback_to_active_device():
    global LAST_DEVICE_ID
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                       client_secret=SPOTIFY_CLIENT_SECRET,
                                                       redirect_uri=SPOTIFY_REDIRECT_URI,
                                                       scope="user-modify-playback-state,user-read-playback-state"))
        devices = sp.devices()
        if devices["devices"]:
            device_id = devices["devices"][0]["id"]
            if LAST_DEVICE_ID != device_id:
                sp.transfer_playback(device_id=device_id, force_play=True)
                LAST_DEVICE_ID = device_id
            return device_id
        else:
            speak("No active Spotify device found. Please open Spotify.")
            return None
    except Exception as e:
        print(f"Error transferring playback: {e}")
        return None

def play_spotify_song(song_name):
    try:
        device_id = transfer_playback_to_active_device()
        if not device_id:
            return
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                       client_secret=SPOTIFY_CLIENT_SECRET,
                                                       redirect_uri=SPOTIFY_REDIRECT_URI,
                                                       scope="user-modify-playback-state,user-read-playback-state"))
        results = sp.search(q=f"track:{song_name}", limit=1, type="track", market="IN")
        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            track_uri = track["uri"]
            speak(f"Playing {track_name} by {artist_name} on Spotify.")
            sp.start_playback(device_id=device_id, uris=[track_uri])
        else:
            speak("Sorry, I couldn’t find that song on Spotify.")
    except Exception as e:
        speak("Sorry, I encountered an error while trying to play the song.")
        print(f"Error: {e}")

def get_confirmation():
    filename = record_audio(duration=3)
    if filename:
        text = transcribe_audio_offline(filename)
        if text and ("yes" in text.lower() or "yeah" in text.lower() or "correct" in text.lower() or "yep" in text.lower()):
            return True
    return False

def send_whatsapp_message(recipient, message):
    recipient = recipient.lower().strip()
    print(f"Processing recipient: '{recipient}'")
    matched_contact = find_closest_contact(recipient)
    if matched_contact:
        recipient_number = CONTACTS[matched_contact]
        try:
            if matched_contact != recipient:
                speak(f"Did you mean {matched_contact}? Please say yes or no.")
                confirmation = get_confirmation()
                if not confirmation:
                    speak("Message canceled. Please try again.")
                    return
            kit.sendwhatmsg_instantly(recipient_number, message)
            speak(f"Message sent successfully to {matched_contact}!")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            speak("I couldn’t send the message.")
    else:
        speak(f"I couldn’t find a close match for {recipient} in your contacts.")

def open_whatsapp():
    try:
        print("Attempting to open WhatsApp Desktop via shell URI...")
        subprocess.run(['start', 'shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App'], shell=True, check=True)
        speak("Opening WhatsApp Desktop.")
        return
    except subprocess.CalledProcessError as e:
        print(f"Shell URI failed: {e}")
    
    try:
        print("Attempting to open WhatsApp Desktop via executable...")
        whatsapp_path = os.path.expanduser("~\\AppData\\Local\\WhatsApp\\WhatsApp.exe")
        if os.path.exists(whatsapp_path):
            subprocess.run([whatsapp_path], check=True)
            speak("Opening WhatsApp Desktop.")
            return
        else:
            print("WhatsApp executable not found at default path.")
    except subprocess.CalledProcessError as e:
        print(f"Executable launch failed: {e}")

    print("Falling back to WhatsApp Web.")
    webbrowser.open("https://web.whatsapp.com")
    speak("Opening WhatsApp Web.")

def transcribe_audio_offline(filename):
    # Use a smaller, faster model ('tiny' instead of 'large') for quicker transcription
    model = faster_whisper.WhisperModel("tiny", device="cpu", compute_type="int8", num_workers=2)
    try:
        # Read the WAV file efficiently
        start_time = time.time()  # Define start_time here
        with wave.open(filename, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                raise ValueError("Audio file must be WAV format, mono, PCM, 16kHz")
            audio_data = wf.readframes(wf.getnframes())
            audio = np.frombuffer(audio_data, np.int16).flatten().astype(np.float32) / 32768.0

        # Transcribe with optimized parameters for speed
        segments, _ = model.transcribe(audio, language="en", beam_size=1, vad_filter=True)
        text = " ".join(segment.text for segment in segments).strip()
        print(f"Transcribed text: '{text}' (Time: {time.time() - start_time:.2f}s)")  # Optional timing for debugging
        return text
    except Exception as e:
        print(f"Speech recognition error with faster-whisper: {e}")
        return None

def google_search(query):
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        result = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=1).execute()
        if "items" in result:
            top_result = result["items"][0]
            return f"Here's what I found: {top_result['snippet']}"
        else:
            return "I couldn’t find an answer to that."
    except Exception as e:
        print(f"Error with Google Search: {e}")
        return "Sorry, I couldn’t search for that right now."

def record_audio(filename="input.wav", duration=3, rate=16000, channels=1):  # Reduced duration for faster response
    try:
        print("Recording...")
        audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=channels, dtype=np.int16)
        sd.wait()
        print("Recording Finished.")
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            wf.writeframes(audio_data.tobytes())
        return filename
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

def get_weather(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Use "imperial" for Fahrenheit if preferred
        "lang": "en"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()

        if data["cod"] != 200:
            speak(f"Sorry, I couldn’t find weather data for {location}.")
            return

        temperature = data["main"]["temp"]
        weather_condition = data["weather"][0]["description"]
        city = data["name"]
        country = data.get("sys", {}).get("country", "Unknown")

        weather_message = f"The current weather in {city}, {country} is {weather_condition} with a temperature of {temperature}°C."
        speak(weather_message)
        print(weather_message)
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        speak("Sorry, I couldn’t retrieve the weather information right now.")

def process_command(command):
    command = command.lower()
    print(f"Processing command: '{command}'")

    if "open whatsapp" in command or "launch whatsapp" in command:
        print("Matched 'open whatsapp' command")
        open_whatsapp()
        return

    if "whatsapp" in command or "text" in command or "message" in command:
        try:
            patterns = [
                r".*(?:whatsapp|send a whatsapp|text|message) (?:to|for) ([\w\s]+)[.:,]? (.+)",
                r".*(?:whatsapp|send a whatsapp|text|message) ([\w\s]+)[.:,]? (.+)",
                r".*(?:tell|ask) ([\w\s]+) (?:that|to|about) (.+)",
                r".*(?:message to|on whatsapp) ([\w\s]+)[.:,]? (.+)"
            ]
            match = None
            for pattern in patterns:
                match = re.match(pattern, command, re.IGNORECASE)
                if match:
                    break
            if match:
                contact_name = match.group(1).strip().lower()
                message = match.group(2).strip()
                print(f"Extracted contact: '{contact_name}', message: '{message}'")
                send_whatsapp_message(contact_name, message)
            else:
                print("No messaging pattern matched")
                speak("Please say something like 'Send a message to John saying hello' or 'WhatsApp John: Hello!'")
        except Exception as e:
            print(f"Error processing WhatsApp command: {e}")
            speak("I couldn’t process the WhatsApp command.")

    elif "google" in command and "open" not in command:
        query = command.replace("google", "").strip()
        response = google_search(query)
        speak(response)
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "play" in command:
        song_name = command.replace("play", "").strip()
        play_spotify_song(song_name)
    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("calc")
    elif "open camera" in command:
        speak("Opening Camera")
        os.system("start microsoft.windows.camera:")
    elif "spotify" in command:
        speak("Opening Spotify")
        os.system("start spotify")
    elif "pause" in command:
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET,
                                                           redirect_uri=SPOTIFY_REDIRECT_URI,
                                                           scope="user-modify-playback-state,user-read-playback-state"))
            sp.pause_playback()
            speak("Playback paused.")
        except Exception as e:
            print(f"Error: {e}")
            speak("I couldn’t pause playback.")
    elif "resume" in command:
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET,
                                                           redirect_uri=SPOTIFY_REDIRECT_URI,
                                                           scope="user-modify-playback-state,user-read-playback-state"))
            sp.start_playback()
            speak("Resuming playback.")
        except Exception as e:
            print(f"Error: {e}")
            speak("I couldn’t resume playback.")
    elif "stop" in command:
        speak("Goodbye!")
        exit()
    elif "what's the weather" in command or "weather" in command:
        # Extract location from the command (e.g., "what's the weather in New York")
        match = re.search(r"in\s+([\w\s]+)", command)
        if match:
            location = match.group(1).strip()
            get_weather(location)
        else:
            speak("Please specify a location, like 'What’s the weather in New York'.")
    else:
        response = google_search(command)
        speak(response)

def native_messaging_main():
    while True:
        # Read message length
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            sys.exit(0)
        message_length = struct.unpack('@I', raw_length)[0]
        # Read message
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        command = json.loads(message)["command"]
        print(f"Received command: {command}", file=sys.stderr)
        process_command(command)
        # Send response (optional)
        response = {"status": "processed"}
        sys.stdout.buffer.write(struct.pack('@I', len(json.dumps(response))))
        sys.stdout.buffer.write(json.dumps(response).encode('utf-8'))
        sys.stdout.buffer.flush()

def main():
    speak("Listening... Say 'Friday' to activate.")
    while True:
        recorded_file = record_audio()
        if recorded_file:
            command = transcribe_audio_offline(recorded_file)
            if command and "friday" in command.lower():
                speak("Yes, I am listening...")
                recorded_file = record_audio()
                if recorded_file:
                    command = transcribe_audio_offline(recorded_file)
                    print(f"Transcribed command: '{command}'")
                    if command:
                        process_command(command)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--native":
        native_messaging_main()
    else:
        main()