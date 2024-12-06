import gradio as gr
from backend.processing import transcribe_video, clear_output, download_and_update

import gradio as gr

def prepare_to_download():
    return "Downloading and Processing Videos...", gr.update(visible=True)

def complete_status():
    return "Download completed."

def show_uploaded_video(video_file):
    return video_file.name

def create_interface(language_choices):
    with gr.Blocks(theme=gr.themes.Soft()) as iface:
        gr.Markdown("# PlainScribe")
    #     gr.Markdown("""
    # # PlainScribe <img src="https://photos.onedrive.com/photo/C0B185B397D4957F!s3d08f7c9ece34b078fcabf7157c30558?view=all" alt="icon" style="vertical-align: middle; height: 24px;">
    # """)
        video_and_srt_and_plain_srt_paths = gr.State()
        
        with gr.Row():
            with gr.Column(scale=1):
                youtube_url_input = gr.Textbox(label="Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=example")
                download_button = gr.Button("Download Video")
                status_text = gr.Textbox(label="Download Status", interactive=False, visible=False)
                video_input = gr.Video(label="Upload a video")
                language_dropdown = gr.Dropdown(label="Select Transcription Language", choices=language_choices, value="English")
                transcribe_button = gr.Button("Transcribe")
                clear_button = gr.Button("Clear")
            
            with gr.Column(scale=2):
                video_output = gr.Video(label="Video Output", interactive=False)
                download_video_button = gr.File(label="Download Video", visible=False)
                download_sub_button = gr.File(label="Download Subtitles", visible=False)
                download_plain_sub_button = gr.File(label="Download Plain Language Subtitles", visible=False)
        
        transcribe_button.click(
            fn=transcribe_video,
            inputs=[video_input, language_dropdown],
            outputs=[video_and_srt_and_plain_srt_paths, video_output, download_video_button, download_sub_button, download_plain_sub_button]
        )
        
        clear_button.click(
            fn=clear_output,
            inputs=[video_and_srt_and_plain_srt_paths],
            outputs=[video_input, video_output, download_sub_button, download_video_button, download_plain_sub_button,
                     youtube_url_input, status_text, video_and_srt_and_plain_srt_paths]
        )
        
        download_button.click(
            fn=prepare_to_download,
            inputs=None,
            outputs=[status_text, status_text]
        ).then(
            fn=download_and_update,
            inputs=[youtube_url_input],
            outputs=[video_input]
        ).then(
            fn=complete_status,
            inputs=None,
            outputs=[status_text]
        )
        
        return iface


# import gradio as gr
# from backend.processing import transcribe_video, clear_output, download_and_update
# from backend.utils import format_selector


# def prepare_to_download():
#     return "Downloading and Processing Videos...", gr.update(visible=True)

# def complete_status():
#     return "Download completed."

# def show_uploaded_video(video_file):
#     return video_file.name

# def create_interface(language_choices):
#     """Creates and launches the Gradio interface for the application."""
#     with gr.Blocks() as iface:
#         gr.Markdown("# PlainScribe")

#         video_and_srt_paths = gr.State()

#         with gr.Row():
#             with gr.Column(scale=1):
#                 youtube_url_input = gr.Textbox(
#                     label="Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=example")
#                 download_button = gr.Button("Download Video")
#                 status_text = gr.Textbox(
#                     label="Download Status", interactive=False, visible=False)
#                 video_input = gr.Video(label="Upload a video")
#                 language_dropdown = gr.Dropdown(
#                     label="Select Transcription Language",
#                     choices=language_choices,
#                     value="English"
#                 )
#                 transcribe_button = gr.Button("Transcribe")
#                 clear_button = gr.Button("Clear")

#             with gr.Column(scale=2):
#                 video_output = gr.Video(label="Video Output", interactive=False)
#                 download_video_button = gr.File(
#                     label="Download Video", visible=False)
#                 download_sub_button = gr.File(
#                     label="Download Subtitles", visible=False)

#         # Link functions to Gradio buttons
#         transcribe_button.click(
#             fn=transcribe_video,
#             inputs=[video_input, language_dropdown],
#             outputs=[video_and_srt_paths, video_output, download_video_button, download_sub_button]
#         )

#         clear_button.click(
#             fn=clear_output,
#             inputs=[video_and_srt_paths],
#             outputs=[video_input, video_output, download_sub_button, download_video_button,
#                      youtube_url_input, status_text, video_and_srt_paths]
#         )

#         download_button.click(
#             fn=prepare_to_download,
#             inputs=None,
#             outputs=[status_text, status_text]
#         ).then(
#             fn=download_and_update,
#             inputs=[youtube_url_input],
#             outputs=[video_input]
#         ).then(
#             fn=complete_status,
#             inputs=None,
#             outputs=[status_text]
#         )

#     return iface