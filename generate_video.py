from moviepy.editor import *
from moviepy.video.VideoClip import TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import fire

def generate_video(audio_file, subtitle_file, output_file):
    audio = AudioFileClip(audio_file)
    video = ColorClip((1280, 720), (0, 0, 0)).set_duration(audio.duration)
    video = video.set_audio(audio)

    # apt-get install ttf-wqy-microhei
    subtitle = SubtitlesClip(subtitle_file, make_textclip=lambda txt: TextClip(txt, font='WenQuanYi-Micro-Hei',
                                            fontsize=40, color='white', 
                                            stroke_color='white', stroke_width=0.5))
    subtitle = subtitle.set_position('center', 'center')

    #final_clip = final_clip.subclip(0, audio.duration).set_audio(audio)
    #final_clip = final_clip.set_audio(audio).set_duration(subtitle.duration).set_fps(24)
    final_clip = CompositeVideoClip([video, subtitle])

    final_clip.write_videofile(output_file, fps=24)

if __name__ == "__main__":
    fire.Fire(generate_video)