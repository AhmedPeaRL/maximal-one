import re

power_file = "../data/power_result.txt"
readme = "../README.md"

with open(power_file) as f:
    content = f.read()

match = re.search(r"Power:\s*([0-9.]+)", content)
if match:
    power = float(match.group(1))
    if power >= 0.8:
        color = "brightgreen"
    else:
        color = "orange"
    badge = f"https://img.shields.io/badge/power-{power}-{color}"
else:
    badge = "https://img.shields.io/badge/power-unknown-lightgrey"

with open(readme, "r") as f:
    text = f.read()

text = re.sub(
    r"https://img\.shields\.io/badge/power-[^)]*",
    badge,
    text
)

with open(readme, "w") as f:
    f.write(text)
