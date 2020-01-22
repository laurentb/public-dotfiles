import re
import subprocess

# References:
# https://bitbucket.org/mgorny/cpuinfo2cpuflags
# https://github.com/hartwork/resolve-march-native

with open("/proc/cpuinfo") as f:
    cpuinfo = f.read()
    flags = re.search("^flags\s+:\s+(.+)$", cpuinfo, re.MULTILINE).groups()[0].split(" ")
    # See /usr/portage/profiles/desc/cpu_flags_x86.desc
    flags = ['sse3' if flag == 'pni' else flag for flag in flags]
    flags = ['fma3' if flag == 'fma' else flag for flag in flags]
    flags = ['popcnt' if flag == 'abm' else flag for flag in flags]
    flags = ['padlock' if flag == 'phe' else flag for flag in flags]

    procs = re.findall("^processor\s+:\s+(\d+)$", cpuinfo, re.MULTILINE)
    jobs = len(procs)


available_use_flags = ("avx", "avx2", "ssse3", "xop", "aes",
                       "popcnt", "f16c",
                       "mmx", "mmxext",
                       "3dnow", "3dnowext",
                       "fma3", "fma4",
                       "sse", "sse2", "sse3", "sse4a", "sse4_1", "sse4_2")

use_flags = set([flag for flag in available_use_flags if flag in flags])
# mmxext/mmx2 is a subset of SSE (blame AMD marketing)
if 'sse' in use_flags:
    use_flags.add('mmxext')


gccv = subprocess.Popen(['gcc', '-march=native', '-E', '-v', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate('')[1].decode('utf-8')  # capture stderr
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
# Remove -mno arguments, they confuse some packages.
short_cflags = re.sub(' -mno-[^ ]+', '', short_cflags).strip()

cflags = cflags.strip()


lspci = subprocess.check_output(['lspci', '-k']).decode('utf-8')
cards = ['vesa', 'dummy', 'none']
llvm = ['X86', 'BPF']
use_cards = []
if ': i915' in lspci or ': i965' in lspci:
    cards.append('intel')
    cards.append('i915')
    cards.append('i965')
    use_cards.append('vulkan')
if ': radeon' in lspci:
    cards.append('radeon')
    cards.append('radeonsi')
    cards.append('amdgpu')
    llvm.append('AMDGPU')
    use_cards.append('opencl')
    use_cards.append('vulkan')
if ': nouveau' in lspci:
    cards.append('nouveau')


if __name__ == "__main__":
    print(use_flags)
    print(gccv[0])
    print(cflags)
    print(short_cflags)
    print(jobs)
    print(cards)
    exit()


text("""# $warning
CPU_FLAGS_X86="$flags"
ARCH_FLAGS="$cflags"
SHORT_ARCH_FLAGS="$short_cflags"
ARCH_JOBS="$jobs"
VIDEO_CARDS="$cards"
LLVM_TARGETS="$llvm"
USE_VIDEO_CARDS="$use_cards"
""").render(flags=" ".join(sorted(use_flags)),
            cflags=cflags,
            short_cflags=short_cflags,
            jobs=jobs,
            cards=" ".join(cards),
            llvm=" ".join(llvm),
            use_cards=" ".join(use_cards))
