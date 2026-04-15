from sys import stdin, stdout


def main():
    # 把鍵盤照順序排好，之後就能用「往左 2 格」來找答案。
    keyboard = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    text = stdin.read()
    out = []

    for ch in text:
        small = ch.lower()

        # 找得到的字元就往左抓 2 格；找不到的像空白和換行就原樣保留。
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
