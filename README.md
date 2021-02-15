<!-- PROJECT LOGO -->
<p align="center">
  <img width="250" src="https://www.jing.fm/clipimg/full/357-3579864_pokemon-sword-shield-logo.png" />
  <img width="250" src="https://cdn3.iconfinder.com/data/icons/popular-services-brands-vol-2/512/twitch-512.png" />
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
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#notes">Notes</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The goal of this project is to automate the repetitive task of increasing the value while doing shiny hunting in Pokémon Sword/Shield. The project is aimed for streamers that wants to increase their productivity being more focus on their viewers and chat interactions.

### Built With

Script is built with:
* Python 3.8
* [OpenCV](https://opencv.org/)
* [Tesseract](https://github.com/tesseract-ocr/tesseract)

<!-- GETTING STARTED -->
## Getting Started

To get this running in your local environment we need to do some steps before actually running it.

### Prerequisites

Before installing the dependencies for Python we need to have installed Tesseract in our local machine. I recommend doing it with [Brew](https://brew.sh). After install Brew you just need to run:

```bash
brew install tesseract
```

### Installation

After we installed all the things that were prerequisites now we can proceed to install the python libraries we need to run the script. For this we simply run this comando:

```bash
pip3 install -r requirements.txt
```

If the installation was successful we can run the command.

<!-- USAGE EXAMPLES -->
## Usage

The command accepts three arguments that are required:
* inputVideo: This is the number that indicates your capture card, in most cases it works with 0 but you'll need to test if not.
* file: File where the number to increase is stored.
* phrase: This is the phrase that the process will look for it in the video stream and update the counter.

So the command will look like this:
```bash
python3 process_stream.py -inputVideo 0 -file PATH_OF_THE_FILE -phrase "PHRASE_TO_SEARCH"
```

## Notes

Didn't found why but you need to execute this script before your OBS or whatever software you are using for streaming because if you open after the script will crash.
