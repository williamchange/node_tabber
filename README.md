# node_tabber

Node Tabber is a Houdini/Nuke style node adding tool for Blender's Node tree graphs; namely the Shader, Compositing and Texture graphs.

Instead of having to press SHIFT+A and then scrolling the sub menus to fins the correct node, or even clicking on the search menu and maybe getting the correct node; you can just press the TAB button which will bring up an intelligent search list which even supports node acronyms. For example, typing SX would bring up the Seperate XYZ node.
This saves a lot of time when working with large node trees.

# Fork

This is a fork which includes:
- Additional sub node entries for new vector math operations
- Geometry Nodes sub node entries (i.e. switch/random value nodes)
- Fix for appending custom nodegroups (see https://github.com/jiggymoon69/node_tabber/pull/10)
  
## Installation
Download this [repository(3.2 branch)](https://github.com/williamchange/node_tabber/archive/refs/heads/3.2.zip) and install from Blender's preferences, just like any other add-on (no need to unzip)