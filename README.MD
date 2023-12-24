# Cliplogger


Cliplogger is a Python script that monitors clipboard data and log them into markdown files
under an Obsidian vault, (not nessesarily) a directory on the user's local file system where all notes are stored.git 

## Dependencies

This script heavily relies on:

- **pyperclip:** This Python library is used for clipboard operations. It allows the script to access and modify
  clipboard data.

- **Pillow:** This Python Imaging Library is used to get images from the clipboard.

- **python-dotenv:** This Python library is used for managing environment variables.

## Functionality

The script is intended for the following tasks:

- Log images copied to clipboard.

- Log texts copied to clipboard and add timestamps.

- When a picture is copied to clipboard, save it to the obsidian_attachments folder and also add it to the note in a way
  that it can be viewed in Obsidian.

- Add tags to the notes.

- Log the active window name.

- Log the active window name and the time spent on it.

## To-do

- [x] Basics
- [ ] Module for logging active window name and time spent on it.
- [ ] Move image clips to seperate md file?
- [ ] Module for Encryption of the notes and git integration.
- [ ] what exactly happens when a `file` is copied to clipboard? FAFO
- [ ] Is this consuming too much memory? FAFO
- [ ] Module for removing passwords and emails and other sensitive data from the notes.
- [ ] Module for removing duplicate notes.

## LLM Integration

The end goal is to integrate this with a LLM. It should be providing additional context and thoughts to what the user is currently researching on, or perheps tell the user to stop playing rust for 7 hours straight with the context of the active window logging.

TLDR: Your personal AI powered Knowledge Management System.

