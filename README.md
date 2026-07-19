# Project Description: Openusd Reactive Simulation-On-Demand Ingestion

## Overview: Generates dust simulations without an artist ever touching the mouse.
Things to understand before looking at the code: python, python for Houdini, openUSD basics, basic nets in Houdini, Solaris basics, os, some idea about hython

# flowchart

<img width="3281" height="1575" alt="usd_project_flowchart" src="https://github.com/user-attachments/assets/262ee533-37f8-4e9f-8071-0c17d388b63a" />

# demo output_v1

https://github.com/user-attachments/assets/c2b7c652-cc27-4ae4-a080-6ce323c71931

# Notes

1. using vex within to run with hython: i had to use vex to manually simulate the dust because popnet wouldn't load into my memory ue to system issues. using vex doesn't load and heavy dopnet with all its nodes and node types, and therefore the it executes super fast. of course, this is in fact taking a step backwards because solaris already has the option to create a popnet in just a few lines but i was not able to do this on my machine so i am leaving this note here for others.
Also, this was very intersting for learning more about how houdini manages things. so popnet is not a c++ hardcoded node in houdini's codebase- it is an HDA (network of nodes in a package), which means it takes a while to load all of the assets when this is called. if, in any case, the load fails, then even accessing any one asset is not possible. in fact even when opening the Houdini application, it takes time to load because it is loading all of these HDAs.
and since hython is instructed to boot as fast as possible, it might sometimes skip loading the HDAs at all, and we end up getting some error like 'a node type is not recognized'.
another fix (other than manually vex scripting) is find and load the required library before we create the popnet. this makes sure hython already has access to the nodes before it ever executes. i will leave both these methods in the code and you can choose which one based on your usecase.
something like a simple dust sim can be written with vex, but there is no point going by this method if your net is going to be complex. that would defeat the purpose of using hython (headless Houdini) at all.
2. using houdini apprentice so dust sim is exporting as .usdnc. not recognized so need to write a plugin using Sdf


# References:

1. [https://openusd.org/dev/tut_xforms.html](https://openusd.org/dev/tut_xforms.html)
2. [https://github.com/kiryha/Houdini/wiki/pixar-usd-python-api](https://github.com/kiryha/Houdini/wiki/pixar-usd-python-api)
3. [https://tokeru.com/cgwiki/HoudiniPython.html](https://tokeru.com/cgwiki/HoudiniPython.html)


### PENDING TASKS
- naming conventions to be corrected
- detailed diagram workflow to be added
- dynamic coordinates in rand for sphere and ground




