import speech_recognition as sr


def get_device():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if 'USB PnP Audio' in name:
            return index

