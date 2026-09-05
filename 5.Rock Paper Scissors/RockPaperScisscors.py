import random


def get_computer_choice():
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)


def determine_winner(player, computer):
    if player == computer:
        return "draw"

    if (
        (player == "rock" and computer == "scissors")
        or (player == "paper" and computer == "rock")
        or (player == "scissors" and computer == "paper")
    ):
        return "player"

    return "computer"


def display_score(player_score, computer_score):
    print("\n" + "=" * 35)
    print("              SCORE")
    print("=" * 35)
    print(f"You      : {player_score}")
    print(f"Computer : {computer_score}")
    print("=" * 35)


def main():
    player_score = 0
    computer_score = 0

    print("=" * 40)
    print("       ROCK PAPER SCISSORS")
    print("=" * 40)

    while True:
        print("\nChoose your move:")
        print("1. Rock")
        print("2. Paper")
        print("3. Scissors")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "4":
            break

        choices = {
            "1": "rock",
            "2": "paper",
            "3": "scissors"
        }

        if choice not in choices:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            continue

        player_choice = choices[choice]
        computer_choice = get_computer_choice()

        print(f"\nYou chose      : {player_choice.title()}")
        print(f"Computer chose : {computer_choice.title()}")

        result = determine_winner(
            player_choice,
            computer_choice
        )

        if result == "player":
            print("🎉 You win!")
            player_score += 1

        elif result == "computer":
            print("🤖 Computer wins!")
            computer_score += 1

        else:
            print("🤝 It's a draw!")

        display_score(player_score, computer_score)

    print("\n" + "=" * 40)
    print("             FINAL SCORE")
    print("=" * 40)
    print(f"You      : {player_score}")
    print(f"Computer : {computer_score}")

    if player_score > computer_score:
        print("\n🏆 Congratulations! You won the game!")

    elif computer_score > player_score:
        print("\n🤖 Computer wins the game!")

    else:
        print("\n🤝 The game ended in a draw!")

    print("\nThanks for playing! 👋")


main()
