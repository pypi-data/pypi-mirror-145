import wave
import os
from formatConvert.wav_pcm import pcm2wav,wav2pcm,get_data_array
import  numpy as np
import math
from moviepy.editor import AudioFileClip



def get_wav_from_mp4(mp4file):
    """
    Parameters
    ----------
    mp4file

    Returns
    -------

    """
    suffix = os.path.splitext(mp4file)[-1]
    if suffix != '.mp4':
        raise TypeError('wrong format! not mp4 file!' + str(suffix))
    my_audio_clip = AudioFileClip(mp4file)
    newFileName = mp4file[:-4] + '.wav'
    my_audio_clip.write_audiofile(newFileName)
    return newFileName


def get_rms(records):
    '''
    Parameters
    ----------
    records

    Returns
    -------
    '''
    #return math.sqrt(sum([x * x for x in records])/len(records))
    data = records.astype(np.float32).tolist()
    rms = math.sqrt(sum([(x/32767) * (x/32767) for x in data])/len(data))
    dBrmsValue = 20*math.log10(rms + 1.0E-6)
    return dBrmsValue

def isSlience(Filename =None):
    """
    Parameters
    ----------
    Filename 支持 wav 和 pcm 和MP4

    Returns
    -------

    """
    suffix = os.path.splitext(Filename)[-1]
    if suffix == '.mp4':
        Filename = get_wav_from_mp4(Filename)
        ins, _,_ = get_data_array(Filename)
    if suffix == '.pcm':
        pcmf = open(Filename, 'rb')
        pcmdata = pcmf.read()
        ins = np.frombuffer(pcmdata, dtype=np.int16)
        pcmf.close()
    if suffix == '.wav':
        ins,_,_ = get_data_array(Filename)
    dBrmsValue = get_rms(ins)#20*math.log10(get_rms(ins)/32767+ 1.0E-6)
    print(dBrmsValue)
    if dBrmsValue > -70:
        return False
    else:
        for n in range(len(ins)//480):
            curdata = ins[480*n:480*(n+1)]
            dBrmsValue = get_rms(curdata)#20 * math.log10(get_rms(curdata) / 32767 + 1.0E-6)
            print(dBrmsValue)
            if dBrmsValue > -60:
                return False
        return True
    pass


def audioFormat(wavFileName=None):
    """
    wavFileName：输入文件 wav，mp4
    Returns
    -------
    refChannel:通道数
    refsamWidth：比特位 2代表16bit
    refsamplerate：采样率
    refframeCount：样点数
    """
    suffix = os.path.splitext(wavFileName)[-1]
    if suffix != '.wav' and suffix != '.mp4':
        raise TypeError('wrong format! not wav/mp4 file!' + str(suffix))
    if suffix == '.mp4':
        wavFileName = get_wav_from_mp4(wavFileName)
    wavf = wave.open(wavFileName, 'rb')
    refChannel,refsamWidth,refsamplerate,refframeCount = wavf.getnchannels(),wavf.getsampwidth(),wavf.getframerate(),wavf.getnframes()
    return refChannel,refsamWidth*8,refsamplerate,refframeCount




if __name__ == '__main__':
    ref = r'C:\Users\vcloud_avl\Documents\我的POPO\src.pcm'
    print(isSlience(ref))
    #print(audioFormat(ref))