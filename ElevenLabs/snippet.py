import asyncio
import base64
import io
import re
import time
from collections import deque
from typing import Optional

import azure.cognitiveservices.speech as speechsdk
import soundfile as sf
from server.utils.common import split_text
from server.config import get_settings, get_gpt_client, get_elevenlabs_client
from server.config.prompts import ELEVEN_LABS_EMOTION_TAG_PROMPT

settings = get_settings()
gpt_client = get_gpt_client()
elevenlabs_client = get_elevenlabs_client()


class TTSChunk:
    def __init__(self, text, is_final=False):
        self.text = re.sub(r"[\n\r\t]", "", text)
        self.audio_data = None
        self.speech_timing = None
        self.duration = None
        self.future = None
        self.animation_class= None
        self.is_final = is_final
        self.isWelcomeSpeech = False

    def to_dict(self):
        """Serialize the TTSChunk to a dictionary."""
        return {
            "text": self.text,
            "audio_data": self.audio_data,
            "speech_timing": self.speech_timing,
            "duration": self.duration,
            "animation_class": self.animation_class,
            "is_final": self.is_final,
            "isWelcomeSpeech" : self.isWelcomeSpeech
        }

    @classmethod
    def from_dict(cls, data):
        """Create a TTSChunk from serialized data."""
        chunk = cls(data["text"], is_final=data["is_final"])
        chunk.audio_data = data["audio_data"]
        chunk.speech_timing = data["speech_timing"]
        chunk.duration = data["duration"]
        chunk.animation_class = data["animation_class"]
        return chunk


class StreamingTTSService:
    def __init__(self, speech_key, speech_region, classifier_module=None):
        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )
        self.audio_queue = deque()
        self.remaining_text = ""
        self._available_duration = 0.0
        self.classifier_module = classifier_module
        self.text_chunks = []

    async def insert_text(
        self,
        text,
        is_final=False,
        style="empathetic",
        style_degree="1.0",
        language="de-DE",
        voice="de-DE-FlorianMultilingualNeural",
        volume="default",
        topic=None,
    ):
        """Insert text into the queue for synthesis"""
        if self.audio_queue:
            await asyncio.sleep(0.1)
        text = self.remaining_text + text
        chunks, self.remaining_text = self._split_text(text, is_final)
        nr_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            tts_chunk = TTSChunk(chunk, is_final=(is_final and i == nr_chunks - 1))
            self.text_chunks.append(chunk)
            # Create an asyncio task for each chunk to process in parallel
            tts_chunk.future = asyncio.create_task(  # type: ignore
                self._synthesize_chunk_async(
                    tts_chunk,
                    style,
                    style_degree,
                    language,
                    voice,
                    volume,
                    topic,
                    index=len(self.text_chunks) - 1,
                )
            )
            self.audio_queue.append(tts_chunk)
            print(f"Chunk added to queue: {chunk} - available duration: {self._available_duration:.2f}s")
        return len(self.audio_queue) > 0

    async def get_audio_chunk(self):
        """Get the next audio chunk from the queue that has been processed"""
        if not self.audio_queue:
            return None
        if self._available_duration < 0.1:
            await asyncio.sleep(0.25)
            return None

        # Check the first chunk in the queue
        chunk: TTSChunk = self.audio_queue[0]
        if chunk.future and chunk.future.done():
            # Remove the chunk from the queue before returning it
            self._available_duration -= chunk.duration or 0.0
            return self.audio_queue.popleft()
        return TTSChunk("")

    async def _synthesize_chunk_async(self, chunk: TTSChunk, style: str, style_degree:str, language: str, 
                                    voice: str, volume: str, topic: Optional[str], index: Optional[int] = None):
        """Asynchronously process a text chunk into audio and assigns corresponding animation class"""
        # Run the synchronous method in a thread pool to avoid blocking
        loop = asyncio.get_running_loop()
        tts_task = loop.run_in_executor(
            None, self._synthesize_chunk, chunk.text, style, style_degree, language, voice, volume, index
        )
        tasks = [tts_task]
        if self.classifier_module is not None:
            clf_task = loop.run_in_executor(
                None, self.classifier_module.classify_text, chunk.text, topic
            )
            tasks.append(clf_task)
        else:
            print("No classifier module assigned; skipping classification.")
        (audio_data, speech_timing, duration), animation_class = await asyncio.gather(*tasks)

        # for debugging
        mapping = self.classifier_module.class_to_key if self.classifier_module else {}
        anim_key = animation_class.animation_class if animation_class else None
        anim_class_name = next((k for k, v in mapping.items() if v == anim_key), "unknown") 
        print(f"Animation for chunk '{chunk.text}': {anim_class_name}")
        self._available_duration += duration or 0.0

        chunk.audio_data = audio_data  # type: ignore
        chunk.speech_timing = speech_timing  # type: ignore
        chunk.duration = duration
        chunk.animation_class = animation_class
        return chunk

    def _synthesize_chunk(
        self,
        text,
        voice_id="EkK5I93UQWFDigLMpZcX",
        index: Optional[int] = None
    ):
        """Convert text to speech using Azure TTS"""
        if not text:
            return None, None, None

        start_time = time.time()

        try:
            response = gpt_client.chat.completions.create(
                model=settings.MODEL_EMOTION_TAG_ADDER,
                max_tokens=500,
                temperature=0.9,
                timeout=None,
                messages=[
                    {"role": "system", "content": ELEVEN_LABS_EMOTION_TAG_PROMPT},
                    {"role": "user", "content": text},
                ]
            )
            text_with_emotion = response.choices[0].message.content
            print(f"Emotion tagger response: {text_with_emotion}")
            print(f"Index of chunk: {index}")
            if index is not None and index > 0:
                previous_text = self.text_chunks[index - 1]
                print(f"Previous text for context: {previous_text}")

            # Retry logic up to 3 attempts
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    # result = synthesizer.speak_ssml(ssml=ssml)
                    previous_text = None
                    if index is not None and index > 0:
                        previous_text = self.text_chunks[index - 1]
                    audio_iter = elevenlabs_client.text_to_speech.convert(
                        text=text_with_emotion,
                        voice_id=voice_id,
                        model_id="eleven_multilingual_v2",
                        previous_text= self.text_chunks[index - 1] if index and index > 0 else None
                    )
                except Exception as e:
                    print(f"TTS attempt {attempt} exception: {e}")
                    if attempt == max_retries:
                        print("Max retries reached; failing synthesis.")
                        return None, None, None
                    continue
                
                data = base64.b64encode(audio_iter).decode("utf-8")
                print("Audio data encoded to base64.")

                # Get audio duration
                wav_io = io.BytesIO(wav_data)
                audio, samplerate = sf.read(wav_io)
                duration = len(audio) / samplerate
                print(f"Audio duration: {duration} seconds")

                speech_timing = time.time() - start_time
                print(f"Speech synthesis took {speech_timing:.2f} seconds")
                return data, speech_timing, duration
        except RuntimeError as e:
            print(f"TTS error: {e}")
            return None, None, None

    def _split_text(self, text: str, is_final=False):
        return split_text(text, self._available_duration, is_final)


async def main():
    from server.config.keys import keys
    from server.utils.audio import play_audio

    service = StreamingTTSService(keys["SPEECH_KEY"], keys["SPEECH_REGION"])
    await service.insert_text(
        """The tiger (Panthera tigris) is a large cat and a member of """,
        is_final=False,
    )
    await service.insert_text(
        """the genus Panthera native to Asia. """,
        is_final=False,
    )
    await service.insert_text(
        """It has a powerful, muscular body with a large head and paws, a long tail and orange fur with black, 
    mostly vertical stripes. It is traditionally classified into nine recent subspecies, 
    though some recognise only two subspecies, mainland Asian tigers and the island tigers of the Sunda Islands.""",
        is_final=True,
    )
    # Process chunks as they become available

    start_time = time.time()
    while True:
        chunk = await service.get_audio_chunk()
        if chunk and chunk.audio_data:
            end_time = time.time()
            time_chunk = end_time - start_time
            print(f"Time to first chunk: {time_chunk} seconds")
            print(f"Got chunk with text: {chunk.text}")
            print(f"Duration: {chunk.duration}s")
            play_audio(chunk.audio_data)
            # Process the audio data here
            # chunk.audio_data contains the base64-encoded audio
        else:
            # No chunks ready yet, wait a moment
            await asyncio.sleep(0.1)
        if chunk and chunk.is_final:
            break


if __name__ == "__main__":
    asyncio.run(main())
