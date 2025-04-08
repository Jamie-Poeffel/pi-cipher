import math
import random
from collections import Counter
import base64

REDUNDANCY = 3
DUMMY_PROBABILITY = 0.4

def get_pi_digits(n):
    pi_str = str(math.pi).replace('.', '')
    while len(pi_str) < n:
        pi_str += str(math.pi).replace('.', '')
    return [int(d) for d in pi_str[:n]]

def text_to_numbers(text):
    return [ord(char) for char in text]

def numbers_to_text(numbers):
    return ''.join(chr(num) for num in numbers)

def numbers_to_bytes(numbers):
    return bytes(numbers)

def bytes_to_numbers(b):
    return list(b)

def create_real_group(char_value, offset, pi_digits):
    group = []
    current_offset = offset
    for _ in range(REDUNDANCY):
        pi_value = pi_digits[current_offset % len(pi_digits)]
        encrypted = (char_value + pi_value) % 256
        group.append(encrypted)
        current_offset = (current_offset * 17 + 31) % len(pi_digits)
    return group, current_offset

def create_dummy_group(pi_digits):
    group = []
    dummy_offset = random.randint(0, len(pi_digits) - 1)
    for _ in range(REDUNDANCY):
        dummy_value = random.randint(0, 255)
        pi_value = pi_digits[dummy_offset % len(pi_digits)]
        encrypted = (dummy_value + pi_value) % 256
        group.append(encrypted)
        dummy_offset = (dummy_offset * 17 + 31) % len(pi_digits)
    return group

def encrypt(text):
    numbers = text_to_numbers(text)
    pi_digits = get_pi_digits(100000)

    start_offset = random.randint(0, len(pi_digits) - 1)
    offset = start_offset

    groups = []

    for number in numbers:
        real_group, offset = create_real_group(number, offset, pi_digits)
        groups.append(real_group)

        if random.random() < DUMMY_PROBABILITY:
            dummy_group = create_dummy_group(pi_digits)
            groups.append(dummy_group)

    random.shuffle(groups)
    flat_numbers = [start_offset] + [num for group in groups for num in group]

    message_bytes = numbers_to_bytes(flat_numbers)
    encoded_message = base64.b64encode(message_bytes).decode('utf-8')
    return encoded_message

def decrypt(encoded_message):
    message_bytes = base64.b64decode(encoded_message)
    message = bytes_to_numbers(message_bytes)

    start_offset = message[0]
    data = message[1:]

    pi_digits = get_pi_digits(100000)
    groups = [data[i:i + REDUNDANCY] for i in range(0, len(data), REDUNDANCY)]

    offset = start_offset
    potential_numbers = []

    for group in groups:
        if len(group) < REDUNDANCY:
            continue

        decrypted_candidates = []
        current_offset = offset

        for encrypted_num in group:
            pi_value = pi_digits[current_offset % len(pi_digits)]
            original = (encrypted_num - pi_value) % 256
            decrypted_candidates.append(original)
            current_offset = (current_offset * 17 + 31) % len(pi_digits)

        common = Counter(decrypted_candidates).most_common(1)
        if common[0][1] > 1:
            potential_numbers.append(common[0][0])
            offset = current_offset

    return numbers_to_text(potential_numbers)
