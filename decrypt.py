import string

def create_decrypt_map(shift1, shift2):
    """Creates a reverse mapping to safely handle character wrapping."""
    rev_map = {}
    for c in string.ascii_lowercase:
        if 'a' <= c <= 'm':
            enc = chr((ord(c) - 97 + (shift1 * shift2)) % 26 + 97)
        else:
            enc = chr((ord(c) - 97 - (shift1 + shift2)) % 26 + 97)
        rev_map[enc] = c

    for c in string.ascii_uppercase:
        if 'A' <= c <= 'M':
            enc = chr((ord(c) - 65 - shift1) % 26 + 65)
        else:
            enc = chr((ord(c) - 65 + (shift2 ** 2)) % 26 + 65)
        rev_map[enc] = c
    return rev_map

def decrypt_text(input_file, output_file, shift1, shift2):
    rev_map = create_decrypt_map(shift1, shift2)
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    decrypted = ""
    for c in content:
        if c.isalpha():
            decrypted += rev_map.get(c, c)
        else:
            decrypted += c

    with open(output_file, 'w') as f:
        f.write(decrypted)
    print(f"Successfully decrypted to '{output_file}'.")