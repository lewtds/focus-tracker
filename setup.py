from distutils.core import setup

files = ["gui/*"]

setup(name='focus-tracker',
      version='0.1',
      packages=['focustracker'],
      package_data={'focustracker':files},
      data_files=[("share/applications", ["focus-tracker.desktop"])],
      license="GPL",
      scripts=["focus-tracker"]
      )
