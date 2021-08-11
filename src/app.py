import speech_recognition as sr
import moviepy.editor as mp
import os, glob, shutil
from os import path
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

#configuratiton parameters
VIDEO_EXTENSION = 'mp4'
MP3_EXTENSION = 'mp3'
WAV_EXTENSION = 'wav'
TXT_EXTENSION = "txt"
SOURCE_LANGUAGE = "PT-BR"
AUDIO_BASE_PATH = "./audios"
TEXT_BASE_PATH = "./texts"
DIRETORIO_CHUNKS = "./audios/audio-chunks"


def get_file_name(path):
    return os.path.basename(path)

def extract_audio_from_video(video_file):
    print("Extraindo audio do video")
    my_clip = mp.VideoFileClip(video_file)
    my_clip.audio.write_audiofile(
        os.path.join(AUDIO_BASE_PATH, 
                     get_file_name(video_file)
                     .replace(VIDEO_EXTENSION, MP3_EXTENSION)))
    
    print("Extração concluida")
    
def convert_mp3_to_wave(audio_file_path):
    print("Convertendo de mp3 para wav")
    sound = AudioSegment.from_mp3(audio_file_path)
    sound.export(audio_file_path.replace(MP3_EXTENSION, WAV_EXTENSION), format="wav")
    print("Conversão concluida")
 
def extract_text_from_audio_chunks(wav_file):
    print("Preparando audio para transcrição: " + wav_file)
    print("Esse processo pode demorar um pouco. Aguarde...")
   
    # open the audio file using pydub
    sound = AudioSegment.from_wav(wav_file)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = DIRETORIO_CHUNKS
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    
    r = sr.Recognizer()
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=SOURCE_LANGUAGE)
                text_file = os.path.join(TEXT_BASE_PATH, get_file_name(wav_file).replace(WAV_EXTENSION, TXT_EXTENSION))
                filehandle = open(text_file, 'a')
                filehandle.write(text + ' \n')
                filehandle.close()
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(text)
                whole_text += text
                
                
def clear_directory(path):
    print('limpando diretorio: ', path)
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def start():
    video_list = glob.glob("./videos/*.mp4")
    start_time = datetime.now()
    
    for video_file in video_list:
        print('Iniciando processo de transcricao de audio  do arquivo :  ' + os.path.basename(video_file))
        clear_directory(AUDIO_BASE_PATH)
        extract_audio_from_video(video_file)
        convert_mp3_to_wave(os.path.join(AUDIO_BASE_PATH, get_file_name(video_file).replace(VIDEO_EXTENSION, MP3_EXTENSION)))
        wave_file = glob.glob(os.path.join(AUDIO_BASE_PATH, '*.wav'))
        extract_text_from_audio_chunks(wave_file[0])
        print('Transcricao concluida. Tempo total do proceso: ' + str((datetime.now() - start_time)))

start()