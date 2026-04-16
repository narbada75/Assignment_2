def encrypt_text(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    encrypted = ""
    for c in content:
        if 'a' <= c <= 'm':
            encrypted += chr((ord(c) - 97 + (shift1 * shift2)) % 26 + 97)
        elif 'n' <= c <= 'z':
            encrypted += chr((ord(c) - 97 - (shift1 + shift2)) % 26 + 97)
        elif 'A' <= c <= 'M':
            encrypted += chr((ord(c) - 65 - shift1) % 26 + 65)
        elif 'N' <= c <= 'Z':
            encrypted += chr((ord(c) - 65 + (shift2 ** 2)) % 26 + 65)
        else:
            encrypted += c

    with open(output_file, 'w') as f:
        f.write(encrypted)
    print(f"Successfully encrypted to '{output_file}'.")