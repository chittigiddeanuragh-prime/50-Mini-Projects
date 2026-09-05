import re


def validate_email(email):
    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if re.fullmatch(pattern, email):
        return True

    return False


def main():
    print("=" * 45)
    print("          EMAIL VALIDATOR")
    print("=" * 45)

    while True:
        email = input("\nEnter your email address: ").strip()

        if not email:
            print("❌ Please enter an email address.")
            continue

        if validate_email(email):
            print(f"✅ {email} is a valid email address.")
        else:
            print(f"❌ {email} is not a valid email address.")

        choice = input("\nDo you want to check another email? (y/n): ").lower()

        if choice != "y":
            print("\nThank you for using Email Validator!")
            break


main()