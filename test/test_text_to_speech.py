import boto3
from unittest.mock import MagicMock, patch
from my_module import TextToSpeech


def test_create_audio_file():
    mock_response = {"AudioStream": MagicMock(), "ContentType": "audio/mpeg"}
    with patch.object(
        boto3.client("polly", region_name="us-east-1"),
        "synthesize_speech",
        return_value=mock_response,
    ) as mock_client:
        tts = TextToSpeech()
        tts.create_audio_file("Hello world!", "output.mp3")
        mock_client.assert_called_once_with(
            Text="Hello world!", OutputFormat="mp3", VoiceId="Joanna"
        )
