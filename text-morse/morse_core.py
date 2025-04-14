from morse import MORSE_CODE_DICT
import time
import winsound

TEXT_CODE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}


class MorseTranslator:
    @staticmethod
    def text_to_morse(text):
        """Convert text to Morse code"""
        morse_code = []
        for char in text.upper():
            if char in MORSE_CODE_DICT:
                morse_code.append(MORSE_CODE_DICT[char])
            elif char == ' ':
                morse_code.append('/')
            else:
                morse_code.append(' ')
        return ' '.join(morse_code)

    @staticmethod
    def morse_to_text(morse_code):
        """Convert Morse code to text"""
        if not morse_code.strip():
            return ""

        morse_code = ' '.join(morse_code.split())
        decoded_text = []
        words = morse_code.split('/')

        for word in words:
            decoded_word = []
            letters = word.strip().split(' ')

            for letter in letters:
                try:
                    decoded_word.append(TEXT_CODE_DICT[letter])
                except KeyError:
                    decoded_word.append('�')

            decoded_text.append(''.join(decoded_word))

        return ' '.join(decoded_text).capitalize()


class MorsePlayer:
    @staticmethod
    def play_morse_code(morse_code, dot_duration=100, frequency=1000):
        """Play Morse code as sound"""
        for symbol in morse_code:
            if symbol == '.':
                winsound.Beep(frequency, dot_duration)
            elif symbol == '-':
                winsound.Beep(frequency, dot_duration * 3)
            elif symbol == ' ':
                time.sleep(dot_duration / 1000 * 3)
            time.sleep(dot_duration / 1000)
