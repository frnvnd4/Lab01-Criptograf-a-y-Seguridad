import sys
import colorama
from colorama import Fore, Style
from scapy.all import rdpcap

colorama.init()

# Frecuencias de letras en español (tomadas de https://es.wikipedia.org/wiki/Frecuencia_de_letras)
spanish_letter_frequencies = {
    'a': 11.96, 'b': 2.22, 'c': 4.11, 'd': 5.16, 'e': 13.68,
    'f': 0.69, 'g': 1.01, 'h': 0.70, 'i': 6.25, 'j': 0.44,
    'k': 0.02, 'l': 4.97, 'm': 3.15, 'n': 6.71, 'o': 8.68,
    'p': 2.51, 'q': 0.88, 'r': 6.87, 's': 7.98, 't': 4.63,
    'u': 3.93, 'v': 1.18, 'w': 0.22, 'x': 0.22, 'y': 0.90, 'z': 0.52
}

def cesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted_index = (ord(char.lower()) - ord('a') - shift) % 26
            decrypted_char = chr(shifted_index + ord('a'))
            if char.isupper():
                decrypted_char = decrypted_char.upper()
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def evaluate_text_legibility(text):
    score = 0
    for char in text:
        if char.isalpha():
            score += spanish_letter_frequencies.get(char.lower(), 0)
    return score

def main():
    if len(sys.argv) != 2:
        print("Uso: python programa.py <nombre_archivo.pcapng>")
        return

    pcap_file = sys.argv[1]
    packets = rdpcap(pcap_file)

    extracted_chars = []

    for packet in packets:
        if packet.haslayer('ICMP'):
            icmp_payload = packet['ICMP'].load
            if len(icmp_payload) > 0:
                extracted_char = chr(icmp_payload[-1] & 0xFF)
                extracted_chars.append(extracted_char)

    encrypted_message = ''.join(extracted_chars)

    best_shift = None
    best_score = float('-inf')
    best_decrypted_message = ""

    all_decrypted_messages = []  # Almacenar todas las opciones para imprimir una sola vez

    for shift in range(1, 27):
        decrypted_message = cesar_decrypt(encrypted_message, shift)
        score = evaluate_text_legibility(decrypted_message)
        
        all_decrypted_messages.append((shift, decrypted_message, score))

        if score > best_score:
            best_score = score
            best_shift = shift
            best_decrypted_message = decrypted_message

    print("\nCombinaciones posibles:")
    for shift, decrypted_message, score in all_decrypted_messages:
        if shift == best_shift:
            print(Fore.GREEN +f"{shift:2}: {decrypted_message}"+ Style.RESET_ALL)
        else:
            print(f"{shift:2}: {decrypted_message}")

if __name__ == "__main__":
    main()

