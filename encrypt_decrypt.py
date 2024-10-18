class Htet_Encryption:
    def start_encryption(self, plain_text, key):
        encrypted_text = ""
        key_length = len(key)

        for i in range(len(plain_text)):
            # Get the shift from the key character, cycling through the key
            shift = ord(key[i % key_length])  # ASCII value of key character
            # Shift the character
            encrypted_text += chr(ord(plain_text[i]) + shift)

        return encrypted_text

    def start_decryption(self, cipher_text, key):
        decrypted_text = ""
        key_length = len(key)

        for i in range(len(cipher_text)):
            # Get the shift from the key character, cycling through the key
            shift = ord(key[i % key_length])  # ASCII value of key character
            # Shift the character back
            decrypted_text += chr(ord(cipher_text[i]) - shift)

        return decrypted_text


# # Example usage:
# encryption = Htet_Encryption()
# key = "abc"  # Simple string key for encryption
# plain_text = "Hello, World!"
# cipher_text = encryption.start_encryption(plain_text, key)
# print("Encrypted:", cipher_text)
#
# decrypted_text = encryption.start_decryption(cipher_text, key)
# print("Decrypted:", decrypted_text)
