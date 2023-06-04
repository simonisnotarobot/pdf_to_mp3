from pdfminer.high_level import extract_text
from google.cloud import texttospeech

# CONVERTS PDF FILE TEXT TO AUDIO (MP3)
# USES GOOGLE CLOUD TEXT-TO-SPEECH https://cloud.google.com/text-to-speech/docs/basics


def synthesize_text_file(text_file):
    """Synthesizes speech from the input file of text."""
    client = texttospeech.TextToSpeechClient()

    with open(text_file) as f:
        text = f.read()
        input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(f"{text_file.split('.')[0]}.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f'\nAudio content written to file {text_file.split(".")[0]}.mp3')


def pdf_text_to_file(pdf_file):
    text = extract_text(pdf_file)
    # remove form feed
    text = text.replace('\x0c', '')
    filename = f'{pdf_file.split(".")[0]}.txt'
    with open(filename, 'w') as text_file:
        text_file.write(text)
    return filename


def ask_for_pdf():
    pdf = input('Please enter the path to the PDF file to convert to audio: ')
    try:
        with open(pdf) as file:
            file.read()
            return pdf
    except FileNotFoundError:
        print(f'\nCan\'t locate PDF file: {pdf}\nPlease try again\n')
        ask_for_pdf()


pdf_file = ask_for_pdf()
synthesize_text_file(pdf_text_to_file(pdf_file))

