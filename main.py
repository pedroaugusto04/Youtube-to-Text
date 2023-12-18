import assemblyai as aai
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
import sys
def url_process(video_url):
    video_id = video_url.split("v=")[1]
    try:
        list_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        for transcript in list_transcript:
            print(transcript["text"])
        sys.exit()
    except:
        print("Erro ao buscar legendas. Tentando outro método")
    finally:
        file_process(video_url)

def file_process(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )
    fileName = f"{video_info['title']}.mp3"
    options={
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': fileName,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    aai.settings.api_key = "62458bcc09bd47edbf85a63733846c3f"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(fileName)
    with open("transcript" + fileName.strip().replace(" ", "").replace(".mp3", "") + ".txt", "a+", encoding="utf-8") as file:
        for paragraph in transcript.get_paragraphs():
            file.write(paragraph.text + "\n")

def main():
    print("1 - Inserir URL do vídeo")
    print("2 - Inserir arquivo MP3")
    user_input = int(input())
    if user_input == 1:
        video_url = str(input("URL:"))
        url_process(video_url)
    elif user_input == 2:
        video_url = str(input("URL:"))
        file_process(video_url)

if __name__ == "__main__":
    main()
