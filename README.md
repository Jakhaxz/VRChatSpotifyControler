# VRChatSpotifyControler

Media controller for Spotify using VRChat OSC  
Supports now playing text using VRChat chatbox

## Usage

#### Now Playing Chatbox

To use just the now playing chatbox, you only need to run the program while Spotify and VRChat are open.  
To stop the now playing chatbox just close the program.

#### Media Controls

Adding the Media controls to your models allows you to control Spotify and also toggle the now playing chatbox, without closing the program.  

In Unity set your avatar up with avatar 3.0 parameters:

  pause-play : bool  
  next-track : bool  
  previous-track : bool  
  vol-slider : float  
  now-playing : bool  

The names of the parameters must match exactly.

![Avatar_Paramaters](https://user-images.githubusercontent.com/21070138/189288415-bca94324-bd49-4020-975e-eef277fbdb60.png)

Add 4 buttons and one radical puppet to your avatar 3.0 menu, and assign the paramaters as shown

![Avatar_Menu](https://user-images.githubusercontent.com/21070138/157578170-08f8be5e-4c48-43cb-8169-55da703bac62.png)
![Now_Playing](https://user-images.githubusercontent.com/21070138/189288499-d209634c-5183-403f-ba60-3fcff7904571.png)

Upload your avatar, then start VRChat

Download the latest executable from [releases](https://github.com/Jakhaxz/VRChatSpotifyControler/releases) and double click to run.

If all done correctly you can now control Spotify from your Avatar 3.0 menu

## Running from source

### Prerequisites
- Python3

## Getting Started

Download zip or clone repository
Open Command Prompt and navigate to the extracted directory
Install requirements
  ```bash
  py -m pip install -r requirements.txt
  ```
Run main.py
  ```bash
  py main.py
  ```

## Troubleshooting

### Stuck "Searching for an open Spotify.exe process..."

Make sure Spotify is open and if the message persists then play any song.
This should cause the SystemMediaTransportControlsSession to be created for Spotify, that the application is looking for.

### Volume control does not work

Volume control currently only works if the output device for Spotify is the default device.

Search for "Sound mixer options" in Windows start, find Spotify and make sure the Output is set to default. Spotify may need to be open and playing for it to show in the list.

![Spotify_Sound_Mixer_Options](https://user-images.githubusercontent.com/21070138/193977233-02f91a50-6e4a-4fe9-9b4c-84d13a9ca918.png)

