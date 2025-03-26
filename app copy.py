import streamlit as st
import subprocess
import os
from urllib.parse import urlparse
import yt_dlp

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

def main():
    st.title("YouTube Video Downloader")
    
    # Check for required dependencies
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        st.error("yt-dlp is not installed. Please install it using: pip install yt-dlp")
        return

    if not check_ffmpeg():
        st.error("ffmpeg is not installed. Please install it first:")
        st.code("Windows: choco install ffmpeg\nMac: brew install ffmpeg\nLinux: sudo apt install ffmpeg")
        return

    # Improved download location handling
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

    # Video quality options
    quality = st.selectbox(
        "Select Video Quality",
        ["best", "720p", "480p", "360p"]
    )

    # Add format selection
    format_type = st.radio(
        "Select Format",
        ["MP4 Video", "MP3 Audio"]
    )

    url = st.text_input("Enter the YouTube URL:")
    
    if st.button("Download"):
        if url and is_valid_youtube_url(url):
            try:
                st.write("Downloading...")
                progress_bar = st.progress(0)
                
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        progress = float(d['downloaded_bytes'] / d['total_bytes'])
                        progress_bar.progress(progress)

                if format_type == "MP4 Video":
                    ydl_opts = {
                        'format': f'bestvideo[height<={quality[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]' if quality != 'best' else 'best[ext=mp4]',
                        'outtmpl': f'{save_path}/%(title)s.mp4',
                        'progress_hooks': [progress_hook],
                        'merge_output_format': 'mp4',
                        'postprocessor_args': [
                            '-c:v', 'copy',
                            '-c:a', 'aac',
                        ]
                    }
                else:  # MP3 Audio
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{save_path}/%(title)s.mp3',
                        'progress_hooks': [progress_hook],
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                    }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                st.success("Download complete!")
            except Exception as e:
                st.error(f"Error during download: {str(e)}")
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
