from sys import stdin, stdout


KEYBOARD = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
DECODE_MAP = {KEYBOARD[index]: KEYBOARD[index - 2] for index in range(2, len(KEYBOARD))}


def decode(text):
    """把每個字元換成鍵盤左邊第二個按鍵。"""
    answer = []

    for char in text:
        lower_char = char.lower()
        answer.append(DECODE_MAP.get(lower_char, char))

    return "".join(answer)


def main():
    text = stdin.read()
    if text:
        stdout.write(decode(text))


if __name__ == "__main__":
    main()
