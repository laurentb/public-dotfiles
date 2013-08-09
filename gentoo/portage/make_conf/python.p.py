import subprocess

pythons = subprocess.Popen(['eselect', '--brief', 'python', 'list'],
        stdout=subprocess.PIPE).communicate()[0]  # capture stdout
pythons = [python.replace('.', '_') for python in pythons.splitlines()]
assert len(pythons)

defpython = subprocess.Popen(['eselect', '--brief', 'python', 'show'],
        stdout=subprocess.PIPE).communicate()[0]  # capture stdout
defpython = defpython.strip().replace('python', '')
assert len(defpython)

if __name__ == "__main__":
    print pythons
    print defpython
    exit()


text("""# $warning
PYTHON_TARGETS="$pythons"
USE_PYTHON="$defpython"
""").render(pythons=" ".join(pythons), defpython=defpython)
