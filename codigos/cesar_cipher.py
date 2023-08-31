import sys

def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            elif char.isupper():
                encrypted_text += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar_cipher.py <texto> <corrimiento>")
        sys.exit(1)
    
    text_to_encrypt = sys.argv[1]
    shift_amount = int(sys.argv[2])
    
    encrypted_text = caesar_cipher(text_to_encrypt, shift_amount)
    print("Texto cifrado:", encrypted_text)
