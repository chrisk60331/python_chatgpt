import boto3


class TextToSpeech:
    def __init__(self):
        self.polly = boto3.client("polly", region_name="us-east-1")

    def create_audio_file(self, text, output_file):
        response = self.polly.synthesize_speech(
            Text=text, Engine="neural", OutputFormat="mp3", VoiceId="Salli"
        )

        with open(output_file, "wb") as file:
            file.write(response["AudioStream"].read())
