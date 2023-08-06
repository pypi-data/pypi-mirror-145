import datetime
import enum
import typing
import urllib.parse
import warnings

import requests
import xmltodict

try:  # speedup
    import uvloop

    uvloop.install()
    import asyncio
except ModuleNotFoundError or ImportError:  # no uvloop
    import asyncio
try:
    import aiohttp

    aiohttp_exists = True
except ImportError or ModuleNotFoundError:
    aiohttp_exists = False


class VLC_State(enum.Enum):
    playing = "playing"
    paused = "paused"
    stopped = "stopped"


class VLC:
    """
    VLC manager class
    """

    def __init__(
        self,
        url: str = "http://localhost:8080",
        auth: typing.Union[
            tuple, requests.auth.HTTPBasicAuth, list, set
        ] = requests.auth.HTTPBasicAuth("", ""),
    ) -> None:
        """
        VLC Class
        This class will initialize a VLC instance by connect to it using REST API w/ HTTP Basic Auth.
        This class is blocking.
        If you want to use asynchornous version please install
        `aiohttp <https://pypi.org/project/aiohttp/>`_
        :param url: VLC url
        :param auth: VLC auth
        :return: None
        """
        self.url = url
        if isinstance(auth, (tuple, list, set)):
            if len(auth) != 2:
                raise ValueError(
                    "Auth must be a tuple or list of 2 elements which is username and password"
                )
            self.auth = requests.auth.HTTPBasicAuth(*auth)
        else:
            self.auth = auth
        if not self.connectable:
            raise Exception("VLC is not running or REST API is not enabled")
        self.full_screen = self.is_fullscreen
        self.volume_percentage = False

    def __encode_uri(self, url: str) -> bool:
        return urllib.parse.quote(url)

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __getattr__(self, name):
        if name not in self.__dict__:
            warnings.warn(
                "Attribute '{}' is not defined in VLC class or not yet implemented".format(
                    name
                ),
                UserWarning,
            )
            return (None,)

    @property
    def is_playing(self):
        """
        Check if VLC is playing or not
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_status", auth=self.auth
            )
            == 200
        )

    @property
    def status(self) -> dict:
        """
        Show the status & configurations inform of a dictionaries
        :return: dict
        """
        return xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text,
        )

    @property
    def playlist(self) -> dict:
        """
        Show the playlist and configurations inform of a dictionaries
        :return: dict
        """
        return xmltodict.parse(
            requests.get(self.url + "/requests/playlist.xml", auth=self.auth).text
        )

    @property
    def connectable(self) -> bool:
        """
        Check if VLC REST API is running
        :return: bool
        """
        try:
            return (
                requests.get(
                    self.url + "/requests/status.xml", auth=self.auth
                ).status_code
                == 200
            )
        except requests.exceptions.ConnectionError:
            return False

    def stop(self) -> bool:
        """
        Stop the current playing media and return back the boolean of the result
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_stop", auth=self.auth
            ).status_code
            == 200
        )

    def clear_playlist(self) -> bool:
        """
        Clear the playlist and return back the boolean of the result
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_empty", auth=self.auth
            ).status_code
            == 200
        )

    def play(self, uri: str) -> bool:
        """
        Play a media by uri and return back the boolean of the result if success or not
        :param uri: media uri
        :return: bool
        """
        uri = self.__encode_uri(uri)
        return (
            requests.get(
                self.url + "/requests/status.xml?command=in_play&input=" + uri,
                auth=self.auth,
            ).status_code
            == 200
        )

    def append_queue(self, uri: str) -> bool:
        """
        Append a media to the queue and return back the boolean of the result if success or not
        :param uri: media uri
        :return: bool
        """
        uri = self.__encode_uri(uri)
        return (
            requests.get(
                self.url + "/requests/status.xml?command=in_enqueue&input=" + uri,
                auth=self.auth,
            ).status_code
            == 200
        )

    def set_volume(self, volume: int, percent: bool = False) -> bool:
        """
        Set the volume of VLC and return back the boolean of the result if success or not
        :param volume: volume value (0-512 = 0-200%)
        :param percent: option for volume is actually percentage or not
        :return: bool
        """
        if percent:
            volume = int(volume * 2.56)
        return (
            requests.get(
                self.url + "/requests/status.xml?command=volume&val=" + str(volume),
                auth=self.auth,
            ).status_code
            == 200
        )

    def set_random(self, random: bool) -> bool:
        """
        Set the shuffle state of VLC and return back the boolean of the result if success or not
        :param random: random state
        :return: bool
        """

        return (
            requests.get(
                self.url
                + "/requests/status.xml?command=pl_random&state="
                + str(random),
                auth=self.auth,
            ).status_code
            == 200
        )

    @property
    def is_random(self) -> bool:
        """
        A property to get the random state of VLC
        :return: bool
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return True if content["root"]["random"] in ("true", "1") else False

    def set_repeat_media(self, repeat: bool) -> bool:
        """
        Set the repeat state of VLC and return back the boolean of the result if success or not
        :param repeat: repeat state
        :return: bool
        """
        return (
            requests.get(
                self.url
                + "/requests/status.xml?command=pl_repeat&state="
                + str(repeat),
                auth=self.auth,
            ).status_code
            == 200
        )

    @property
    def is_repeat_media(self) -> bool:
        """
        A property to get the repeat state of VLC
        :return: bool
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return True if content["root"]["repeat"] in ("true", "1") else False

    def set_loop_queue(self, loop: bool) -> bool:
        """
        Set the loop state of VLC and return back the boolean of the result if success or not
        :param loop: loop state
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_loop&state=" + str(loop),
                auth=self.auth,
            ).status_code
            == 200
        )

    @property
    def is_loop_queue(self) -> bool:
        """
        A property to get the loop state of VLC
        :return: bool
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return True if content["root"]["loop"] in ("true", "1") else False

    def fullscreen(self) -> list:
        """
        Set the fullscreen state of VLC and return back the boolean of the result if success or not and the current state of the screen
        :return: bool, bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=fullscreen", auth=self.auth
            ).status_code
            == 200,
            self.is_fullscreen,
        )

    @property
    def is_fullscreen(self) -> bool:

        """
        Return the current state of VLC if VLC is in fullscreen returns true otherwise false
        :return: bool
        """

        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return True if content["root"]["fullscreen"] in ("true", "1") else False

    def set_subtitle_file(self, uri: str) -> bool:
        """
        Set the subtitle file to show in the VLC and returns bool based on successful or not
        :return: bool
        """
        uri = self.__encode_uri(uri)
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_enqueue&input=" + uri,
                auth=self.auth,
            ).status_code
            == 200
        )

    def browse(self, uri: str) -> dict:
        """
        Give the list of the files and return the dictionaries of XML
        :return: dict
        """
        uri = self.__encode_uri(uri)
        return xmltodict.parse(
            requests.get(self.url + "/requests/browse.xml?uri=" + uri).text
        )

    def previous(self) -> bool:
        """
        Revert to previous media and return if request was successful or not
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_previous", auth=self.auth
            ).status_code
            == 200
        )

    def delete(self, uri: str) -> bool:
        """
        Delete media off the playlist by finding with the specified URI. Returns bool indicate if request was successful or not
        """
        uri = self.__encode_uri(uri)
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_delete&id=" + uri,
                auth=self.auth,
            ).status_code
            == 200
        )

    def next(self) -> bool:
        """
        Skip to next media and return if request was successful or not
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_next", auth=self.auth
            ).status_code
            == 200
        )

    def clear_history(self) -> bool:
        """
        Clear the histories. Returns boolean indicate request is successful or not
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_history&val=clear",
                auth=self.auth,
            ).status_code
            == 200
        )

    def pause(self) -> bool:
        """
        Pause the media playback. Returns bool indicate request was successful or not
        :return: bool
        """
        return (
            requests.get(
                self.url + "/requests/status.xml?command=pl_pause", auth=self.auth
            ).status_code
            == 200
        )

    @property
    def is_paused(self) -> bool:
        """
        Check if the media is actually paused or not. Returns bool indicate media is paused or not
        :return: bool
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return True if content["root"]["state"] in ("paused", "stopped") else False

    def seek(self, time: typing.Union[str, datetime.timedelta, int]) -> bool:
        """
        Seeking between time in the media with required arg is time which is supported int,str and datetime.timedelta. Returns bool indicate requests was successful or not
        :return: bool
        """
        if isinstance(time, datetime.timedelta):
            time = time.total_seconds()
        return (
            requests.get(
                self.url + "/requests/status.xml?command=seek&val=" + str(time),
                auth=self.auth,
            ).status_code
            == 200
        )

    @property
    def time(self) -> int:
        """
        Give the current time media is at (Unit seconds)
        :return: int, str
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return content["root"]["time"]

    @property
    def duration(self) -> float:
        """
        Give how long media is. (Unit seconds)
        :return: int, str
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return content["root"]["length"]

    @property
    def position(self) -> float:
        """
        Get current bar position (0,1)
        :return: float, str
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return content["root"]["position"]

    @property
    def state(self) -> VLC_State:
        """
        Give current state of the playback.
        :return: str
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        return VLC_State(content["root"]["state"])

    @property
    def volume(self) -> typing.Union[int, float]:
        """
        Get current playback's volume (0-512)
        :return: int
        """
        content = xmltodict.parse(
            requests.get(self.url + "/requests/status.xml", auth=self.auth).text
        )
        if self.volume_percentage:
            return float(content["root"]["volume"] / 2.56)
        else:
            return int(content["root"]["volume"])


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not aiohttp_exists:
    warnings.warn(
        "aiohttp is not installed, so you can't use the async version of this library",
        RuntimeWarning,
    )

    class Async_VLC:
        def __init__(self, *args) -> bool:
            raise ImportError("No aiohttp exists")

        def __getattr__(cls, name) -> bool:
            raise ImportError("No aiohttp exists")

    class aiohttp_wrap:
        def __init__(self, *args) -> bool:
            raise ImportError("No aiohttp exists")

        def __getattr__(cls, name) -> bool:
            raise ImportError("No aiohttp exists")

else:

    class dummy:
        pass

    class aiohttp_wrap:
        async def get(self, *args, **kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.get(*args, **kwargs) as response:
                    d = dummy()
                    d.status = response.status
                    d.status_code = response.status
                    d.text = await response.text()
            return d

        async def post(self, *args, **kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.post(*args, **kwargs) as response:
                    d = dummy()
                    d.status = response.status
                    d.status_code = response.status
                    d.text = await response.text()
            return d

        async def put(self, *args, **kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.put(*args, **kwargs) as response:
                    d = dummy()
                    d.status = response.status
                    d.status_code = response.status
                    d.text = await response.text()
            return d

        async def patch(self, *args, **kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.patch(*args, **kwargs) as response:
                    d = dummy()
                    d.status = response.status
                    d.status_code = response.status
                    d.text = await response.text()
            return d

        async def delete(self, *args, **kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.delete(*args, **kwargs) as response:
                    d = dummy()
                    d.status = response.status
                    d.status_code = response.status
                    d.text = await response.text()
            return d

    aiohttp_wrap = aiohttp_wrap()

    class Async_VLC:
        def __init__(
            self,
            url: str = "http://localhost:8080",
            auth: typing.Union[aiohttp.BasicAuth, tuple, set, list] = aiohttp.BasicAuth(
                "", ""
            ),
        ) -> None:
            """
            VLC Class
            This class will initialize a VLC instance by connect to it using REST API w/ HTTP Basic Auth.
            This class is blocking.
            If you want to use asynchornous version please install
            `aiohttp <https://pypi.org/project/aiohttp/>`_
            :param url: VLC url
            :param auth: VLC auth
            :return: None
            """
            self.url = url
            if isinstance(auth, (tuple, set, list)):
                if len(auth) != 2:
                    raise ValueError(
                        "Auth must be tuple or list of length 2 which is username and password"
                    )
                self.auth = aiohttp.BasicAuth(*auth)
            if not self.connectable:
                raise Exception("VLC is not running or REST API is not enabled")
            self.full_screen = self.is_fullscreen

        def __encode_uri(self, url: str) -> bool:
            return urllib.parse.quote(url)

        def __set_name__(self, owner, name):
            self.name = "_" + name

        @property
        def status(self) -> dict:
            """
            Show the status & configurations inform of a dictionaries
            :return: dict
            """
            return xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text,
            )

        @property
        def playlist(self) -> dict:
            """
            Show the playlist and configurations inform of a dictionaries
            :return: dict
            """
            return xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(
                        self.url + "/requests/playlist.xml", auth=self.auth
                    )
                ).text
            )

        @property
        def connectable(self) -> bool:
            """
            Check if VLC REST API is running
            :return: bool
            """
            try:
                return (
                    asyncio.run(
                        aiohttp_wrap.get(
                            self.url + "/requests/status.xml", auth=self.auth
                        )
                    ).status_code
                    == 200
                )
            except aiohttp.client_exceptions.ClientConnectorError:
                return False

        async def stop(self) -> bool:
            """
            Stop the current playing media and return back the boolean of the result
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_stop", auth=self.auth
            )
            return d.status_code == 200

        async def clear_playlist(self) -> bool:
            """
            Clear the playlist and return back the boolean of the result
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_empty", auth=self.auth
            )
            return d.status_code == 200

        async def play(self, uri: str) -> bool:
            """
            Play a media by uri and return back the boolean of the result if success or not
            :param uri: media uri
            :return: bool
            """
            uri = self.__encode_uri(uri)
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=in_play&input=" + uri,
                auth=self.auth,
            )
            return d.status_code == 200

        async def append_queue(self, uri: str) -> bool:
            """
            Append a media to the queue and return back the boolean of the result if success or not
            :param uri: media uri
            :return: bool
            """
            uri = self.__encode_uri(uri)
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=in_enqueue&input=" + uri,
                auth=self.auth,
            )
            return d.status_code == 200

        async def set_volume(self, volume: int, percent: bool = False) -> bool:
            """
            Set the volume of VLC and return back the boolean of the result if success or not
            :param volume: volume value (0-512 = 0-200%)
            :param percent: option for volume is actually percentage or not
            :return: bool
            """
            if percent:
                volume = int(volume * 2.56)
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=volume&val=" + str(volume),
                auth=self.auth,
            )
            return d.status_code == 200

        async def set_random(self, random: bool) -> bool:
            """
            Set the shuffle state of VLC and return back the boolean of the result if success or not
            :param random: random state
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url
                + "/requests/status.xml?command=pl_random&state="
                + str(random).lower(),
                auth=self.auth,
            )
            return d.status_code == 200

        @property
        def is_random(self) -> bool:
            """
            A property to get the random state of VLC
            :return: bool
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return True if content["root"]["random"] in ("true", "1") else False

        async def set_repeat_media(self, repeat: bool) -> bool:
            """
            Set the repeat state of VLC and return back the boolean of the result if success or not
            :param repeat: repeat state
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url
                + "/requests/status.xml?command=pl_repeat&state="
                + str(repeat).lower(),
                auth=self.auth,
            )
            return d.status_code == 200

        @property
        def is_repeat_media(self) -> bool:
            """
            A property to get the repeat state of VLC
            :return: bool
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return True if content["root"]["repeat"] in ("true", "1") else False

        async def set_loop_queue(self, loop: bool) -> bool:
            """
            Set the loop state of VLC and return back the boolean of the result if success or not
            :param loop: loop state
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url
                + "/requests/status.xml?command=pl_loop&state="
                + str(loop).lower(),
                auth=self.auth,
            )
            return d.status_code == 200

        @property
        def is_loop_queue(self) -> bool:
            """
            A property to get the loop state of VLC
            :return: bool
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return True if content["root"]["loop"] in ("true", "1") else False

        async def fullscreen(self) -> bool:
            """
            Set the fullscreen state of VLC and return back the boolean of the result if success or not and the current state of the screen
            :return: bool, bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=fullscreen", auth=self.auth
            )
            return (
                d.status_code == 200,
                self.is_fullscreen,
            )

        @property
        def is_fullscreen(self) -> bool:

            """
            Return the current state of VLC if VLC is in fullscreen returns true otherwise false
            :return: bool
            """

            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return True if content["root"]["fullscreen"] in ("true", "1") else False

        async def set_subtitle_file(self, uri: str) -> bool:
            """
            Set the subtitle file to show in the VLC and returns bool based on successful or not
            :return: bool
            """
            uri = self.__encode_uri(uri)
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_enqueue&input=" + uri,
                auth=self.auth,
            )
            return d.status_code == 200

        async def browse(self, uri: str) -> dict:
            """
            Give the list of the files and return the dictionaries of XML
            :return: dict
            """
            uri = self.__encode_uri(uri)
            d = await aiohttp_wrap.get(self.url + "/requests/browse.xml?uri=" + uri)
            return xmltodict.parse(d.text)

        async def previous(self) -> bool:
            """
            Revert to previous media and return if request was successful or not
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_previous",
                auth=self.auth,
            )
            return d.status_code == 200

        async def delete(self, uri: str) -> bool:
            """
            Delete media off the playlist by finding with the specified URI. Returns bool indicate if request was successful or not
            """
            uri = self.__encode_uri(uri)
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_delete&id=" + uri,
                auth=self.auth,
            )
            return d.status_code == 200

        async def next(self) -> bool:
            """
            Skip to next media and return if request was successful or not
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_next", auth=self.auth
            )
            return d.status_code == 200

        async def clear_history(self) -> bool:
            """
            Clear the histories. Returns boolean indicate request is successful or not
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_history&val=clear",
                auth=self.auth,
            )
            return d.status_code == 200

        async def pause(self) -> bool:
            """
            Pause the media playback. Returns bool indicate request was successful or not
            :return: bool
            """
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=pl_pause", auth=self.auth
            )
            return d.status_code == 200

        @property
        def is_paused(self) -> bool:
            """
            Check if the media is actually paused or not. Returns bool indicate media is paused or not
            :return: bool
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return True if content["root"]["state"] in ("paused", "stopped") else False

        async def seek(self, time: typing.Union[str, datetime.timedelta, int]) -> bool:
            """
            Seeking between time in the media with required arg is time which is supported int,str and datetime.timedelta. Returns bool indicate requests was successful or not
            :return: bool
            """
            if isinstance(time, datetime.timedelta):
                time = time.total_seconds()
            d = await aiohttp_wrap.get(
                self.url + "/requests/status.xml?command=seek&val=" + str(time),
                auth=self.auth,
            )
            return d.status_code == 200

        @property
        def time(self) -> int:
            """
            Give the current time media is at (Unit seconds)
            :return: int, str
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return content["root"]["time"]

        @property
        def duration(self) -> float:
            """
            Give how long media is. (Unit seconds)
            :return: int, str
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return content["root"]["length"]

        @property
        def position(self) -> float:
            """
            Get current bar position (0,1)
            :return: float, str
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return content["root"]["position"]

        @property
        def state(self) -> VLC_State:
            """
            Give current state of the playback.
            :return: str
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            return VLC_State(content["root"]["state"])

        @property
        def volume(self) -> typing.Union[int, float]:
            """
            Get current playback's volume (0-512)
            :return: int
            """

            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                ).text
            )
            if self.volume_percentage:
                return float(content["root"]["volume"] / 2.56)
            else:
                return int(content["root"]["volume"])

        @property
        def is_playing(self):
            """
            Check if VLC is playing or not
            :return: bool
            """
            content = xmltodict.parse(
                asyncio.run(
                    aiohttp_wrap.get(self.url + "/requests/status.xml", auth=self.auth)
                )
            )
            return True if content["root"]["state"] in ("playing", "paused") else False
