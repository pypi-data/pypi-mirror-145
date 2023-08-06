.. title:: python3 bot library

**NAME**

**BOTLIB** - python3 bot library


**SYNOPSIS**

| ``bot <cmd> [key=value] [key==value]``


**DESCRIPTION**

**BOTLIB** is a solid, non hackable bot, that runs under systemd as a 24/7
background service and starts the bot after reboot, intended to be
programmable in a static, only code, no popen, no imports and no reading
modules from a directory.

**BOTLIB** is programmable, to program the bot you have to have the code
available as employing your own code requires that you install your own bot as
the system bot. This is to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runnable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are avoided. Scanning
sys.path is avoided with a bot.all module that imports all needed modules.

**BOTLIB** stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence more chance.
Paths carry the type in the path name what makes reconstruction from filename
easier then reading type from the object.

Only include your own written code should be the path to "secure".


**INSTALL**

``pip3 install botlib``


**CONFIGURATION**

configuration is done by calling the config command of the bot.

**irc**

| ``bot config server=<server> channel=<channel> nick=<nick>``
|
| (*) default channel/server is #botlib on localhost

**sasl**

| ``bot password <nickservnick> <nickservpass>``
| ``bot config password=<outputfrompwd>``

**users**

| ``bot config users=True``
| ``bot meet <userhost>``

**RUNNING**

run the bot with the ``bot`` command, it will start a shell with
the irc bot. use the -c option if you don't want just the console.

``bot [-c]``

**console**

| ``bart@botlib:~$ bot -c``
| ``BOT start at Fri Apr 1 20:02:40 2022``
| ``> thr``
| ``Console.loop(1s) thr(1s)``
| ``>`` 


**irc**


| ``bart@botlib:~$ bot``
| ``BOT start at Fri Apr 1 20:00:43 2022``
| ``server=localhost port=6667 channel=#botlib nick=botlib cc=!``
| ``> thr``
| ``Console.loop(8s) IRC.keep(8s) IRC.loop(8s) IRC.output(8s) thr(8s) Fetcher.run(4m52s)``
| ``>`` 


**COMMANDS**

the bot has the following commands.

| ``bart@botlib:~$ bot commands``
| ``alias,commands,config,delete,display,fetch,find,fleet,log,meet,more,nick,``
| ``operator,password,remove,rse,rss,threads,todo``

here is a short description of the commands.

| ``alias`` - shows all the aliases the bot knows
| ``commands`` - shows all commands
| ``config`` - shows the irc configuration, also edits the config
| ``delete`` - removes a user from bot
| ``display`` - sets display items for a rss feed
| ``fetch`` - runs a rss feed fetching batch
| ``find`` - allows you to display objects on the datastore, read-only json files on disk 
| ``fleet`` - shows a list of bot registered to the bus
| ``log`` - logs some text
| ``meet`` - adds a users with there irc userhost
| ``more`` - displays cached output, channel wise.
| ``nick`` - changes nick on irc
| ``operator`` - tries to have the bot give you operator status (+o)
| ``password`` - combines a nickserv name/password into a sasl password
| ``remove`` - removes a rss feed by matching is to its url
| ``rse`` - raises an Raise exception, for debug purposes
| ``rss`` - adds a feed to fetch, fetcher runs every 5 minutes
| ``threads`` - show the running threads
| ``todo`` - adds a todo item, no options returns list of todo's

**PROGRAMMING**

``git clone https://github.com/bthate/botlib``

``joe bot/hello.py``

::

 from bot.command import Command

 def hello(event):
     event.reply("hello!")

 Command.add(hello)

``joe bot/all.py``

::

 from bot.table import Table

 from bot import hello

 Table.add(hello)

**AUTHOR**

Bart Thate

**COPYRIGHT**

**BOTLIB** is placed in the Public Domain. No Copyright, No License.
