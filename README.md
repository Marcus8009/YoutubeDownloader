# YouTube Video Downloader

A Streamlit-based application that allows you to download YouTube videos in different qualities and formats.

## Features

- Download YouTube videos in various qualities (best, 720p, 480p, 360p)
- Download audio as MP3 files
- Support for multiple URLs (up to 5 at once)
- Custom download location support
- Progress bar for download tracking
- Input validation for YouTube URLs

## Requirements

### Python Packages
- Python 3.7+
- Streamlit
- yt-dlp

### System Dependencies
- FFmpeg (required for video processing)

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd YoutubeDownloader
```

2. Run the setup script:
```bash
setup_env.bat
```

3. Install FFmpeg using Chocolatey on Windows:

```bash
# IMPORTANT: Run PowerShell as Administrator
# 1. Press Windows key
# 2. Type "PowerShell"
# 3. Right-click "Windows PowerShell" and select "Run as administrator"

# If Chocolatey is not installed:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install FFmpeg
choco install ffmpeg --force
```

Alternative FFmpeg Installation Methods:
1. Download FFmpeg directly from [FFmpeg Official Website](https://ffmpeg.org/download.html)
2. Extract the ZIP file and add the `bin` folder to your system's PATH environment variable

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter up to 5 YouTube URLs in the input fields
3. Select your desired format:
   - MP4 Video: Choose video quality (best, 720p, 480p, 360p)
   - MP3 Audio: Extracts audio in MP3 format
4. Choose download location (defaults to your Downloads folder)
5. Click "Download All" to start downloading

## Troubleshooting

- If you get an FFmpeg error, ensure it's properly installed and available in your system PATH
- For permission errors when creating download directories, run the application with appropriate permissions
- Make sure your YouTube URL is valid and the video is available

## License

This project is open source and available under the MIT License.
