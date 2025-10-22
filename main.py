# main.py
import parrot_ai  # 這行會先報錯，因為檔案還沒建立
import random

moods = ["happy", "sad", "cry", "angry"]


def run_game():
    print("--- AI 鸚鵡啟動！--- (輸入 'quit' 離開)")
    while True:
        user_input = input("你說: ")
        if user_input.lower() == "quit":
            break

        ai_response = parrot_ai.get_parrot_response(
            {"input": user_input, "mood": random.choice(moods)}
        )

        print(f"AI鸚鵡說: {ai_response}")


if __name__ == "__main__":
    run_game()
