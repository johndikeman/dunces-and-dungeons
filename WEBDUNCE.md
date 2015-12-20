<p align='center'><img src='https://dl.dropboxusercontent.com/s/6az46igwevjzgz4/20151219_174739-1.jpg?dl=0' length=300px width=300px></p>
WELCOME TO WEBDUNCE
===================

"one time she'rak hit me so hard the game crashed" -john


INSTALLING
==========

1. clone the repo, if you haven't already.
2. install the dependencies with ```pip install -r requirements.txt```
3. if you're on a *nix system, head on over to the <a href='redis.io/download'>redis download page</a> and download and install the version that smells the best to you. if you're on windows, get a better computer. just kidding. lucky for you, MSOpenTech provides redis windows binaries. <a href='https://github.com/MSOpenTech/redis/releases/tag/win-2.8.2104'>this one</a> worked for me.
4. now you should be ready to rock and roll.

RUNNING THE GAME
================
these steps need to be followed every time you want to launch webdunce.

1. if you're on windows, you can probably skip this step. everyone else: start the redis server by mashing ```redis-server``` into your terminal of choice.
2. cd into the ```web``` directory, and launch the server by running `python server.py'
3. back out into the root of the project and then run the game itself by typing ```python dunces-and-dungeons.py web```
4. fire up your browser of choice and navigate to localhost:5000. if you don't see anything, do these steps over again and be SURE to do them in order.
5. ???
6. profit!

as always, open an issue if you find an issue in any of the issues that i have issued to you. <3 john
