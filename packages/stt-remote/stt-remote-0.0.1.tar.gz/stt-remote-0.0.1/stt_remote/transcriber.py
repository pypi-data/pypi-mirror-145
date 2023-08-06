import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests_futures.sessions import FuturesSession
from tqdm import tqdm


class Transcriber:
    """
    Single file transcription and batched transcription of audio files.

        transcriber = Transcriber("https://stt.coqui.ai/...")
        transcript = transcriber.transcribe_one("audio_file.wav")
        print(f"Transcript: {transcript}")

        from glob import glob
        audio_files = glob.glob("audio/*.wav")
        samples = transcriber.transcribe_many(audio_files)
        for file_path, transcript in samples:
            print(f"{file_path}: {transcript}")
    """

    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    @staticmethod
    def _read_wav(audio_path):
        with open(audio_path, "rb") as fin:
            return fin.read()

    def _get_transcript(self, session, audio_path):
        wavcontents = self._read_wav(audio_path)
        future = session.post(
            self.endpoint_url,
            data=wavcontents,
            headers={"Content-Type": "application/octet-stream"},
        )
        future.audio_path = audio_path
        return future

    def transcribe_many(self, audio_path_list, worker_count=8):
        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=worker_count))
        futures = [self._get_transcript(session, path) for path in audio_path_list]
        samples = []
        for result in tqdm(as_completed(futures)):
            audio_path = result.audio_path
            try:
                transcript = result.result().json()["transcript"]
            except requests.exceptions.RequestException as exc:
                print(f"Couldn't transcribe {audio_path}: {exc}")
            samples.append((audio_path, transcript))
        return samples

    def transcribe_one(self, audio_path):
        wavcontents = self._read_wav(audio_path)
        res = requests.post(
            self.endpoint_url,
            data=wavcontents,
            headers={"Content-Type": "application/octet-stream"},
        )
        return res.json()["transcript"]


def main():
    transcriber = Transcriber(sys.argv[1])
    if len(sys.argv) > 2:
        samples = transcriber.transcribe_many(sys.argv[2:])
        for audio_path, transcript in samples:
            print(f"{audio_path}: {transcript}")
    else:
        print(transcriber.transcribe_one(sys.argv[2]))


if __name__ == "__main__":
    main()
