# Nødvendige biblioteker
import unittest
import random
import string
import requests
from MorseCodePy import encode

# Den kode, der skal testes
import morse

class TestDictionary(unittest.TestCase):
    def testMorseCode(self):
        # Kontroller korrekt type
        self.assertIsInstance(morse.morseCode, dict)

        # Kontroller at alle keys er enten tal eller bogstaver
        for e in morse.morseCode.keys():
            self.assertTrue(e.isalpha() or e.isdigit() or e in ' .,;:?!-/', msg='Testen er fejlet ved: ' + e)

        # Kontroller at alle values er morsetegn
        for e in morse.morseCode.values():
            self.assertTrue('.' in e or '-' in e or e == '')
            self.assertFalse(e.isalpha())

class TestTranslateStringToMorse(unittest.TestCase):
    def testTranslateCharacter(self):
        char = random.choice(string.ascii_letters)
        reference = encode(char, language='english')
        subject = morse.translate(char, morse.morseCode).upper()
        self.assertEqual(reference, subject)

    def testTranslateText(self):
        req = requests.get('https://loripsum.net/api/1/short/plaintext')
        text = None
        if req.status_code == 200:
            text = req.text.strip()
        reference = encode(text, language='english')
        reference = reference.replace(' / ', '//')
        reference = reference.replace(' ', '/')
        reference = reference + '//'

        subject = morse.encodeMessage(text, morse.morseCode).upper()
        self.assertEqual(reference, subject)

class TestTranslateMorseToString(unittest.TestCase):
    def testTranslateCharacter(self):
        reference = random.choice(string.ascii_letters).upper()
        morse_char = encode(reference, language='english')
        subject = morse.translate(morse_char, morse.morseCodeReverse).upper()
        self.assertEqual(reference, subject)

    def testTranslateText(self):
        req = requests.get('https://loripsum.net/api/1/short/plaintext')
        reference = None
        if req.status_code == 200:
            reference = req.text.strip().upper()
        message = encode(reference, language='english')
        message = message.replace(' / ', '//')
        message = message.replace(' ', '/')

        subject = morse.decodeMessage(message, morse.morseCodeReverse).upper()
        self.assertEqual(reference, subject)

if __name__ == '__main__':
    unittest.main()
