# measure_wav_linux64.py
# Paul Boersma 2017-01-25
#
# A sample script that uses the Vokaturi library to extract the emotions from
# a wav file on disk. The file has to contain a mono recording.
#
# Call syntax:
#   python3 measure_wav_linux64.py path_to_sound_file.wav

import sys
import scipy.io.wavfile
#import scipy
sys.path.append("../api")
import Vokaturi


def analyze(file_name):
    
#   print ("Loading library...")
    Vokaturi.load("../lib/Vokaturi_linux64.so")
#   print ("Analyzed by: %s" % Vokaturi.versionAndLicense())

#   print ("Reading sound file...")
    (sample_rate, samples) = scipy.io.wavfile.read(file_name)
#   print ("   sample rate %.3f Hz" % sample_rate)

#   print ("Allocating Vokaturi sample array...")
    buffer_length = len(samples)

#   print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
    c_buffer = Vokaturi.SampleArrayC(buffer_length)

    if samples.ndim == 1:  # mono
            c_buffer[:] = samples[:] / 32768.0
    else:  # stereo
            c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

#   print ("Creating VokaturiVoice...")
    voice = Vokaturi.Voice (sample_rate, buffer_length)

#   print ("Filling VokaturiVoice with samples...")
    voice.fill(buffer_length, c_buffer)

#   print ("Extracting emotions from VokaturiVoice...")
    quality = Vokaturi.Quality()
    emotionProbabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotionProbabilities)

    enabled = True
    if quality.valid:
#          print ("Neutral: %.3f" % emotionProbabilities.neutrality)
#          print ("Happy: %.3f" % emotionProbabilities.happiness)
#          print ("Sad: %.3f" % emotionProbabilities.sadness)
#          print ("Angry: %.3f" % emotionProbabilities.anger)
#          print ("Fear: %.3f" % emotionProbabilities.fear)
	   value = emotionProbabilities.anger
    else:
           value = 0
           enabled = False

    voice.destroy()
    return enabled, value 

