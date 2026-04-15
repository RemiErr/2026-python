from sys import stdin, stdout


def main():
    keyboard = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    text = stdin.read()
    out = []

    for ch in text:
        small = ch.lower()

        if small in keyboard:
            pos = keyboard.index(small)
            if pos >= 2:
                out.append(keyboard[pos - 2])
            else:
                out.append(ch)
        else:
            out.append(ch)

    stdout.write("".join(out))


if __name__ == "__main__":
    main()
