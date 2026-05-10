import subprocess

result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True
)

changes = []

for line in result.stdout.splitlines():

    path = line[3:]

    if (
        path.startswith("artifacts/")
        and path != "artifacts/release_manifest.json"
    ):
        changes.append(line)

if changes:

    print("\n".join(changes))

    raise SystemExit(
        "❌ Post-seal mutation detected"
    )

print("✅ RELEASE MANIFEST SEALED")
print("✅ No post-seal mutation detected")
