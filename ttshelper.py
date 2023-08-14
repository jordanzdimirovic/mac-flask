"""
Text-to-speech helper

This will conditionally use different TTS method
based on your operating system.

Allows for simple TTS usage through the `say` function

Author: Jordan Zdimirovic (MAC)
"""

# Imports
import os
import sys
import threading

# Placeholder for TTS engine
ttsengine = None

# Check if this machine is running MACOS
IS_MACOS = (sys.platform == 'darwin')

# Use TTSX3 on MAC-OS regardless
USE_TTSX3_ALWAYS = False

USE_TTSX3 = USE_TTSX3_ALWAYS or not IS_MACOS

if USE_TTSX3_ALWAYS or not IS_MACOS:
    try:
        import pyttsx3
        ttsengine = pyttsx3.init()
    except AttributeError as e:
        raise OSError("TTS failed when importing TTSX3 - it has known issues on MacOS.") from e
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError("You'll need pyttsx3 to use TTS. Install using: pip install pyttsx3.") from e
    except Exception as e:
        raise RuntimeError("Issue when initialising TTS engine.") from e


def __say_with_ttsx3(message: str, wait = True) -> None:
    if ttsengine is None: raise ValueError("TTS engine was not initialised.")
    ttsengine.say(message)
    if wait: ttsengine.runAndWait()
    else: threading.Thread(target=lambda: ttsengine.runAndWait()).start()


def __say_with_macostts(message: str, wait = True) -> None:
    fn = lambda: os.system(f'say "{message}"')
    if wait: fn()
    else: threading.Thread(target=fn).start()    

# This is the one you'll use.
def say(message: str, wait = True) -> None:
    """Say a message using the configured TTS method"""
    if USE_TTSX3: __say_with_ttsx3(message, wait)
    else: __say_with_macostts(message, wait)
