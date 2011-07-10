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

gcc = "gcc -march=native -E -v - </dev/null 2>&1 | sed -n 's/.* -v - //p'"
cflags = subprocess.Popen(gcc, shell=True, stdout=subprocess.PIPE).communicate()[0].strip()

if __name__ == "__main__":
    print use_flags
    print cflags
    print jobs
    exit()

text("""# $warning
USE_ARCH="$flags"
ARCH_FLAGS="$cflags"
ARCH_JOBS="$jobs"
""").render(flags=" ".join(use_flags), cflags=cflags, jobs=jobs)
