from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import os
import time

# Here is one number you can adjust!
# I played around with the threshold sound -- which from what I recall is the minimum amount of sound from your mic that counts as it being used.
THRESHOLD = 300
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100 


def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r


def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False
    t_time = 0

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)
        t_time += 1

        silent = is_silent(snd_data)

        if not silent and not snd_started:
            snd_started = True
        elif silent and snd_started:
            num_silent += 1
        # Below this line is another number you can adjust!
        # It describes how long is a given audio sample you will use to detect silence
        # If you make these too small then it will be much more likely to detect silence
        # If you make these two big then you are much less likely to detect a silence
        if t_time > 200:
            num_silent = 0
            t_time = 0
        # This is the last number you can adjust!
        # this last number determines what proportion of the time sample has to be silent for silence to be detected.
        # If it's too small, silence is detected more often
        # If it's too big, then you would have to be silent for a while for silence to be detected.
        if snd_started and num_silent > 90:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def play(path):
    wf = wave.open(path, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK_SIZE)
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK_SIZE)
    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    for i in range(30):
        # play the boop!
        os.system('afplay /System/Library/Sounds/tink.aiff >/dev/null 2>&1 &')
        print("please speak a word into the microphone")
        time.sleep(.200)
        record_to_file('demo.wav')
        print("done - result written to demo.wav")
        play('demo.wav')
        print(i)
