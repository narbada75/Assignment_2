def encrypt_text(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    encrypted = ""
    shift = shift1 + shift2  # single consistent shift

    for c in content:
        if 'a' <= c <= 'z':
            encrypted += chr((ord(c) - 97 + shift) % 26 + 97)
        elif 'A' <= c <= 'Z':
            encrypted += chr((ord(c) - 65 + shift) % 26 + 65)
        else:
            encrypted += c

    with open(output_file, 'w') as f:
        f.write(encrypted)

    print("\n--- Encrypted Text ---")
    print(encrypted)


def decrypt_text(input_file, output_file, shift1, shift2):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    decrypted = ""
    shift = shift1 + shift2

    for c in content:
        if 'a' <= c <= 'z':
            decrypted += chr((ord(c) - 97 - shift) % 26 + 97)
        elif 'A' <= c <= 'Z':
            decrypted += chr((ord(c) - 65 - shift) % 26 + 65)
        else:
            decrypted += c

    with open(output_file, 'w') as f:
        f.write(decrypted)

    print("\n--- Decrypted Text ---")
    print(decrypted)


def verify_decryption(original_file, decrypted_file):
    try:
        with open(original_file, 'r') as f1, open(decrypted_file, 'r') as f2:
            original = f1.read()
            decrypted = f2.read()

        print("\n--- Verification ---")
        if original == decrypted:
            print("✅ Success: Decrypted text matches original.")
        else:
            print("❌ Failed: Decrypted text does NOT match original.")

    except FileNotFoundError:
        print("Error: Files missing for verification.")


def main():
    print("--- Encryption & Decryption Program ---")

    try:
        shift1 = int(input("Enter shift1 value: "))
        shift2 = int(input("Enter shift2 value: "))
    except ValueError:
        print("Invalid input.")
        return

    encrypt_text("raw_text.txt", "encrypted_text.txt", shift1, shift2)
    decrypt_text("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)
    verify_decryption("raw_text.txt", "decrypted_text.txt")


if __name__ == "__main__":
    main()