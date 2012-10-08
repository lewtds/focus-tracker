# Description #

Focus Tracker is a simple app to keep track of how much time an app has
the user's focus, potentially helping them better track their time on the 
computer.

# Usage #

## Prerequisites ##

On a Ubuntu 12.04 machine or a similar environment, this should suffice:
    
    sudo apt-get install gir1.2-appindicator3-0.1 gir1.2-wnck-3.0 \
       gir1.2-gtk-3.0 gir1.2-webkit-3.0 python-gi

For an ArchLinux machine:

    sudo pacman -S libwebkit3 libwnck3 gtk3 gobject-introspection \
       python-gobject python

_Note_: The project uses GNOME's GObject Introspection technology (hence the "gi"
part in those package names) to enable Python to utilize GNOME's available
packages (Ubuntu's AppIndicator, GTK+, ...) so if you happen to run a different
distro, just look around for some similar GObject Introspection packages.

## Download ##

    git clone https://github.com/lewtds/focus-tracker.git focus-tracker

## Running ##

Currently, there's no install script. But there's a run script inside the
main package directory under the name of "focus-tracker". Assuming
you've downloaded and unpacked the software into a folder named focus-tracker,
the following command should runs the app:

    cd focus-tracker && ./focus-tracker

[aoeaoe](#/aoeuthaue)
