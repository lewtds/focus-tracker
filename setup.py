from distutils.core import setup

files = ["gui/index.html", 
    "gui/js/*.js",
    "gui/js/adapters/*.js",
    "gui/js/modules/*.js",
    "gui/js/themes/*.js"]

setup(name='focus-tracker',
      version='0.1',
      packages=['focustracker'],
      package_data={'focustracker':files},
      data_files=[("share/applications", ["focus-tracker.desktop"])],
      license="GPL",
      scripts=["focus-tracker"]
      )
