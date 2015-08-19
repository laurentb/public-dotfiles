from __future__ import print_function

import subprocess
from textwrap import dedent

try:
    subprocess.check_output(['eselect', 'ruby', 'show'], stderr=subprocess.PIPE)
    has_ruby = True
except subprocess.CalledProcessError:
    has_ruby = False

if has_ruby:
    rubies = subprocess.check_output(['eselect', '--brief', 'ruby', 'list'])
    rubies = [ruby.split('(')[0].strip() for ruby in rubies.splitlines()]
    assert len(rubies)

if __name__ == "__main__":
    print(rubies)
    exit()


if has_ruby:
    text(dedent("""
        # $warning
        RUBY_TARGETS="$rubies"
        """)).render(rubies=" ".join(rubies))
else:
    text("# No ruby installation found.\n").render()
