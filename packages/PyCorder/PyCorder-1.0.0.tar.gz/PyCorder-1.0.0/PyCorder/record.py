import wave
import pyaudio

class MicStream:
    def __init__(self, frame: list[bytes], format: int, channels: int, rate: int, core: pyaudio.PyAudio):
        self.__frame = frame
        self.__channels = channels
        self.__rate = rate
        self.__core = core
        self.__format = format

    def save(self, name: str, suffix: str = None):
        with wave.open(f'{name}.{"wav" if not suffix else suffix}', 'wb') as wf:
            wf.setnchannels(self.__channels)
            wf.setsampwidth(self.__core.get_sample_size(self.__format))
            wf.setframerate(self.__rate)
            wf.writeframes(b''.join(self.__frame))

        wf.close()
        return None

class MicRecorder:
    def __init__(self, chunk: int = None, second: int = None, rate: int = None, channels: int = None):
        self.__chunk = 4096 if not chunk else chunk
        self.__second = second
        self.__channels = 1 if not channels else channels
        self.__rate = 44100 if not rate else rate
        self.__core = pyaudio.PyAudio()

    def record(self, format: int = None):
        format = pyaudio.paInt16 if not format else format
        stream = self.__core.open(
            format=format,
            channels=self.__channels,
            rate=self.__rate,
            input=True,
            frames_per_buffer=self.__chunk,
        )

        frames = []

        if not self.__second:
            try:
                while True:
                    data = stream.read(self.__chunk)
                    frames.append(data)
            except KeyboardInterrupt:
                pass

        stream.stop_stream()
        stream.close()
        self.__core.terminate()
        return MicStream(frames, format, self.__channels, self.__rate, self.__core)