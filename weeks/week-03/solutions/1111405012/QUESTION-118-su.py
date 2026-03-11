import sys


def solve(input_str: str) -> str:
    lines = [line.strip() for line in input_str.splitlines() if line.strip()]
    if not lines:
        return ""

    max_x, max_y = map(int, lines[0].split())
    scent = set()
    out = []

    i = 1
    while i < len(lines):
        x, y, d = lines[i].split()
        x = int(x)
        y = int(y)
        i += 1

        cmds = lines[i] if i < len(lines) else ""
        i += 1

        lost = False
        for c in cmds:
            if c == "L":
                d = {"N": "W", "W": "S", "S": "E", "E": "N"}[d]
            elif c == "R":
                d = {"N": "E", "E": "S", "S": "W", "W": "N"}[d]
            elif c == "F":
                nx, ny = x, y
                if d == "N":
                    ny += 1
                elif d == "S":
                    ny -= 1
                elif d == "E":
                    nx += 1
                else:
                    nx -= 1

                if nx < 0 or nx > max_x or ny < 0 or ny > max_y:
                    if (x, y, d) in scent:
                        continue
                    scent.add((x, y, d))
                    lost = True
                    break
                else:
                    x, y = nx, ny

        if lost:
            out.append(f"{x} {y} {d} LOST")
        else:
            out.append(f"{x} {y} {d}")

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
