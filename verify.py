def verify_decryption(original_file, decrypted_file):
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