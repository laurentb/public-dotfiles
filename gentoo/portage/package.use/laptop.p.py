# Only link the file if we want "desktop" files
if "laptop" in options.tags:
    redirect("laptop")
else:
    ignore()
