import string

def encrypt_text(input_file, output_file, shift1, shift2):
    """
    Encrypt text from input file using custom shift rules.
    
    Args:
        input_file (str): Path to the input file to encrypt.
        output_file (str): Path to write the encrypted output.
        shift1 (int): First shift parameter.
        shift2 (int): Second shift parameter.
    """
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    encrypted = ""
    for c in content:
        if 'a' <= c <= 'm':
            # Shift forward by shift1 * shift2
            # Wrap-around modulo ensures result stays within a-z range (0-25)
            encrypted += chr((ord(c) - 97 + (shift1 * shift2)) % 26 + 97)
        elif 'n' <= c <= 'z':
            # Shift backward by shift1 + shift2
            # Modulo 26 handles negative wrap-around correctly
            encrypted += chr((ord(c) - 97 - (shift1 + shift2)) % 26 + 97)
        elif 'A' <= c <= 'M':
            # Shift backward by shift1
            encrypted += chr((ord(c) - 65 - shift1) % 26 + 65)
        elif 'N' <= c <= 'Z':
            # Shift forward by shift2 squared
            encrypted += chr((ord(c) - 65 + (shift2 ** 2)) % 26 + 65)
        else:
            # Spaces, tabs, special characters, and numbers remain unchanged
            encrypted += c

    with open(output_file, 'w') as f:
        f.write(encrypted)
    print(f"Successfully encrypted to '{output_file}'.")

def create_decrypt_map(shift1, shift2):
    """
    Creates a reverse mapping to safely handle character wrapping.
    
    Args:
        shift1 (int): First shift parameter.
        shift2 (int): Second shift parameter.
    
    Returns:
        dict: Mapping from encrypted characters to original characters.
    """
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
    """
    Decrypt text from input file using the reverse mapping.
    
    Args:
        input_file (str): Path to the encrypted file.
        output_file (str): Path to write the decrypted output.
        shift1 (int): First shift parameter.
        shift2 (int): Second shift parameter.
    """
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

def verify_decryption(original_file, decrypted_file):
    """
    Verify that the decrypted text matches the original text.
    
    Args:
        original_file (str): Path to the original file.
        decrypted_file (str): Path to the decrypted file.
    """
    try:
        with open(original_file, 'r') as f1, open(decrypted_file, 'r') as f2:
            original = f1.read()
            decrypted = f2.read()
        
        if original == decrypted:
            print("Verification successful: Decrypted text matches the original.")
        else:
            print("Verification failed: Decrypted text does not match the original.")
    except FileNotFoundError:
        print("Error: Files missing for verification.")

def main():
    """Main function to orchestrate encryption, decryption, and verification."""
    print("--- Question 1: Encryption & Decryption ---")
    try:
        shift1 = int(input("Enter shift1 value: "))
        shift2 = int(input("Enter shift2 value: "))
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    # Automatically run the required sequence
    encrypt_text("raw_text.txt", "encrypted_text.txt", shift1, shift2)
    decrypt_text("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)
    verify_decryption("raw_text.txt", "decrypted_text.txt")

if __name__ == "__main__":
    main()