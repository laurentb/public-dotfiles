import subprocess

pythons = subprocess.Popen(['eselect', '--brief', 'python', 'list'],
        stdout=subprocess.PIPE).communicate()[0]  # capture stdout
pythons = [python.replace('.', '_') for python in pythons.splitlines()]
assert len(pythons)

if __name__ == "__main__":
    print pythons
    exit()


text("""# $warning
PYTHON_TARGETS="$pythons"
""").render(pythons=" ".join(pythons))
