import math
import secrets
from collections import Counter
import base64
import hashlib

DEFAULT_REDUNDANCY_OPTIONS = [2, 3, 4]
DUMMY_PROBABILITY = 0.4
ENABLE_INTEGRITY_CHECK = True

# Multi-Byte Konvertierung
BYTE_LENGTH = 16  # 128 Bit Startoffset

def int_to_bytes(value, length=BYTE_LENGTH):
    return list(value.to_bytes(length, byteorder='big'))

def bytes_to_int(byte_list):
    return int.from_bytes(byte_list, byteorder='big')

# Komplexe Konstante
def get_complex_constants_digits(n):
    pi = str(math.pi).replace('.', '')
    e = str(math.e).replace('.', '')
    phi = str((1 + math.sqrt(5)) / 2).replace('.', '')

    combined = ''.join(p + e_digit + phi_digit for p, e_digit, phi_digit in zip(pi, e, phi))
    while len(combined) < n:
        combined += combined

    return [int(d) for d in combined[:n]]

def text_to_numbers(text):
    return [ord(char) for char in text]

def numbers_to_text(numbers):
    return ''.join(chr(num) for num in numbers)

def numbers_to_bytes(numbers):
    return bytes(numbers)

def bytes_to_numbers(b):
    return list(b)

def calculate_message_hash(message):
    return list(hashlib.sha256(message.encode()).digest()[:4])

def create_real_group(char_value, offset, pi_digits, redundancy_level, multiplier, adder):
    group = []
    current_offset = offset
    for _ in range(redundancy_level):
        pi_value = pi_digits[current_offset % len(pi_digits)]
        encrypted = (char_value + pi_value) % 256
        group.append(encrypted)
        current_offset = (current_offset * multiplier + adder) % len(pi_digits)
    return group, current_offset

def create_dummy_group(pi_digits, redundancy_level, multiplier, adder):
    group = []
    dummy_offset = secrets.randbelow(len(pi_digits))
    for _ in range(redundancy_level):
        dummy_value = secrets.randbelow(256)
        pi_value = pi_digits[dummy_offset % len(pi_digits)]
        encrypted = (dummy_value + pi_value) % 256
        group.append(encrypted)
        dummy_offset = (dummy_offset * multiplier + adder) % len(pi_digits)
    return group

def encrypt(text):
    numbers = text_to_numbers(text)
    pi_digits = get_complex_constants_digits(100000)

    start_offset = secrets.randbits(BYTE_LENGTH * 8)
    redundancy_level = secrets.choice(DEFAULT_REDUNDANCY_OPTIONS)
    multiplier = secrets.choice([13, 17, 19, 23])
    adder = secrets.choice([29, 31, 37, 41])

    offset = start_offset
    groups = []

    for number in numbers:
        real_group, offset = create_real_group(number, offset, pi_digits, redundancy_level, multiplier, adder)
        groups.append(real_group)

        if secrets.randbelow(100) / 100 < DUMMY_PROBABILITY:
            dummy_group = create_dummy_group(pi_digits, redundancy_level, multiplier, adder)
            groups.append(dummy_group)

    secrets.SystemRandom().shuffle(groups)

    flat_numbers = int_to_bytes(start_offset) + [redundancy_level, multiplier, adder]

    if ENABLE_INTEGRITY_CHECK:
        flat_numbers.extend(calculate_message_hash(text))

    flat_numbers += [num for group in groups for num in group]

    message_bytes = numbers_to_bytes(flat_numbers)
    encoded_message = base64.b64encode(message_bytes).decode('utf-8')
    return encoded_message

def decrypt(encoded_message):
    message_bytes = base64.b64decode(encoded_message)
    message = bytes_to_numbers(message_bytes)

    start_offset = bytes_to_int(message[:BYTE_LENGTH])
    redundancy_level = message[BYTE_LENGTH]
    multiplier = message[BYTE_LENGTH + 1]
    adder = message[BYTE_LENGTH + 2]

    hash_check = message[BYTE_LENGTH + 3: BYTE_LENGTH + 7] if ENABLE_INTEGRITY_CHECK else None
    data = message[BYTE_LENGTH + 7:] if ENABLE_INTEGRITY_CHECK else message[BYTE_LENGTH + 3:]

    pi_digits = get_complex_constants_digits(100000)
    groups = [data[i:i + redundancy_level] for i in range(0, len(data), redundancy_level)]

    offset = start_offset
    potential_numbers = []

    for group in groups:
        if len(group) < redundancy_level:
            continue

        decrypted_candidates = []
        current_offset = offset

        for encrypted_num in group:
            pi_value = pi_digits[current_offset % len(pi_digits)]
            original = (encrypted_num - pi_value) % 256
            decrypted_candidates.append(original)
            current_offset = (current_offset * multiplier + adder) % len(pi_digits)

        common = Counter(decrypted_candidates).most_common(1)
        if common[0][1] > 1:
            potential_numbers.append(common[0][0])
            offset = current_offset

    decrypted_text = numbers_to_text(potential_numbers)

    if ENABLE_INTEGRITY_CHECK:
        if calculate_message_hash(decrypted_text) != hash_check:
            print("Warnung: Integritätsprüfung fehlgeschlagen! Nachricht eventuell beschädigt.")

    return decrypted_text
