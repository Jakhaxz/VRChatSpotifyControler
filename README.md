# VRChatMediaControls

Media controller for Spotify using VRChat OSC

## Usage

In Unity set your avatar up with avatar 3.0 parameters:

  pause-play : bool
  next-track : bool
  previous-track : bool
  vol-slider : float

The names of the parameters must match exactly.

![Avatar_Paramaters](https://user-images.githubusercontent.com/21070138/157577856-77a88efb-c6fd-4dec-b2e2-784223fb4f37.png)

Add 3 buttons and one radical puppet to your avatar 3.0 menu, and assign the paramaters as shown

![Avatar_Menu](https://user-images.githubusercontent.com/21070138/157578170-08f8be5e-4c48-43cb-8169-55da703bac62.png)

Upload your avatar, then start VRChat

Download the latest executable from [releases](https://github.com/Jakhaxz/VRChatMediaControls/releases) and double click to run.

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
