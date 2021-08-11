# alx-audio-transcript

This script was built to help the large audio or video files transcription. Currently the script is configured to extract the transcription from a video file source, but is possible to adapt it to use a audio file source easily.

#### Libs and thecnologies used

> python3, pip3, SpeechRecognition, Pydub, moviePy



## instalation (linux based)

### Requeriments

    python 3^

### Steps

####  Install ffmpeg codec

    sudo apt update
    sudo apt install ffmpeg


####  Install requirements

    pip3 install requirements.txt

#### Project Structure

    src/
	|__
	    |__audios/
	    |__texts/
	    |__videos/
	    |__app.py

#### how to use

 1. Create directories: audios/, texts/, and videos/ 
 2. Put the video file into videos directory
 3. Execute de command indo src directory: 
  `python app.py`
 6. The process will start extracting the audio (mp3) from video file.
 7. After, the mp3 audio will be converted to wav.
 8. In the final step, the process will catch the large audio file (wav) and will slice in small chunks and will start the transcription.  This process can be seen on the console where the transcript will be displayed.
 9. When the process finish, the complet transcription will be in direcoty texts/original_file_name.txxt


Author: [André Luiz Ximenes](https://www.linkedin.com/in/andreluizximenes/)
Email: andreluizximenes@gmail.com
