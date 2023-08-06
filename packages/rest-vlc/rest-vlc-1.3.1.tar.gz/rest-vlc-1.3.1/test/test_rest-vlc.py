from dotenv import load_dotenv

load_dotenv()
import os
import sys
import time

import pytest

sys.path.append("..")  # pytest problem?
import rest_vlc

vlc = rest_vlc.VLC(auth=("", os.environ["VLC_PASSWORD"]))


@pytest.fixture
def x():
    pass


def test_low_volume():
    assert vlc.set_volume(0), "Failed to set volume to 0"


def test_up_volume():
    assert vlc.set_volume(256), "Failed to set volume to 100"


def test_pause():
    assert vlc.pause(), "Failed to pause"


def test_stop():
    assert vlc.stop(), "Failed to stop"


def test_clear_playlist():
    assert vlc.clear_playlist(), "Failed to clear playlist"


def test_play():
    assert vlc.play(os.environ["VLC_URI"]), "Failed to play"


def test_append():
    assert vlc.append_queue(os.environ["VLC_URI2"]), "Failed to append"


def test_random():
    assert vlc.set_random(True), "Failed to set random"
    assert vlc.is_random, "Failed to set random"


def test_repeat():
    assert vlc.set_repeat_media(True), "Failed to set repeat"
    assert vlc.is_repeat_media, "Failed to set repeat"


def test_loop():
    assert vlc.set_loop_queue(True), "Failed to set loop"
    assert vlc.is_loop_queue, "Failed to set loop"


def test_fullscreen():
    assert vlc.fullscreen(), "Failed to set fullscreen"
    assert vlc.is_fullscreen, "Failed to set fullscreen"
    assert vlc.fullscreen(), "Failed to set fullscreen"  # revert
    assert not vlc.is_fullscreen, "Failed to set fullscreen"  # revert


def test_browse():
    assert vlc.browse(os.environ["VLC_FOLDER"]), "Failed to browse"


def test_previous():
    assert vlc.previous(), "Failed to previous"


def test_next():
    assert vlc.next(), "Failed to next"


def test_delete():
    assert vlc.delete(os.environ["VLC_URI"]), "Failed to delete"


def test_clear_history():
    assert vlc.clear_history(), "Failed to clear history"


def test_seeking():
    assert vlc.seek(69), "Failed to seek"
