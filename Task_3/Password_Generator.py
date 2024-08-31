import random
import string

def generate_password(length, use_special_chars=True):
    """
    Generates a random password with the specified length.
    
    Parameters:
        length (int): The length of the generated password.
        use_special_chars (bool): Whether to include special characters in the password.
    
    Returns:
        str: The generated password.
    """
    if length <= 0:
        return "Password length must be greater than 0."
    
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("Welcome to the Password Generator!")
    
    while True:
        try:
            length = int(input("Enter the desired length of the password: "))
            if length <= 0:
                print("Please enter a positive integer.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        use_special_chars = input("Include special characters (e.g., @, #, $)? (yes/no): ").strip().lower()
        if use_special_chars in ['yes', 'y']:
            use_special_chars = True
        elif use_special_chars in ['no', 'n']:
            use_special_chars = False
        else:
            print("Invalid response. Defaulting to no special characters.")
            use_special_chars = False
        
        password = generate_password(length, use_special_chars)
        print(f"Generated Password: {password}")
        print("---------------------------------")
        
        again = input("Generate another password? (yes/no): ").strip().lower()
        if again not in ['yes', 'y']:
            print("Thank you for using the Password Generator!")
            break

if __name__ == "__main__":
    main()
