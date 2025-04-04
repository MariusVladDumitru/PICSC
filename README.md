# Project Goal
This project is a ML classifier for the open-source RTS game 0.A.D, available at. [https://play0ad.com/](https://play0ad.com/).  
For a given 0.A.D 1v1 match, the system needs to classify a player either a human or a bot, based on network traffic.

# Dataset
The information about the players are in the form of 0.A.D network traffic between a server and a client. This network traffic is captured by Wireshark and saved in .pcapng files.  
The dataset are .pcapng files alongside an annotations file. The system will extract relevant features that describes human and bot behavior then provide them to the model as input.

# Features

# Model Architecture

# Model Evaluation

# Repository folder structure
- code - all source code
- dataset - dataset files
- docs - relevant documentation files
- requirements.txt - requirements file

# Setup
Install Anaconda or Minicoda from [https://www.anaconda.com/](https://www.anaconda.com/), create a new environment then use the requirements.txt to install dependencies.  
This project has been developed using Pycharm.

# Online Excel
You need to fill [THIS EXCEL SHEEL](https://docs.google.com/spreadsheets/d/1sCSNc8fENn2IUW9N9jBTf3NwCcJGTEYj3rO-6mazUt4/edit?gid=816756393#gid=816756393) under your name.