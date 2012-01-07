import re
import subprocess

with open("/proc/cpuinfo", "r") as cpuinfo:
    flags = re.search("^flags\s+:\s+(.+)$", cpuinfo.read(), re.MULTILINE).groups()[0].split(" ")
    # HACK: pni means sse3
    flags = [ 'sse3' if flag == 'pni' else flag for flag in flags ]

with open("/proc/cpuinfo", "r") as cpuinfo:
    procs = re.findall("^processor\s+:\s+(\d+)$", cpuinfo.read(), re.MULTILINE)
    jobs = len(procs) + 1

available_use_flags = ( "avx", "mmx", "mmxext", "3dnow", "3dnowext", "sse", "sse2", "sse3", "sse4", "ssse3" )

use_flags = [ flag for flag in available_use_flags if flag in flags ]
use_flags += [ "-"+flag for flag in available_use_flags if flag not in flags ]

gccv = subprocess.Popen(['gcc', '-march=native', '-E', '-v', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate('')[1] # capture stderr
gccv = [flags for flags in gccv.split('\n') if ' -v - ' in flags]
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

## Remove --param arguments.
## They don't seem that useful (sets exact CPU cache sizes).
## This prevents badly written build systems, like Chromium's,
## from failing.
#cflags = re.sub(' --param [^ ]+', '', cflags)

cflags = cflags.strip()

if __name__ == "__main__":
    print use_flags
    print gccv[0]
    print cflags
    print jobs
    exit()

text("""# $warning
USE_ARCH="$flags"
ARCH_FLAGS="$cflags"
ARCH_JOBS="$jobs"
""").render(flags=" ".join(use_flags), cflags=cflags, jobs=jobs)
