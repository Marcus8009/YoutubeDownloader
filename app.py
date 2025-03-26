import streamlit as st
import subprocess
import os
from urllib.parse import urlparse
import yt_dlp
import time
from typing import Dict

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_valid_youtube_url(url):
    try:
        parsed = urlparse(url)
        return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc
    except:
        return False

def download_video(url: str, save_path: str, format_type: str, quality: str, progress_dict: Dict) -> None:
    try:
        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                
                if total:
                    progress = float(downloaded / total)
                else:
                    speed = d.get('speed', 0)
                    progress = 0.5 if speed else 0
                        
                progress_dict[url] = progress
            elif d['status'] == 'finished':
                progress_dict[url] = 1.0

        common_opts = {
            'progress_hooks': [progress_hook],
            'retries': 10,
            'fragment_retries': 10,
            'socket_timeout': 30,
            'continuedl': True,
            'throttledratelimit': 100000,
            'sleep_interval': 2,
            'max_sleep_interval': 5,
        }

        if format_type == "MP4 Video":
            ydl_opts = {
                **common_opts,
                'format': f'bestvideo[height<={quality[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]' if quality != 'best' else 'best[ext=mp4]',
                'outtmpl': f'{save_path}/%(title)s.mp4',
                'merge_output_format': 'mp4'
            }
        else:
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'outtmpl': f'{save_path}/%(title)s.mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        progress_dict[url] = 1.0

    except Exception as e:
        st.error(f"Error downloading {url}: {str(e)}")
        progress_dict[url] = 1.0

def main():
    st.title("YouTube Video Downloader")
    
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        st.error("yt-dlp is not installed. Please install it using: pip install yt-dlp")
        return

    if not check_ffmpeg():
        st.error("ffmpeg is not installed. Please install it first:")
        st.code("Windows: choco install ffmpeg\nMac: brew install ffmpeg\nLinux: sudo apt install ffmpeg")
        return

    default_path = os.path.join(os.path.expanduser("~"), "Downloads")
    save_path = st.text_input(
        "Save videos to:",
        value=default_path,
        help="Enter the folder path where you want to save the videos (e.g., C:\\Users\\YourName\\Downloads)"
    )
    
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
            st.info(f"Created download directory: {save_path}")
        except Exception as e:
            st.error(f"Cannot create directory {save_path}. Please choose a valid location.")
            return

    quality = st.selectbox(
        "Select Video Quality",
        ["best", "720p", "480p", "360p"]
    )

    format_type = st.radio(
        "Select Format",
        ["MP4 Video", "MP3 Audio"]
    )

    urls = []
    for i in range(5):
        url = st.text_input(f"URL {i+1}:", key=f"url_{i}")
        if url:
            urls.append(url)

    if st.button("Download All"):
        urls = [url for url in urls if url.strip()]
        
        if not urls:
            st.warning("Please enter at least one URL")
            return

        invalid_urls = [url for url in urls if not is_valid_youtube_url(url)]
        if invalid_urls:
            st.error(f"Invalid URLs: {', '.join(invalid_urls)}")
            return

        progress_dict = {url: 0.0 for url in urls}
        progress_bars = {url: st.progress(0) for url in urls}

        with st.expander("Download Info", expanded=True):
            st.info("Downloads will process one at a time to avoid YouTube restrictions")

        for url in urls:
            st.write(f"Downloading: {url}")
            download_video(url, save_path, format_type, quality, progress_dict)
            while progress_dict[url] < 1.0:
                progress_bars[url].progress(progress_dict[url])
                time.sleep(0.1)
            progress_bars[url].progress(1.0)

        st.success("All downloads completed!")

if __name__ == "__main__":
    main()
