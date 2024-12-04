import gradio as gr
import yt_dlp
import os
import torchaudio
from pyannote.audio import Pipeline
from transformers import pipeline as hf_pipeline
import pysrt
from tqdm import tqdm
from moviepy import VideoFileClip
import torch
import re
from typing import Any, Mapping, Optional, Text
import yaml
import shutil
from backend.utils import convert_seconds_to_srt_time, format_selector, TqdmProgressHook
from transformers import pipeline

# Load configuration from YAML file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Configure token and models from Hugging Face website
huggingface_token = config['huggingface']['token']
transcribe_model_path = config['huggingface']['transcribe_model_path']
diarization_model = config['huggingface']['diarization_model']
language_choices = config['languages']

result_folder = "result"
os.makedirs(result_folder, exist_ok=True)

# Helper function to extract audio from a video file
def extract_audio_from_video(video_path, output_wav_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_wav_path, codec='pcm_s16le')

# Helper function to simulate the transcription task with progress
def transcribe_video(input_video, language, progress=gr.Progress(track_tqdm=True)):
    os.makedirs("audio_chunks", exist_ok=True)

    # Extract the filename and extension from the input video path
    filename, ext = os.path.splitext(os.path.basename(input_video))
    # If the filename doesn't have an extension, add .mp4
    if not ext:
        ext = '.mp4'  # Add .mp4 as the default extension

    # Else, construct the full path for the output video
    video = os.path.join(result_folder, filename + ext)
    shutil.copy(input_video, video)
    
    wav_path = os.path.join(result_folder,"tmp.wav")
    srt_output_path = os.path.join(result_folder, f"{filename}.srt")

    extract_audio_from_video(video, wav_path)

    pipeline = Pipeline.from_pretrained(diarization_model, use_auth_token=huggingface_token)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipeline.to(device)

    whisper_pipe = hf_pipeline("automatic-speech-recognition", model=transcribe_model_path,
                               device=0 if torch.cuda.is_available() else -1, generate_kwargs={"language": language, "task": "transcribe"})

    waveform, sample_rate = torchaudio.load(wav_path)

    with TqdmProgressHook() as hook:
        diarization = pipeline(wav_path, hook=hook)

    subs = pysrt.SubRipFile()
    total_segments = len(list(diarization.itertracks(yield_label=True)))
    progress_bar = tqdm(total=total_segments, desc="Transcribing")

    chunk_index = 0
    chunk_files = []
    sentence_splitter = re.compile(r'(?<=[.!?]) +')

    for speech_turn, _, _ in diarization.itertracks(yield_label=True):
        seg_start = speech_turn.start
        seg_end = speech_turn.end
        chunk_waveform = waveform[:, int(seg_start * sample_rate):int(seg_end * sample_rate)]
        chunk_filename = f"audio_chunks/temp_chunk_{chunk_index}.wav"
        torchaudio.save(chunk_filename, chunk_waveform, sample_rate)
        result = whisper_pipe(chunk_filename)
        transcription_text = result['text'].strip()
        sentences = sentence_splitter.split(transcription_text)

        total_duration_ms = (seg_end - seg_start) * 1000
        total_chars = sum(len(sentence) for sentence in sentences)
        current_start_time_ms = seg_start * 1000

        for sentence in sentences:
            words = sentence.split()
            if len(words) > 8:
                sentence_chunks = [words[i:i + 8] for i in range(0, len(words), 8)]
                total_words_in_sentence = len(words)
                sentence_ratio = len(sentence) / total_chars
                sentence_duration_ms = total_duration_ms * sentence_ratio

                for chunk in sentence_chunks:
                    chunk_word_count = len(chunk)
                    chunk_duration_ms = sentence_duration_ms * (chunk_word_count / total_words_in_sentence)
                    end_time_chunk_ms = current_start_time_ms + chunk_duration_ms
                    start_srt_time = convert_seconds_to_srt_time(current_start_time_ms / 1000)
                    end_srt_time = convert_seconds_to_srt_time(end_time_chunk_ms / 1000)

                    subtitle = pysrt.SubRipItem(index=len(subs) + 1, start=start_srt_time, end=end_srt_time, text=' '.join(chunk).strip())
                    subs.append(subtitle)
                    current_start_time_ms = end_time_chunk_ms
            else:
                sentence_ratio = len(sentence) / total_chars
                sentence_duration_ms = total_duration_ms * sentence_ratio
                end_time_sentence_ms = current_start_time_ms + sentence_duration_ms
                start_srt_time = convert_seconds_to_srt_time(current_start_time_ms / 1000)
                end_srt_time = convert_seconds_to_srt_time(end_time_sentence_ms / 1000)

                subtitle = pysrt.SubRipItem(index=len(subs) + 1, start=start_srt_time, end=end_srt_time, text=sentence.strip())
                subs.append(subtitle)
                current_start_time_ms = end_time_sentence_ms

        chunk_index += 1
        chunk_files.append(chunk_filename)
        progress_bar.update(1)

    progress_bar.close()
    subs.save(srt_output_path, encoding='utf-8')

    # Generate plain language subtitles
    plain_srt_path = generate_plain_language_subtitles(srt_output_path, language)

    for chunk_file in chunk_files:
        os.remove(chunk_file)
    os.remove(wav_path)

    return (video, srt_output_path, plain_srt_path), (video, srt_output_path), gr.update(value=video, visible=True), gr.update(value=srt_output_path, visible=True), gr.update(value=plain_srt_path, visible=True)

# Helper function to clear the video player and remove the SRT file
def clear_output(video_and_srt_paths):
    video, srt_output_path, plain_srt_path = video_and_srt_and_plain_srt_paths
    
    if os.path.exists(srt_output_path):
        os.remove(srt_output_path)
    if os.path.exists(plain_srt_path):
        os.remove(plain_srt_path)
    if os.path.exists(video):
        os.remove(video)
    
    return gr.update(value=None), gr.update(value=None), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), \
           gr.update(value=None, label="Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=example"), gr.update(value=None, visible=False), \
           gr.update(value=None)

def download_and_update(url):

    # This gets the downloaded video file name either from system or from YouTube
    output_file_from_download = os.path.join(result_folder, "download_file.mp4")

    # Checks if user submitted a file from the system
    if os.path.exists(output_file_from_download):
        os.remove(output_file_from_download)
    
    # Checks if the user submitted a file from a YouTube link
    ydl_opts = {
        'format': format_selector,
        "outtmpl": output_file_from_download,
        "merge_output_format": "mp4",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_file_from_download



def generate_plain_language_subtitles(srt_file_path, language):
    subs = pysrt.open(srt_file_path)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    plain_subs = pysrt.SubRipFile()
    
    for sub in subs:
        summary = summarizer(sub.text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
        plain_sub = pysrt.SubRipItem(
            index=sub.index,
            start=sub.start,
            end=sub.end,
            text=summary
        )
        plain_subs.append(plain_sub)
    
    plain_srt_file_path = srt_file_path.replace('.srt', '_plain.srt')
    plain_subs.save(plain_srt_file_path, encoding='utf-8')
    
    return plain_srt_file_path
