import re
import subprocess

with open("/proc/cpuinfo") as f:
    cpuinfo = f.read()
    flags = re.search("^flags\s+:\s+(.+)$", cpuinfo, re.MULTILINE).groups()[0].split(" ")
    # HACK: pni means sse3
    flags = ['sse3' if flag == 'pni' else flag for flag in flags]

    procs = re.findall("^processor\s+:\s+(\d+)$", cpuinfo, re.MULTILINE)
    jobs = len(procs)


available_use_flags = ("avx", "ssse3",
                       "mmx", "mmxext",
                       "3dnow", "3dnowext",
                       "sse", "sse2", "sse3", "sse4", "sse4_1")

use_flags = set([flag for flag in available_use_flags if flag in flags])
# mmxext/mmx2 is a subset of SSE (blame AMD marketing)
if 'sse' in use_flags:
    use_flags.add('mmxext')


gccv = subprocess.Popen(['gcc', '-march=native', '-E', '-v', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate('')[1]  # capture stderr
gccv = [flags for flags in gccv.splitlines() if ' -v - ' in flags]
assert len(gccv) == 1

# Remove everything before -march.
# It usually has -D_FORTIFY_SOURCE=2 which is implied by -O2 in Gentoo.
cflags, count = re.subn('^.+-march=', '-march=', gccv[0], 1)
assert count == 1

# Remove everything after -mtune
# It is implied by -march, and everything after is either nothing or
# default Gentoo Hardened stuff.
cflags, count = re.subn('-mtune=.+$', '', cflags, 1)
assert count == 1

# Remove --param arguments.
# They don't seem that useful (sets exact CPU cache sizes).
# This prevents badly written build systems, like Chromium's,
# from failing.
short_cflags = re.sub(' --param [^ ]+', '', cflags).strip()

cflags = cflags.strip()


lspci = subprocess.check_output(['lspci', '-k'])
cards = ['vesa', 'dummy', 'none']
use_cards = []
if ': i915' in lspci:
    cards.append('intel')
if ': radeon' in lspci:
    cards.append('radeon')
    use_cards.append('r600-llvm-compiler')
if ': nouveau' in lspci:
    cards.append('nouveau')


if __name__ == "__main__":
    print use_flags
    print gccv[0]
    print cflags
    print short_cflags
    print jobs
    print cards
    exit()


text("""# $warning
USE_ARCH="$flags"
ARCH_FLAGS="$cflags"
SHORT_ARCH_FLAGS="$short_cflags"
ARCH_JOBS="$jobs"
VIDEO_CARDS="$cards"
USE_VIDEO_CARDS="$use_cards"
""").render(flags=" ".join(use_flags),
            cflags=cflags,
            short_cflags=short_cflags,
            jobs=jobs,
            cards=" ".join(cards),
            use_cards=" ".join(use_cards))
