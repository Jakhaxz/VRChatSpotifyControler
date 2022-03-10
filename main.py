from argparse import ArgumentParser
from pythonosc import dispatcher, osc_server
from win32api import keybd_event
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CoInitialize, CoUninitialize

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

######## MEDIA CONTROLS END ########

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=9001, help="The port to listen on")
    sargs = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/avatar/parameters/pause-play", pauseTrack)
    dispatcher.map("/avatar/parameters/next-track", nextTrack)
    dispatcher.map("/avatar/parameters/previous-track", previousTrack)
    dispatcher.map("/avatar/parameters/vol-slider", volSlider)

    server = osc_server.ThreadingOSCUDPServer(
        (sargs.ip, sargs.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()