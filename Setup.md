🚀 Get Friday Up and Running on Your System!
Before diving into Friday’s features, please go through the README file for an overview of the requirements. Now, let's get started!
🔹 Step 1: Set Up a Virtual Environment
A virtual environment helps keep dependencies isolated and prevents conflicts.

📌 For Windows:
=>python -m venv venv  
=>venv\Scripts\activate  (Run these commands separately in your terminal.)

📌 For macOS/Linux:
=>python3 -m venv venv  
=>source venv/bin/activate  

🔹 Step 2: Install Dependencies
Once the virtual environment is active, install all required dependencies with:
=>pip install -r requirements.txt  

🔹 Step 3: Download the Faster-Whisper Model
Friday relies on faster-whisper for offline speech recognition. To download the model, run:
=>python download_model.py  
📍 Where does the model get stored?

=>Windows: %AppData%\faster_whisper
=>macOS/Linux: ~/.cache/faster_whisper (Requires an internet connection for the first-time setup.)

🔹 Step 4: Set Up API Keys
To unlock Friday’s full potential, you need API keys for various services. Here's how to get them:

🎵 Spotify API (For Music Control)
=>Purpose: Play music with voice commands (e.g., "Friday, play a song.")
=>Setup:
->Go to Spotify Developer and log in or sign up.
->Create a Developer Account and agree to the terms.
->Click “Create an App” → Name it (e.g., "Friday Voice Assistant").
->Copy the Client ID & Client Secret from the dashboard.
->Set a Redirect URI (e.g., http://localhost:8888/callback).

🔍 Google Custom Search API (For Web Searching)
=>Purpose: Allows Friday to search the web (e.g., "Friday, Google something.")
=>Setup:
->Go to Google Cloud Console and log in.
->Create a New Project (e.g., "Friday Search") and enable Custom Search API.
->Set up a Custom Search Engine (here) and copy the Search Engine ID.
->Generate an API Key in the Credentials section.

☁️ OpenWeatherMap API (For Weather Updates)
=>Purpose: Fetches real-time weather data (e.g., "Friday, what’s the weather in New York?")
=>Setup:
->Sign up at OpenWeatherMap and verify your email.
->Copy the API Key from your account page.
(Consider the json.example file for relevance)

🔹 Step 5: Running Friday!
=>Once everything is set, launch Friday with:
 ->python friday.py  
 ->python main.py  

🔹 Bonus: Automate the Setup with a Script!
Want to avoid activating the virtual environment manually each time? Create a setup script!

📌 For Windows – Create a file called setup.bat in your project directory:
 => @echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Setup complete. Run "python friday.py" to start Friday.
pause
=> 📍 How to Run?
-> Navigate to your project folder:
cd C:\path\to\FridayProject  # (For CMD)  
cd "C:\path\to\FridayProject"  # (For PowerShell)  
=>Run:
setup.bat  # (For CMD)  
.\setup.bat  # (For PowerShell)  

=>📌 For macOS/Linux – Create a file called setup.sh in your project directory:
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete. Run 'python3 friday.py' to start Friday."

=>📍 How to Run?
->First, make the script executable:
chmod +x setup.sh  

Then run:
./setup.sh  

🎉 Congratulations! 🎉
You’re all set to experience Friday—your smart, voice-controlled assistant! 🚀

💡 Explore, tweak, and improve Friday! If you have any questions or feature requests, feel free to connect. Let’s push the boundaries of AI together! 💡

#Python #AI #VoiceAssistant #Automation #Friday #TechInnovation





