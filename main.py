import assemblyai as aai
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
import os
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)
def url_process(video_url):
    video_id = video_url.split("v=")[1]
    try:
        list_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        with open("transcript" + video_id + ".txt", "a+", encoding="utf-8") as file:
            for transcript in list_transcript:
                file.write(transcript["text"] + "\n")
        print("Transcrição concluída. Arquivo txt salvo.")
        main()
    except:
        print("O vídeo não possui legendas.")
        print("Deseja baixar o arquivo mp3 para realizar a transcrição? ( 1 - SIM / 0 - NÃO )")
        print("OBS: Somente inglês")
        user_input = int(input())
        if user_input == 0:
            main()
        elif user_input == 1:
            fileName = file_download(video_url)
            print("Transcrição Iniciada")
            file_process(file_download(video_url))



def file_download(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )
    fileName = f"{video_info['title']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': fileName,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    return fileName

def file_process(fileName):
    aai.settings.api_key = "62458bcc09bd47edbf85a63733846c3f"
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(fileName, config)
    with open("transcript" + fileName.strip().replace(" ", "").replace(".mp3", "") + ".txt", "a+", encoding="utf-8") as file:
        for paragraph in transcript.get_paragraphs():
            file.write(paragraph.text + "\n")
    print("Transcrição concluída. Arquivo txt salvo.")
def main():
    print("1 - Inserir URL do vídeo")
    print("2 - Inserir arquivo MP3 ( Somente inglês )")
    user_input = int(input())
    if user_input == 1:
        video_url = str(input("URL:"))
        url_process(video_url)
    elif user_input == 2:
        fileName = str(input("File Name:"))
        try:
            file_process(fileName)
        except:
            print("Arquivo não encontrado. Deve estar na pasta local.")
            main()

if __name__ == "__main__":
    main()
