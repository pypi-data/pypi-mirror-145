# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathfind_visualiser']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['pathfind-visualiser = pathfind_visualiser.main:main']}

setup_kwargs = {
    'name': 'pathfind-visualiser',
    'version': '0.1.3',
    'description': 'Pathfinding algorigthms written in Python and visualised with the Pygame library',
    'long_description': "# pathfind-visualiser\n\n![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)\n![OSX](https://img.shields.io/badge/-OSX-black?logo=apple)\n![Windows](https://img.shields.io/badge/-Windows-blue?logo=windows)\n![Python](https://img.shields.io/badge/Python-v3.9%5E-green?logo=python)\n![Version](https://img.shields.io/github/v/tag/rolv-apneseth/ps-typer?label=version)\n[![PyPi](https://img.shields.io/pypi/v/pathfind-visualiser?label=pypi)](https://pypi.org/project/pathfind-visualiser/)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n![pathfind-visualiser](https://user-images.githubusercontent.com/69486699/161395210-d3d26e3b-7921-4e86-9b2d-54b6478688bd.png)\n\n## Description\n\nPathfinding algorigthms written in Python and visualised with the [Pygame](https://pypi.org/project/pygame/) library. Also has a couple built-in maze generation algorithms, and gives the user the ability to create their own mazes by hand, so that algorithms can be observed under a variety of different circumstances.\n\n## Installation\n\nUsing `pip` (if you're on Windows, replace `python3` with just `python` down below):\n\n```bash\npython3 -m pip install pathfind-visualiser\n```\n\nThen, launch the program by running the command:\n\n```bash\npathfind-visualiser\n```\n\nNote that if the command does not work you may need to configure your system `PATH` variable (check out some Stack Overflow answers linked below).\n\n-   [Windows](https://stackoverflow.com/a/36160069/14316282)\n-   [Linux or Mac](https://stackoverflow.com/a/62823029/14316282)\n\n## Usage\n\n1. From the main menu, read the instructions and keys sections to familiarise yourself with how to use the interface\n2. In the options section select the number of rows/columns you want and select a maze type (or leave it on none)\n    - Note: Random is it's own maze generating algorithm (defined below)\n3. Click on the algorithm you wish to visualise and the maze should appear\n4. If you wish to view another algorithm (or take another look at the instructions), press the `Esc` key to return to the main menu\n\n## The Algorithms:\n\n#### 1. [A\\* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)\n\n-   Uses a heuristic function (manhattan distance) to guide the pathfinding algorithm via the use of a priority queue\n-   This makes it one of the faster algorithm, but note that this is because you need to know the position of the end point for the heuristic function\n-   Nodes are expanded in the direction of the end node\n-   The shortest path is always guaranteed\n\n#### 2. [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)\n\n-   Uses a simple FIFO queue so nodes are expanded in every direction equally (searches in a circle outwards from the starting node if maze is empty)\n-   The shortest path is always guaranteed\n\n#### 3. [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search)\n\n-   Uses a LIFO queue, where nodes are added in order of direction (top, right, bottom then left) from expanded nodes\n-   This means that nodes will always be expanded leftwards until there is a barrier, then down, etc.\n-   Therefore, this is a very inefficient algorithm but it is used because it is the way a human might navigate a maze (left-hand rule)\n-   Does not guarantee the shortest path. In fact, in an open maze this could take very long to finish even if the end node is directly beside the start\n\n#### 4. [Dijkstra's Shortest Path First](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)\n\n-   Nodes will be expanded very similarly to breadth-first search, but it is designed to be able to handle paths of different weights\n-   The main difference is the use of a priority queue\n-   Unfortunately this visualiser only uses weights of 1 between each adjacent node so the changes are not visualisable, but feel free to check out the code in algorithms.py (they're different, I promise!)\n-   This always guarantees the shortest possible path\n\n#### 5. [Greedy Best-First Search](http://web.pdx.edu/~arhodes/ai6.pdf)\n\n-   Uses the manhattan distance heuristic function like the a\\* algorithm\n-   However, it does not take into account the distance already travelled and just expands the node with the shortest estimated distance next (hence greedy)\n-   Does not guarantee the shortest path but it often does find the shortest path\n\n## The Maze Types:\n\n-   **Random** - All nodes have a 25% chance of becoming a barrier node\n-   **Swirl** - Basic swirl pattern which takes up the entire grid\n-   **Imperfect** - My first attempt at a proper maze generating algorithm. Called imperfect because very small sections of the maze may be sectioned off from the rest of the maze\n-   **Simple** - Based off of recursive division but slightly different\n",
    'author': 'Rolv-Apneseth',
    'author_email': 'rolv.apneseth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rolv-Apneseth/pathfind-visualiser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
