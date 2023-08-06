from distutils.core import setup
setup(
  name = 'freqle',         # How you named your package folder (MyLib)
  packages = ['freqle'],   # Chose the same as "name"
  version = '1.2.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The package is used to simulate the emission of gravitational waves from a cluster of black holes',   # Give a short description about your library
  author = 'Riccardo Felicetti',                   # Type in your name
  author_email = 'felicettiriccardo1@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Unoaccaso/freqle',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Unoaccaso/freqle/archive/refs/tags/v_1.2.1.tar.gz',
  keywords = ['Gravitational Waves', 'Black Holes', 'Simulation'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
          'numpy',
          'termcolor',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10'
  ],
)
