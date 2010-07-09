import re
import subprocess

with open("/proc/cpuinfo", "r") as cpuinfo:
    flags = re.search("^flags\s+:\s+(.+)$", cpuinfo.read(), re.MULTILINE).groups()[0].split(" ")

available_use_flags = ( "mmx", "mmxext", "3dnow", "3dnowext", "sse", "sse2", "sse3", "sse4", "ssse3" )

use_flags = [ flag for flag in available_use_flags if flag in flags ]
use_flags += [ "-"+flag for flag in available_use_flags if flag not in flags ]

gcc = "gcc -march=native -E -v - </dev/null 2>&1 | sed -n 's/.* -v - //p'"
cflags = subprocess.Popen(gcc, shell=True, stdout=subprocess.PIPE).communicate()[0].strip()

if __name__ == "__main__":
    print use_flags
    print cflags

text("""# $warning
USE_ARCH="$flags"
ARCH_FLAGS="$cflags"
""").render(flags=" ".join(use_flags), cflags=cflags)
