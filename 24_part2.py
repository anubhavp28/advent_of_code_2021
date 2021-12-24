# CAUTION: 3 AM, shit code. I will refactor someday.
# I de-compiled the program:
# inp w
# z = (10 + w)
# ---------------------------
# inp w
# z = 26 * z + 16 + w
# ---------------------------
# inp w
# z = 26 * z + w
# ---------------------------
# inp w
# z = 26 * z + 13 + w
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 14
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 4
# ---------------------------
# inp w
# z = 26 * z + 11 + w
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 3
# ---------------------------
# inp w
# z = 26 * z + 16 + w
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 12
# ---------------------------
# inp w
# z = 26 * z + 15 + w
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 12
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 15
# ---------------------------
# inp w
# z = z / 26
# w = (z mod 26) - 12


from tqdm import tqdm

stages = [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]
delta = [10, 16, 0, 13, -14, -4, 11, -3, 16, -12, 15, -12, -15, -12]

largest_value = 0
for i in tqdm(range(1111111, int(1e7))):
    values = list(str(i))
    values = list(map(int, values))
    if 0 in values:
        continue
    ans = []
    z = 0
    for idx in range(14):
        if stages[idx] == 1:
            ans.append(values[0])
            z = 26 * z + delta[idx] + values.pop(0)
        else:
            w = (z % 26) + delta[idx]
            if w < 1 or w > 9:
                break
            ans.append(w)
            z = z // 26

    if len(ans) != 14:
        continue

    v = 0
    for d in ans:
        v = 10 * v + d
    print(v)
    break

