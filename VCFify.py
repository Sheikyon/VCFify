import time
import re
import os
import sys

def display_welcome():
    """Display the welcome message with a spinning animation during the loading time."""
    print("Welcome to VCFify v1.0! - written by Sheikyon (sheikyon@sheikyon.me). Available in: https://github.com/Sheikyon/VCFify")
    spin_chars = ['|', '/', '-', '\\']

    # Show the spinning animation for 2 seconds
    start_time = time.time()
    while time.time() - start_time < 2:
        for char in spin_chars:
            sys.stdout.write(f'\r{char} Loading...')
            sys.stdout.flush()
            time.sleep(0.1)  # Adjust the speed of the animation
    print("\rVCFify is a tool that will allow you to generate as many contacts as you want to be saved in a vCard compatible file, so that you can easily import them to your phone.")  # Clear the loading animation line

def validate_phone_number(phone):
    """Check if the input is a valid phone number or not."""
    # Remove all non-digit characters except the initial '+'
    cleaned_phone = re.sub(r'[^0-9x+]', '', phone)
    if '+' in cleaned_phone:  # Ensure it starts with '+'
        return True
    return False

def format_phone_number(base_phone, iteration):
    """Format the phone number, replacing all 'x' with iterated values."""
    formatted_phone = base_phone
    # Count the number of 'x' characters in the phone number
    x_count = formatted_phone.count('x')

    # For each occurrence of 'x', replace it with a digit from the iteration count
    # Calculate the digit that will replace each 'x' based on the current iteration
    # Example: For iteration 0, replace all 'x' with '0', for iteration 1, replace all 'x' with '1', etc.

    # Create a list of digits to replace the 'x's
    digits = [f'{(iteration // (10 ** (x_count - 1 - i))) % 10:01d}' for i in range(x_count)]

    # Replace each 'x' with the corresponding digit from the digits list
    for i, digit in enumerate(digits):
        formatted_phone = formatted_phone.replace('x', digit, 1)

    # Ensure the phone number is formatted in the form +XX XXX XX XX (if there are enough digits)
    formatted_phone = re.sub(r'(\d{2})(\d{3})(\d{2})(\d{2})', r'+\1 \2 \3 \4', formatted_phone)

    return formatted_phone

def generate_vcf(contact_name, phone_number):
    """Generate VCF content for the given contact."""
    vcf_data = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact_name}
TEL:{phone_number}
END:VCARD"""
    return vcf_data

def save_vcf(contact_name, vcf_data, file_name):
    """Save VCF data into a single file."""
    with open(file_name, 'a') as f:
        f.write(vcf_data)
    print(f"Saved contact {contact_name} to {file_name}")

def main():
    # Clear the terminal screen (compatible with Windows, with or without WSL, and Linux)
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix-based (Linux/macOS)
        os.system('clear')

    contact_count = 1
    file_name = "contacts.vcf"

    # Create the VCF file and add the beginning of the VCF data
    with open(file_name, 'w') as f:
        f.write("BEGIN:VCARD\nVERSION:3.0\n")

    display_welcome()

    while True:
        phone = input("Please enter a phone number, with 'x' for placeholders (e.g. +1 (234) 567-xxxx):")

        if not validate_phone_number(phone):
            print("The data you entered is invalid. Please re-enter it.")
        else:
            # Iterate over the 'x' placeholders, replacing them with all combinations of 00, 01, ..., 99
            # The number of iterations depends on the number of 'x' characters in the phone number
            # Example: if there are 4 'x's, we need 10000 iterations, from 0000 to 9999
            x_count = phone.count('x')
            iterations = 10 ** x_count  # 100 if there are 2 'x's, 1000 if 3 'x's, etc.

            for i in range(iterations):
                formatted_phone = format_phone_number(phone, i)
                contact_name = f"VCFify ~#{contact_count}"
                vcf_data = generate_vcf(contact_name, formatted_phone)
                save_vcf(contact_name, vcf_data, file_name)
                contact_count += 1

            cont = input("Do you want to generate another contact? (y/n): ")
            if cont.lower() != 'y':
                break

    # Add the end of the VCF data
    with open(file_name, 'a') as f:
        f.write("END:VCARD\n")

    print(f"All contacts have been saved to {file_name}")

if __name__ == "__main__":
    main()
