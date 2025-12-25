<!-- PROJECT LOGO -->
<p align="center">
  <img width="250" src="https://www.jing.fm/clipimg/full/357-3579864_pokemon-sword-shield-logo.png" />
  <img width="250" src="https://cdn3.iconfinder.com/data/icons/popular-services-brands-vol-2/512/twitch-512.png" />
</p>

<p align="center">
  <a href="https://github.com/xmarston/stream-pkm-update-counter/actions/workflows/ci.yml"><img src="https://github.com/xmarston/stream-pkm-update-counter/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/coverage-99%25-brightgreen" alt="Coverage">
  <img src="https://img.shields.io/badge/python-3.13+-blue" alt="Python 3.13+">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#docker">Docker</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#notes">Notes</a></li>
    <li><a href="#demo">Demo</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The goal of this project is to automate the repetitive task of increasing the value while doing shiny hunting in Pokémon Sword/Shield. The project is aimed for streamers that wants to increase their productivity being more focus on their viewers and chat interactions.

### Built With

* Python 3.13+
* [OpenCV](https://opencv.org/)
* [Tesseract](https://github.com/tesseract-ocr/tesseract)
* Docker (optional)

<!-- GETTING STARTED -->
## Getting Started

To get this running in your local environment we need to do some steps before actually running it.

### Prerequisites

Before installing the dependencies for Python we need to have installed Tesseract in our local machine. I recommend doing it with [Brew](https://brew.sh). After install Brew you just need to run:

```bash
brew install tesseract
```

### Installation

After installing the prerequisites, install the Python dependencies:

```bash
pip3 install -r requirements.txt
```

### Docker

Alternatively, you can run the project using Docker:

```bash
docker compose up --build
```

This will build the image with all dependencies (including Tesseract) and start the counter.

<!-- USAGE EXAMPLES -->
## Usage

The command accepts the following arguments:

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `-inputVideo` | `-i` | Yes | Capture device number (usually 0) |
| `-file` | `-f` | Yes | File where the counter is stored |
| `-phrase` | `-p` | Yes | Phrase to detect in the video stream |
| `-debounce` | `-d` | No | Seconds between detections (default: 15) |

**Run with Python:**
```bash
python -m stream_counter -i 0 -f counter.txt -p "PHRASE_TO_SEARCH"

# Or using the wrapper script
python main.py -i 0 -f counter.txt -p "PHRASE_TO_SEARCH"
```

**Run with Docker:**
```bash
docker compose run stream-counter -i 0 -f /data/counter.txt -p "PHRASE_TO_SEARCH" -d 10
```

## Notes

Didn't found why but you need to execute this script before your OBS or whatever software you are using for streaming because if you open after the script will crash.

## Demo

[![Demo Video](http://img.youtube.com/vi/rAqJKe2oneA/0.jpg)](http://www.youtube.com/watch?v=rAqJKe2oneA "Demonstration Stream PKM Counter Auto Updater")
