"""
python script to monitor clipboard and log them into markdown files under obsidian vault

TODO:
- [ ] should log images as well
- [ ] should all texts and add timestamps
- [ ] if a picture is copied, should save it to obsidian_attachments folder and also add it to the note in a way that it can be viewed in obsidian
- [ ] should be able to add tags to the notes
- [ ] log active window name as well
- [ ] log active window name and time spent on it

The Python library that can get both text and images from the clipboard is Pillow.
The ImageGrab.grabclipboard() function in Pillow can be used to get the image from the clipboard. If any non-image, such as text, is copied on the clipboard, ImageGrab.grabclipboard() returns None. For text-only clipboard operations, pyperclip can be used. To get an image from the clipboard using Pillow, the following code can be used:

Dependencies:
- pyperclip
- Pillow
"""
import hashlib
import os
import time
from datetime import datetime
from pathlib import Path

import PIL
import pyperclip
from PIL import ImageGrab
from dotenv import load_dotenv

# load environment variables
load_dotenv()
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")
OBSIDIAN_ATTACHMENTS_PATH = os.getenv("OBSIDIAN_ATTACHMENTS_PATH")

# define clipboard log file
CLIPBOARD_LOG_FILE = OBSIDIAN_VAULT_PATH + r'\clipboard.md'

def get_clipboard_data():
    """
    Return the data currently stored in the clipboard.

    :return: The data currently stored in the clipboard.
    :rtype: str
    """
    return pyperclip.paste()

def get_clipboard_image():
    """
    Get the image currently on the clipboard.

    :return: The image on the clipboard if it is an instance of PIL.Image.Image, otherwise None.
    :rtype: PIL.Image.Image or None
    """
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, PIL.Image.Image):
            return image
        else:
            return None
    except:
        return None

def create_obsidian_note():
    """
    :return: None
    :rtype: None

    """
    if not Path(CLIPBOARD_LOG_FILE).exists():
        Path(CLIPBOARD_LOG_FILE).touch()

def append_obsidian_note(content,image_path=None):
    """
    Append a note to the Obsidian log file.

    :param content: The content of the note.
    :type content: str
    :param image_path: Optional path to an image file to include in the note, defaults to None.
    :type image_path: Optional[str], optional
    :return: None
    :rtype: None
    """
    if image_path is not None:
        content = f'![Clipboard Image]({content})'
        with open(CLIPBOARD_LOG_FILE, 'a', encoding='utf-8') as file:  # added encoding
            file.write(f"- {datetime.now().isoformat()}:\n\n```\n{content}\n```\n")
            file.write(image_path)
    else:
        with open(CLIPBOARD_LOG_FILE, 'a', encoding='utf-8') as file:  # added encoding
            file.write(f"- {datetime.now().isoformat()}:\n\n```\n{content}\n```\n")


def save_obsidian_image(image):
    """
    :param image: The image that needs to be saved.
    :type image: PIL Image object
    :return: None
    :rtype: None

    This method saves the given `image` to a file in the Obsidian vault. The file name is generated based on the current timestamp to ensure uniqueness. The saved file path is then used
    * to generate an Obsidian compatible image link, which is then appended to an Obsidian note titled "clipboard image".

    Example usage:
        save_obsidian_image(image)
    """
    timestamp = datetime.now().isoformat().replace(':', '_')  # replaced ':' with '_'
    image_filename = OBSIDIAN_ATTACHMENTS_PATH + f'\clipboard_image_{timestamp}.png'
    image.save(image_filename)

    # ![](clipboard_image_1703373990.8852599.png)
    relative_image_filename = image_filename.replace(OBSIDIAN_VAULT_PATH,"")
    relative_image_filename = relative_image_filename.replace("\\","/")
    image_link = f'![]({relative_image_filename})'
    append_obsidian_note("clipboard image",image_link)

def image_to_hash(image):
    """
    Convert an image to its corresponding hash value.

    :param image: The image to be hashed.
    :type image: PIL.Image.Image
    :return: The hash value of the image.
    :rtype: str
    """
    image_bytes = image.tobytes()  # Convert image data to bytes
    image_hash = hashlib.sha256(image_bytes).hexdigest()  # Hash the bytes
    return image_hash

def monitor_clipboard():
    """
    Monitors the clipboard for updates and performs certain actions based on the clipboard data.

    Returns:
    :return: None
    :rtype: None

    Description:
    This method continuously checks the clipboard for updates. It retrieves the clipboard data and image,
    and performs actions based on the type of data.

    If an image is found in the clipboard, it compares the hash of the image with the previously stored hash.
    If the two hashes are different, it saves the image to an Obsidian note and updates the last_image_hash
    with the new hash.

    If text data is found in the clipboard and it is different from the previously stored data, it appends the
    text data to an Obsidian note and updates the last_data with the new data.

    The method uses the following helper methods:
    - create_obsidian_note(): Creates a new Obsidian note.
    - get_clipboard_data(): Retrieves the data currently in the clipboard.
    - get_clipboard_image(): Retrieves the image currently in the clipboard.
    - image_to_hash(): Converts an image into a hash.
    - save_obsidian_image(): Saves an image to an Obsidian note.
    - append_obsidian_note(): Appends text data to an Obsidian note.

    The method also includes a time.sleep(0.1) to prevent excessive checking of the clipboard.

    Example usage:
    monitor_clipboard()
    """
    create_obsidian_note()
    last_data = None
    last_image_hash = None
    while True:
        clipboard_data = get_clipboard_data()
        clipboard_image = get_clipboard_image()
        if clipboard_image is not None:
            current_image_hash = image_to_hash(clipboard_image)
            if current_image_hash != last_image_hash:
                save_obsidian_image(clipboard_image)
                last_image_hash = current_image_hash
        elif clipboard_data is not None and clipboard_data != last_data:
            append_obsidian_note(clipboard_data)
            last_data = clipboard_data
        time.sleep(0.1)

if __name__ == "__main__":

    monitor_clipboard()