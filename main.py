from encrypt import encrypt_text
from decrypt import decrypt_text
from verify import verify_decryption

def main():
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