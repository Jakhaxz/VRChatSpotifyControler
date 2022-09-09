from os import system
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
from win32api import keybd_event
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CoInitialize, CoUninitialize
import winsdk.windows.media.control as wmc
import asyncio

def splash():
    asci = """
  _    ______  ________          __  _____             __  _ ____      ______            __             __         
 | |  / / __ \/ ____/ /_  ____ _/ /_/ ___/____  ____  / /_(_) __/_  __/ ____/___  ____  / /__________  / /__  _____
 | | / / /_/ / /   / __ \/ __ `/ __/\__ \/ __ \/ __ \/ __/ / /_/ / / / /   / __ \/ __ \/ __/ ___/ __ \/ / _ \/ ___/
 | |/ / _, _/ /___/ / / / /_/ / /_ ___/ / /_/ / /_/ / /_/ / __/ /_/ / /___/ /_/ / / / / /_/ /  / /_/ / /  __/ /    
 |___/_/ |_|\____/_/ /_/\__,_/\__//____/ .___/\____/\__/_/_/  \__, /\____/\____/_/ /_/\__/_/   \____/_/\___/_/     
                                      /_/                    /____/                                                
                                                                                                      by Jakhaxz
                                                                                                      """
    print(asci)

chatboxState = 1

######## GET SPOTIFY NOW PLAYING ########

async def get_media_info():
    sessions = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()

    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.

    global current_session
    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        if current_session.source_app_user_model_id == 'Spotify.exe':
            info = await current_session.try_get_media_properties_async()

            # song_attr[0] != '_' ignores system attributes
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            # converts winrt vector to list
            info_dict['genres'] = list(info_dict['genres'])

            return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    raise Exception('TARGET_PROGRAM is not the current media session')

def mediaIs(state):
    if current_session == None:
        return False
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == current_session.get_playback_info().playback_status #get media state enum and compare to current main media session state

######## MEDIA CONTROLS START ########

def pauseTrack(unused_addr, arg):
    if arg:
        keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0) #Play/Pause
        print("Detected Play/Pause")

def nextTrack(unused_addr, arg):
    if arg:
        keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0) #Next Track
        print("Detected Next Track")

def previousTrack(unused_addr, arg):
    if arg:
        keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0) #Previous Track
        print("Detected Previous")

def volSlider(unused_addr, arg):
    CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("Spotify volume: %s" % str(round(volume.GetMasterVolume(), 2)))
            volume.SetMasterVolume(arg, None)
    CoUninitialize()

def chatBox(unused_addr, arg):
    global chatboxState
    if arg == 0:
        chatboxState = 0
        clearChat()
        print("Now Playing Disabled")
    else:
        chatboxState = 1
        print("Now Playing Enabled")


######## MEDIA CONTROLS END ########

def clear():
    system('cls')

def filter_handler(address, *args):
    print(f"{address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/avatar/parameters/pause-play", pauseTrack)
dispatcher.map("/avatar/parameters/next-track", nextTrack)
dispatcher.map("/avatar/parameters/previous-track", previousTrack)
dispatcher.map("/avatar/parameters/vol-slider", volSlider)
dispatcher.map("/avatar/parameters/now-playing", chatBox)

serverip = "127.0.0.1"
serverport = 9001

def sendChat(nowPlaying):
    client.send_message("/chatbox/input", ['[Spotify] ~ ' + nowPlaying, True])

def clearChat():
    client.send_message("/chatbox/input", ['', True])

async def loop():
    global current_media_info
    while True:
        if chatboxState == 1:
            if mediaIs("PLAYING") == True:
                current_media_info = await get_media_info()
                title = current_media_info.get('title')
                artist = current_media_info.get('artist')
                nowPlaying = "%s - %s" % (title, artist)

                clear()
                splash()
                print("Now Playing: %s" % (nowPlaying))
                sendChat(nowPlaying)
                await asyncio.sleep(2)
            else:
                clear()
                splash()
                print("Nothing is playing")
                clearChat()
                await asyncio.sleep(2)
        else:
            await asyncio.sleep(2)


async def init_main():
    global client
    global current_media_info
    server = AsyncIOOSCUDPServer((serverip, serverport), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    clientip = "127.0.0.1"
    clientport = 9000

    client = SimpleUDPClient(clientip, clientport)

    current_media_info = await get_media_info()

    splash()

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint

asyncio.run(init_main())
