---
title: "CSE 493E Final Project Handin"
author: "Shreya Sathyanarayanan"
date: 2024-12-08
layout: post
---

# PlainScribe: A web app for generating plain text subtitles and transcripts for videos {: style="color: #32006e;" }

[**Link to PlainScribe GitHub Repository**](https://github.com/mygcho/cse493e-final-project)

## Introduction {: style="color: #32006e;" }

In today’s media-based world, we often consume video content. Whether it is a YouTube video or an important team meeting recording, we often try our best to understand the content. However, the lack of captions and video transcripts can hinder one’s understanding of the content. Currently, many videos do not have subtitles or automated captions. Many videos, especially newer YouTube uploads, do not have captions, which is an accessibility issue. The lack of captions can leave out populations from being informed. Auto-generated captions also lack a neat and easy-to-follow format when videos are played. Currently, videos with captions or transcripts do not provide plain text versions of the transcripts. Our project aims to help individuals who face challenges in understanding complex language.

In a professional context, working environments may not always be accessible or consider diverse needs of employees. Employees often face difficulties understanding terminology and content, especially if they have less experience. When starting out on a new job, people may find all the information overwhelming. This is especially true for those with intersectional identities, whether they are neurodiverse or speak English as a second language. With large amounts of content during team meetings, employees may face information overload. Plain text transcripts can help employees easily follow along and understand content. Overall, PlainScribe can improve communication in leadership, academic, or professional roles. When everyone can understand what is being said, there are fewer misunderstandings. PlainScribe aims to create more inclusive experiences when interacting with media content. Our tool is helpful for both disabled and non-disabled users.

## Positive Disability Principals {: style="color: #32006e;" }

**Is the practice, policy, or technology ableist?**

No, this technology is not ableist. It actively works against ableism by addressing barriers faced by individuals who struggle with dense or jargon-filled language. By focusing on accessibility and simplifying live meeting transcripts into plain language, it centers the needs of individuals with cognitive disabilities, non-native speakers, or those who process information differently, aiming to create a more inclusive environment.

**Accessible in part or as a whole?**

This project is partly accessible. It helps people who struggle with complex language, but we need to check if the tool itself is easy for everyone to use. Throughout initial development, the user interaction with the application still has yet to be tested. We should better research our implementation requirements to make sure that the user's ability to interact with the tool is accessible. We should ensure compatibility with assistive technologies like screen readers.

**Is it disability-led?**

The project is not fully disability-led. While it is informed by first-person accounts and centers the needs of individuals with disabilities, disabled individuals were actively involved in the design, development, or leadership of the project.

**Is it being used to give control and improve agency for people with disabilities?** 

Yes, this tool enhances agency for people with disabilities by providing them with the means to engage more fully in professional settings. It allows users to understand and participate in meetings in real time without external support, reducing dependency and enabling self-sufficiency. The project also acknowledges diverse communication needs, empowering people to advocate for their inclusion in decision-making processes.

**Is it addressing the whole community?**

Partially. While the project demonstrates intersectional awareness by addressing the needs of multiple groups, including those with cognitive disabilities and non-native speakers, it could be strengthened by further engaging multiple disabled individuals in the design process. It does recognize the intersectionality of needs but might not yet fully encompass all possible overlapping identities without additional community feedback.

## Methodology and Results {: style="color: #32006e;" }

![Screenshot of PlainScribe web app user interface. On the left side of the interface, there is a box for entering YouTube video URL with Download Video button below it. Below the YouTube downloader is a box for Uploading a Video, with a white arrow upload icon indicating the user to “Drop Video Here or Click to Upload”. Below this section is a dropdown menu for selecting transcription language. Below the dropdown is the Transcribe button followed by a Clear button. On the right side, there is an empty box with a film camera icon in the middle.](images/PlainScribeUI1.png)


![Screenshot of PlainScribe web app user interface. On the left side of the interface, there is a box for entering YouTube video URL with Download Video button below it. Below the button is a thumbnail of a user’s uploaded video. Under the uploaded video thumbnail is dropdown menu for selecting transcription language. Below the dropdown is the Transcribe button followed by a Clear button. On the right side, there is an image of the video output. Under the video output image is an option to download the video followed by an option to download the plaintext transcript of the video.](images/PlainScribeUI2.png)

The main features we wanted to implement for this project was to add subtitles to videos that do not have them, and add downloading and transcribing features as a minimum functionality. Adding options for different transcription languages, and letting the user have the option to download the video, original subtitles, and the plain language subtitles created a large range of use for our application. To increase the flexibility and options for video input, we wanted to add the feature for users to be able to add a YouTube URL or directly be able to transcribe it through our app, and additionally let the user upload media from their own device.  We also had the goal of implementing real-time system feedback to the user through a progress bar, so the user is well-informed while using PlainScribe.

We developed a web application using Python for both the frontend and backend. For the frontend of the application, we used *Python Gradio* to design an intuitive user interface for web apps. *Python Gradio* is a library used to develop working interfaces for applications using machine learning models. Users are able to input YouTube video URLs or upload videos from their devices. The interface shows the user the downloaded video. Users can select the transcription language from a dropdown menu. After selecting the transcription language, users can click on the “Transcribe” button to generate the video transcription. A downloadable version of the transcript is generated for the user and displayed on the interface. To clear all input, the user can click on the “Clear” button.

On the backend, the app downloads the video using the *YouTubeDL* library and gets the audio from the video using the *moviepy* Python library. Both the video downloading and audio retrieval process in preparation for transcription utilize *ffmpeg*, a framework for processing media. After retrieving the audio, the app uses *pyannote.audio.Pipeline* for diarization, parsing who is speaking. The app utilizes the speaker audio as data for Hugging Face’s *whisper* model to perform speech recognition and transcribe the speech into text.

To generate the plain text version of the transcript, the app uses Hugging Face’s *bart-large-cnn model*. The *Tqdm progress hook* is used to record progress on the diarization and audio transcription process. The progress for parsing who is speaking through diarization and transcribing the audio is displayed on the user interface as a progress bar. Using *Tqdm* helps provide users with clarity about where the script is in the diarization and transcription process, especially since video files take a long time to process.

![A diagram of the frontend and backend tech stack. Within rectangular outlines connected by arrows, lists ffmpeg, YoutubeDL, and Gradio. Within circular outlines connected by arrows, lists TqdmProgressHook, Hugging Face Model, and pyannote audio pipeline.](images/architectureDiagram.png)

Once the video is processed, the result is a new section on the application with the options to download the video, download the subtitles, or download the plain language subtitles. Throughout the whole process, a purple progress bar shows how far along PlainScribe is in downloading and transcribing the application. They can be downloaded in .mov and .srt formats, respectively. The .srt file can be viewable via Microsoft Word, to ensure that the transcript is viewable in an accessible document. The subtitles contain the timestamps of the speaker notes, and show the real audio versus the plain language transcription from the PlainScribe application.

![A screenshot of the original video transcript. Each line includes a timestamp of the video and has the captions below.](images/OriginalTranscript.png)
*Original Video Transcript*

![A screenshot of the plaintext video transcript after it has been processed by the PlainScribe application. Each line includes a timestamp of the video and has the simplified captions below.](images/PlainTextTranscript.png)
*Plain Text Video Transcript*

To test the accessibility of our application, the main tools we wanted to test with are magnifiers and screen readers. When resizing to 200% and using the magnifier for the resizing, the components of the application remain intact, and the user can scroll down to go to the next section. For the screen reader, each box and section headings are read out loud, including the downloadable files and that a video has to be uploaded by the user. 


## Disability Justice Analysis {: style="color: #32006e;" }

### Intersectionality {: style="color: #32006e;" }

**What it means:** Intersectionality in the context of disability involves the diverse lived experiences and identities of disabled people, which influence their perspectives and experiences in society. Diverse experiences and identities can include factors such as socioeconomic status, gender, race, and having multiple disabilities. The Disability Justice principle of Intersectionality recognizes that individuals often experience multiple, overlapping forms of discrimination or disadvantage due to their intersecting social identities.

**How our tool helps:** Designing and developing a tool that translates transcripts into plain text will support people with multiple disabilities and intersectional identities, because they can now process information in a simple format. Often in corporate settings, there are unrealistic expectations placed on employees without consideration of their needs and/or disability due to their level, years of experience, or standing in the company. Professional settings are also where employees of marginalized communities based on minority race and gender have needs that are often overlooked, as those who are higher-up are often not part of those communities and often do not fully acknowledge or understand their needs. There are many employees that may be on the lower end of the “corporate ladder” and are expected to uphold expectations on knowing and completing projects without realistic timing and fairness. Our project supports those who may relate to these intersectional identities, so they can look back at meetings and find a better summarized and easily comprehensible idea of meeting updates, tasks, and expectations while maintaining professionalism. Our project also benefits both disabled and non-disabled people since plain text is not limited to helping people with disabilities. Plain text can be helpful for people who want to learn about the main points or summary of a meeting rather than reading through the entire transcript, helping reduce cognitive load. Generating plain text versions of transcripts is an example of considering the diverse needs of people with disabilities and intersectional identities, ensuring that they effectively get the information they need.

### Leadership of Those Most Impacted {: style="color: #32006e;" }

**What it means:** Leadership of Those Most Impacted in the context of disability is focusing on understanding the experiences of people who endure the most impact as a result of systems that are not designed to be inclusive. This principle emphasizes the importance of involving individuals most affected by a system or issue in the decision-making processes that shape their lives.

**How our tool helps:** Meetings are often where concrete decisions and conversations in changing them are held, and people with disabilities are often not included in these discussions, causing overall inaccessibility in the environment and within the decision being made. Our project will ensure that the project team focuses on understanding the needs of individuals with disabilities by understanding first-person accounts of people with disabilities who prefer transcripts being offered in plain text. While the project team does not have access to people with disabilities to be integrated in the design process since this is a class project, the team’s learnings from first-person accounts will be incorporated in the tool’s design process, project planning, and decision-making.

In the case that the project team decides to pursue the project beyond the class, the team will seek perspectives and direct involvement from people with disabilities to iterate on the tool’s design, ensuring that their needs are met. The project team is focused on making sure that the tool empowers all users to reach their full potential and first hand experiences are integrated in the design and development process. The project team is interested in understanding the experiences of people with disabilities in professional settings and in what ways they think a plaintext tool can support them.

### Recognizing Wholeness {: style="color: #32006e;" }

**What it means:** Recognizing Wholeness emphasizes acknowledging and respecting the full humanity and inherent value of individuals with disabilities, rather than defining them by their perceived limitations.

**How our tool helps:** Our project team’s approach respects that a person’s worth is not determined by their ability to understand dense jargon or follow rapid conversation flow. Seeing everyone as whole to contribute to professional conversations and on potential outcomes, can make all participants feel whole and is the motivation for our plaintext tool. Our tool will contribute to the process of leveling the playing field in professional environments for users who benefit from reading plain text and easy to parse content, supporting them while completing tasks. Recognizing that people process information in different ways, instead of recognizing them by their limitations, is what we hope our project will help achieve through the plaintext generation, so users do not have to leave out of the meeting to do the translations themselves. By reducing the cognitive load of revisiting transcripts to understand meeting content through our tool’s plain text generations, users can focus during meetings and save time afterwards. Our project team understands that recognizing wholeness can be applicable for both disabled and non-disabled people, since everyone has diverse needs based on their circumstances and everyday life. For example, some users may just want to read a plain text version of a meeting they missed after being tired from a long day of work and everyday tasks at home.

Learnings and future work ~1-2 paragraphs (about 400 words): Describe what you learned and how this can be extended/ built on in the future.

We learned a significant amount on how technology can always be improved upon when considering accessibility. Simple changes such as the styling or typography and sizing of elements on a webpage can impact whether or not a user can use the technology, and we can make better strides to prevent these issues from happening. We also learned that while a good chunk of time spent on the functionality of the website is important, so is the documentation and the user-facing components. Something that can be furthered is using more of a custom combination of CSS with Gradio themes for the interface for more fine-grained styline details that ensure increased accessibility. When coding the project, we acknowledge that while the backend could be fully functional, it may not be usable if the user cannot easily interact with it and lacks accessible features.

## Learnings and Future Work {: style="color: #32006e;" }

Within the scope of programming the application, we learned new technologies that can improve upon current accessible technologies, such as the Speech-to-Text and Diarization models on Hugging Face. There is more to do for future work on choosing efficient models for PlainScribe, as the current models have limited processing capabilities when transcribing longer video files, such as movies and hour-long meetings. We discovered that the current version of the application can easily transcribe shorter videos within 3-5 minutes or so, but videos around 10 minutes have processing times that increase exponentially. We believe that using API calls to generative AI technologies, such as OpenAI’s ChatGPT, Groq, or Google Gemini would allow for faster and more refined plaintext transcription creation, but access to these APIs can be expensive. These APIs will provide us the flexibility of prompt engineering, which will help create refined output that further meets plain text guidelines. In the future, if there were to be an accessible free-tier AI model that can be used, this website would be able to process videos within seconds. We were also able to learn about efficient file management, including temporary file cleanup, when the user continues to use our application after a transcript is done with processing, and real-time progress tracking utilizing tools like TqdmProgressHook. We were able to improve our web app’s accessibility by informing the user of what the system is doing and how long it has left to transcribe. For progress checking, it would be interesting to see future work on informing the user in more accessible ways in addition to having a progress bar. Incorporating audio notifications about diarization and transcription progress can help increase accessibility.
