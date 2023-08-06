"""
Setup manifest.
"""

from setuptools import setup, find_packages

with open("README.md", mode='r', encoding="utf-8") as readme:

    project_description = readme.read()

setup(
  name = 'gamelibgames',
  packages = find_packages(),
  package_data={
    'gamelibgames': [
      "picross/img/gameplay_demo/*.gif",
      "picross/img/icon/*.gif",
      "picross/sfx/*.wav",
      "picross/*.txt",
      "picross/img/demo/*.gif",
      "picross/img/icon/*.gif",
      "picross/img/references/*.png",
      "picross/sfx/*.wav",
      "minesweeper/*.txt"
    ]
  },
  version = '1.1.3',
  license='MIT',
  description = 'A collection of minigames made with Gamelib.',
  long_description=project_description,
  long_description_content_type="text/markdown",
  author = 'NLGS',
  author_email = 'flighterman@fi.uba.ar',
  url = 'https://github.com/NLGS2907/gamelib_games',
  keywords = ['GAMELIB', 'MINIGAMES'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
  ],
)
