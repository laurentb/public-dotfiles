import subprocess

pythons = subprocess.check_output(['eselect', '--brief', 'python', 'list']).decode('utf-8')
pythons = [python.replace('.', '_') for python in pythons.splitlines()]
assert len(pythons)

python = subprocess.check_output(['eselect', '--brief', 'python', 'show']).decode('utf-8')
python = python.replace('.', '_').strip()
assert python

if __name__ == "__main__":
    print(pythons)
    print(python)
    exit()


text("""# $warning
PYTHON_TARGETS="$pythons"
PYTHON_SINGLE_TARGET="$python"
""").render(pythons=" ".join(pythons), python=python)
