#!/usr/bin/env python3.12
"""
This module implements the Caesar Cipher encryption and decryption algorithm.
"""

import argparse
import string


class CaesarCipher:
    """
    This class implements the Caesar Cipher encryption and decryption algorithm.
    """

    def __init__(self) -> None:
        """
        Initializes the Caesar_Cipher object.

        The `chars` attribute is a list of uppercase letters of the English alphabet.
        """
        self.chars = list(string.ascii_uppercase)

    def __perform_caesar(self, text: str, key: int, enc: bool) -> str:
        """
        Performs the Caesar Cipher encryption or decryption on the given text.

        Args:
            text (str): The text to be encrypted or decrypted.
            key (int): The encryption or decryption key.
            enc (bool): A flag indicating whether to perform encryption (True) or decryption (False).

        Returns:
            str: The encrypted or decrypted text.
        """
        decrypted_text = ""

        for char in text:
            if char.upper() in self.chars:
                decrypted_char = self.__rotate(char, key, enc)
                decrypted_text += decrypted_char if char.isupper() else decrypted_char.lower()
            else:
                decrypted_text += char

        return decrypted_text

    def __rotate(self, char: str, key: int, forward: bool) -> str:
        """
        Rotates the given character by the specified key.

        Args:
            char (str): The character to be rotated.
            key (int): The rotation key.
            forward (bool): A flag indicating whether to rotate forward (True) or backward (False).

        Returns:
            str: The rotated character.
        """
        action = lambda a, b, c: a + b if c else a - b
        idx = action(self.chars.index(char.upper()), key, forward)
        return self.chars[idx % len(self.chars)]

    def encrypt(self, text: str, key: int) -> str:
        """
        Encrypts the given text using the Caesar Cipher algorithm.

        Args:
            text (str): The text to be encrypted.
            key (int): The encryption key.

        Returns:
            str: The encrypted text.
        """
        return self.__perform_caesar(text, key, True)

    def decrypt(self, text: str, key: int) -> str:
        """
        Decrypts the given text using the Caesar Cipher algorithm.

        Args:
            text (str): The text to be decrypted.
            key (int): The decryption key.

        Returns:
            str: The decrypted text.
        """
        return self.__perform_caesar(text, key, False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Caesar Cipher")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the given text")
    group.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the given text")
    parser.add_argument("key", type=int, help="The encryption or decryption key")
    parser.add_argument("string", type=str, nargs='+', help="The text to be encrypted or decrypted")

    args = parser.parse_args()

    cipher = CaesarCipher()
    if args.key not in range(1, 25):
        raise ValueError("The key must be between 1 and 25, inclusive.")

    if args.encrypt:
        print(cipher.encrypt(' '.join(args.string), args.key))
    elif args.decrypt:
        print(cipher.decrypt(' '.join(args.string), args.key))
