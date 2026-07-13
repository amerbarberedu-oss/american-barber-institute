with open("build.py", "r") as f:
    lines = f.readlines()

out_lines = []
skip = False
for line in lines:
    if line.startswith('    campus_switch = "", "true"'):
        skip = True
        out_lines.append('    campus_switch = ""\n')
        continue
    if skip:
        if line.strip() == ')':
            skip = False
        continue
    out_lines.append(line)

with open("build.py", "w") as f:
    f.writelines(out_lines)
