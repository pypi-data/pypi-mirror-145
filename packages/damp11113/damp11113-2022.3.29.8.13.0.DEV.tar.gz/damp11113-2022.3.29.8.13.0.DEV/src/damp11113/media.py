import vlc
import pafy
import ffmpeg
import cv2
import tqdm
import os
from PIL import Image
from damp11113.file import sizefolder

class vlc_player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def load(self, file_path):
        self.media = self.instance.media_new(file_path)
        self.player.set_media(self.media)
        return f"Loading {file_path}"

    def play(self):
        self.player.play()
        return f"Playing {self.media.get_mrl()}"

    def pause(self):
        self.player.pause()
        return f"Pausing {self.media.get_mrl()}"

    def stop(self):
        self.player.stop()
        return f"Stopping {self.media.get_mrl()}"

    def get_position(self):
        return self.player.get_position()

    def set_position(self, position):
        self.player.set_position(position)
        return f"Setting position to {position}"

    def get_state(self):
        return self.player.get_state()

    def get_length(self):
        return self.media.get_duration()

    def get_time(self):
        return self.player.get_time()

    def set_time(self, time):
        self.player.set_time(time)
        return f"Setting time to {time}"

    def get_rate(self):
        return self.player.get_rate()

    def set_rate(self, rate):
        self.player.set_rate(rate)
        return f"Setting rate to {rate}"

    def get_volume(self):
        return self.player.audio_get_volume()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)
        return f"Setting volume to {volume}"

    def get_mute(self):
        return self.player.audio_get_mute()

    def set_mute(self, mute):
        self.player.audio_set_mute(mute)
        return f"Setting mute to {mute}"

    def get_chapter(self):
        return self.player.get_chapter()

    def set_chapter(self, chapter):
        self.player.set_chapter(chapter)
        return f"Setting chapter to {chapter}"

    def get_chapter_count(self):
        return self.media.get_chapter_count()

    def get_title(self):
        return self.player.get_title()

    def set_title(self, title):
        self.player.set_title(title)
        return f"Setting title to {title}"

    def get_title_count(self):
        return self.media.get_title_count()

    def get_video_track(self):
        return self.player.video_get_track()

    def set_video_track(self, track):
        self.player.video_set_track(track)
        return f"Setting video track to {track}"

    def get_video_track_count(self):
        return self.media.get_video_track_count()

    def get_audio_track(self):
        return self.player.audio_get_track()

    def set_audio_track(self, track):
        self.player.audio_set_track(track)
        return f"Setting audio track to {track}"

    def get_audio_track_count(self):
        return self.media.get_audio_track_count()

    def get_spu_track(self):
        return self.player.video_get_spu()

    def set_spu_track(self, track):
        self.player.video_set_spu(track)
        return f"Setting subtitle track to {track}"

    def get_spu_track_count(self):
        return self.media.get_spu_track_count()

    def get_chapter_description(self, chapter):
        return self.media.get_chapter_description(chapter)

class youtube_stream:
    def __init__(self, url):
        self.stream = pafy.new(url)

    def video_stream(self):
        best = self.stream.getbestvideo()
        return best.url

    def audio_stream(self):
        best = self.stream.getbestaudio()
        return best.url

    def best_stream(self):
        best = self.stream.getbest()
        return best.url

class ffmpeg_stream:
    def __init__(self) -> None:
        pass

    def load(self, file_path):
        self.stream = ffmpeg.input(file_path)
        return f"Loaded {file_path}"

    def write(self, file_path, format, ac=2, hz='44100', bitrate='320'):
        ffmpeg.run(self.stream.output(file_path, acodec=format, ac=ac, ar=hz, **{'b:a': f'{bitrate}k'}))
        return f"Writing {file_path}"

    def streaming(self, url, format='mp4', ac=2, hz='44100', bitrate='320'):
        ffmpeg.run(self.stream.output(url, acodec=format, ac=ac, ar=hz, **{'b:a': f'{bitrate}k'}))
        return f"Streaming {url}"

def clip2frames(clip_path, frame_path, currentframe=0, filetype='png'):
    try:
        clip = cv2.VideoCapture(clip_path)
        length = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
        progress = tqdm.tqdm(total=length, unit='frame')
        progress.set_description(f'set output to {frame_path}')
        if not os.path.exists(frame_path):
            os.mkdir(frame_path)
            progress.set_description(f'create output folder {frame_path}')
        progress.set_description(f'converting... ')
        while True:
            size = sizefolder(frame_path)
            ret, frame = clip.read()
            cv2.imwrite(f'./{frame_path}/{str(currentframe)}' + f'.{filetype}', frame)
            progress.set_description(f'converting... | filetype .{filetype} | converted {currentframe}/{length} | file {currentframe}.{filetype} | used {size} MB')
            currentframe += 1
            progress.update(1)
            if currentframe == length:
                progress.set_description(f'converted {currentframe} frame | used {size} MB')
                progress.close()
                break
    except Exception as e:
        progress = tqdm.tqdm(total=0)
        progress.set_description(f'error: {e}')
        progress.close()

def im2ascii(image, width=None, height=None, new_width=120, chars=None):
    try:
        img = Image.open(image)
        if width is not None and height is not None:
            img = img.resize((width, height))
        elif width is not None:
            img = img.resize((width, int(img.size[1] * width / img.size[0])))
        elif height is not None:
            img = img.resize((int(img.size[0] * height / img.size[1]), height))
        elif chars is not None:
            chars = ["B","S","#","&","@","$","%","*","!",":","."]
        else:
            width, height = img.size
            aspect_ratio = width / height
            new_height = int(new_width / aspect_ratio)
            img = img.resize((new_width, new_height))
        img = img.convert('L')
        pixels = img.getdata()
        new_pixels = [chars[pixel//25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        return ascii_image
    except Exception as e:
        raise e

def im2pixel(input_file_path, output, pixel_size=5):
    image = Image.open(input_file_path)
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )

    image.save(output)