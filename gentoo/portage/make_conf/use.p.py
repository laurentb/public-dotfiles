collections = set(["USE_UNWANTED", "USE_OPTIMIZE", "USE_LANGUAGES",
                   "USE_HARDWARE", "USE_ADDONS", "USE_FEATURES",
                   "USE_NETWORK", "USE_COMPRESSION"])

inpdevs = ["evdev"]

if "desktop" in options.tags:
    collections.update(["USE_X", "USE_XFEATURES", "USE_DESKENV",
                        "USE_MEDIA", "USE_DESKDEVS",
                        "USE_HOMENETWORK", "USE_VIDEO_CARDS"])

if "homeserver" in options.tags:
    collections.add("USE_HOMENETWORK")

if "laptop" in options.tags:
    collections.add("USE_LAPTOP")
    inpdevs.append("synaptics")

use = ["${%s}" % flag for flag in collections]

text("""# $warning
USE="$use"
INPUT_DEVICES="$inpdevs"
NUT_DRIVERS="usbhid-ups"
SANE_BACKENDS=""
CAMERAS="ptp2"
""").render(use=" ".join(sorted(use)), inpdevs=" ".join(sorted(inpdevs)))
