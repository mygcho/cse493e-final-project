import gradio as gr
from pyannote.audio import Pipeline
from transformers import pipeline as hf_pipeline
import pysrt
from tqdm import tqdm
from moviepy import VideoFileClip
from typing import Any, Mapping, Optional, Text

# Custom hook class to show progress using tqdm
class TqdmProgressHook:
    """Hook to show progress of each internal step using tqdm"""

    def __init__(self):
        self.current_step_bar = None  # Placeholder for the current tqdm progress bar

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.current_step_bar:
            self.current_step_bar.close()

    def __call__(
        self,
        step_name: Text,
        step_artifact: Any,
        file: Optional[Mapping] = None,
        total: Optional[int] = None,
        completed: Optional[int] = None,
    ):
        if completed is None:
            completed = total = 1
        if not hasattr(self, "step_name") or step_name != self.step_name:
            self.step_name = step_name
            if self.current_step_bar:
                self.current_step_bar.close()
            self.current_step_bar = tqdm(total=total, desc=f"{step_name}")
        if self.current_step_bar:
            self.current_step_bar.update(1)

def format_selector(ctx):
    """Select the best video and the best audio that won't result in an mkv.
    Ensures the output format is mp4."""
    formats = ctx.get('formats')[::-1]
    best_video = next(
        f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')
    audio_ext = 'm4a'
    best_audio = next(f for f in formats if f['acodec'] !=
                      'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext)

    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': 'mp4',
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }


# Function to convert seconds to pysrt.SubRipTime
def convert_seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=secs, milliseconds=millis)
