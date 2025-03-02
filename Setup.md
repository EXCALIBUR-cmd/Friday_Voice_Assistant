Note : Please go through the README file for an overview of requirements.
To run "Friday" on your system, here is a series of steps you need to follow:
1-> Set up a virtual environment
    On Windows: python -m venv venv
                venv\Scripts\activate    (run these commands in your terminal separately)
                
  On macOS/Linux: python3 -m venv venv
source venv/bin/activate

2-> Install Dependencies through this command: pip install -r requirements.txt
3-> Download the faster-whisper model (for offline speech recognition): 
    => Run the included download_model.py: python download_model.py (run this command in your terminal)
    Note: The model will be saved to ~/.cache/faster_whisper (macOS/Linux) or %AppData%\faster_whisper (Windows). This requires an internet connection.

4-> Now as to use "Friday's" features, we need to have some API's for yourself:
    => A Spotify API for controlling music features:
    Purpose: Access Spotify’s music library to play songs via voice commands (e.g., "Friday, play a song").
Steps:
Sign Up/Log In:
Go to developer.spotify.com and sign in or create a Spotify account.
Create a Developer Account:
If prompted, agree to the Developer Terms of Service and create a developer account (free).
Create an App:
Navigate to the Spotify Dashboard.
Click “Create an App” or “Create a Client ID.”
Name your app (e.g., “Friday Voice Assistant”) and click “Create.”
Get Credentials:
Copy the Client ID and Client Secret from your app’s dashboard.
Set a Redirect URI (e.g., http://localhost:8888/callback) for authentication, and add it under “Redirect URIs.”
API Usage:
Use these credentials in friday.py (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI) for OAuth with spotipy.
Free Plan Limits:
Free tier allows up to 1,000,000 API calls/day, but requires user authentication for playback (users need a Spotify account).
Upgrade to a Premium plan for higher limits or additional features if needed.

   => Google Custom Search API (for Web Searching):
      Purpose: Search the web via voice commands (e.g., "Friday, Google something").
Steps:
Sign Up/Log In:
Go to console.cloud.google.com and sign in or create a Google Cloud account.
Create a Project:
Click “Select a project” > “New Project,” name it (e.g., “Friday Search”), and create it.
Enable the Custom Search API:
In the Google Cloud Console, navigate to “APIs & Services” > “Library.”
Search for “Custom Search API,” select it, and click “Enable.”
Create a Custom Search Engine:
Go to cse.google.com, sign in, and click “Add” to create a new Custom Search Engine.
Name it (e.g., “Friday Search”), set the search scope (e.g., entire web), and create.
Note the “Search Engine ID” (e.g., c16ff0d6a7f624a8d in your script).
Get an API Key:
In the Google Cloud Console, go to “APIs & Services” > “Credentials.”
Click “Create Credentials” > “API Key,” and copy the key (e.g., AIzaSyBRgK2HyLK0fpyqEwD3ANeQrpr2a8IvwHM).
API Usage:
Use the API key (GOOGLE_API_KEY) and Search Engine ID (GOOGLE_CSE_ID) in friday.py for Google searches.
Free Plan Limits:
Free tier provides 100 queries/day. Upgrade to a paid plan for higher limits (e.g., $5/1,000 queries).

  => OpenWeatherMap API (for Weather Updates)
     Purpose: Provide current weather data via voice commands (e.g., "Friday, what’s the weather in New York").
Steps:
Sign Up/Log In:
Go to openweathermap.org and sign up for a free account using your email.
Verify Your Email:
Check your inbox for a verification email and confirm your account. You can resend it after 1 hour if needed.
Get Your API Key:
After verification, check your inbox for a welcome email containing your API key (APPID).
Alternatively, log in, go to your account page, and find or generate your API key under “API Keys.”
API Usage:
Use the API key (OPENWEATHERMAP_API_KEY) in friday.py for weather queries.
Free Plan Limits:
Free tier allows 60 calls/minute. Upgrade to paid plans (e.g., One Call by Call for 1,000 calls/day) for higher limits or additional data (e.g., historical weather).

Example Integration in friday.py:
# At the top of friday.py or main.py
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "your_spotify_client_id")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "your_spotify_client_secret")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "your_google_api_key")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "your_google_cse_id")
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "your_openweathermap_api_key")

=> Running Friday: python friday.py or python main.py
=> To avoid activating your virtual environment everytime, create a file in notepad with the name "setup.bat" and save this file into your project directory, with these contents: 
@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Setup complete. Run "python friday.py" to start Friday.
pause
To run this file run this command in your powershell or terminal: 
use the cd command to navigate to the directory containing setup.bat (e.g., FridayProject/): cd C:\path\to\FridayProject(cmd) or cd "C:\path\to\FridayProject"(powershell)
once inside the directory run: setup.bat(cmd) or .\setup.bat(powershell)



=> For mac or linux users create the file as told above and save it as "setup.sh" into your project directory, with the following contents:
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete. Run 'python3 friday.py' to start Friday."
to run this file in the terminal  use this command: chmod +x setup.sh
