import pyaudio, wave, pygame,time
import numpy as np
import scipy.io as sio
from wavtorgb import *
from math import *
import matplotlib.pyplot as plt
import soundfile as sf



#Request for the file name of the WAV file.

#Starts Pygame and opens the screen 
pygame.init()
screen = pygame.display.set_mode((200, 200))

chunk = 2048
# open the WAV file
wf = wave.open('test-3A.wav','rb')

swidth = wf.getsampwidth()
SW=print('swidth:',swidth)
#sampling frequency
RATE = wf.getframerate()
Sm=print('RATE:',RATE)
# use a Blackman window
window = np.blackman(chunk)
print(window)
# open the stream
p = pyaudio.PyAudio()
background = pygame.Surface(screen.get_size())
print('background:',background)
background = background.convert()
print('background 1:',background)
thefreq = 1.0

stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)
s=p.get_format_from_width(wf.getsampwidth())
print(s)
q=wf.getnchannels()
print('channels:',q)
# read the incoming data
data = wf.readframes(chunk)
print('data:',data)
len1=len(data)
print('1en1:',len1)
len2=chunk*swidth
print('len2:',len2)
# play stream and find the frequency of each chunk
while len(data) == chunk*swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        thefreq = which*RATE/chunk
        print ("the previous freq is "+str(thefreq))
        while thefreq < 350 and thefreq > 15:
            
            thefreq = thefreq*2
            print ("the new freq is "+str(thefreq))
        while thefreq > 700:
            
            thefreq = thefreq/2
            print ("the new freq is"+str(thefreq))
        c = 3*10**8
        THz = thefreq*2**40
        pre = float(c)/float(THz)
        nm = int(pre*10**(-floor(log10(pre)))*100)
        print ("Your nm total: "+str(nm))
        rgb = wavelen2rgb(nm, MaxIntensity=255)
        print ("the colors for this nm are: "+str(rgb))
  #Fills the background with the appropriate colot, does this so fast, it creates a "fading effect" in between colors
        background.fill((rgb[0],rgb[1],rgb[2]))
  #"blits" (renders) the color to the background
        screen.blit(background, (0, 0))
  #and finally displays the background
        pygame.display.flip()
	
	
	
    # read some more data
    data = wf.readframes(chunk)
    time.sleep(0.5)
if data:
    stream.write(data)
stream.close()
p.terminate()
