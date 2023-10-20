# node_tabber

Node Tabber is a Houdini/Nuke style node adding tool for Blender's Node tree graphs; namely the Shader, Compositing, Texture and Geometry.

Instead of having to press SHIFT+A and then scrolling the sub menus to fins the correct node, or even clicking on the search menu and maybe getting the correct node; you can just press the TAB button which will bring up an intelligent search list which even supports node acronyms. For example, typing SX would bring up the Seperate XYZ node.
This saves a lot of time when working with large node trees.

## Installation (Blender 3.4+)

Download the latest version from the [Releases Page](https://github.com/williamchange/node_tabber/releases), pick the version that best suits the Blender version you are using, and install from Blender's preferences, just like any other add-on (no need to unzip)

> **NOTE**: If you are a regular user, DO NOT go to `'<> Code' > 'Download as ZIP'` to download a copy of the addon. This gives you a development version of the addon which is larger in size and offers no advantage over the release versions outside of development.

## Older versions (Blender 3.1-3.3)

Release versions for these versions are planned, but not implemented yet.

For now the legacy branches where you can download these versions as ZIPs (i.e. [3.3](https://github.com/williamchange/node_tabber/tree/33), [3.2](https://github.com/williamchange/node_tabber/tree/32) and [3.1](https://github.com/williamchange/node_tabber/tree/31)), will be kept up for the time being. These legacy branches may not have the same functionality as the versions with up-to-date releases.

---


# Fork

This is a fork which includes:

- Additional sub node entries for new vector math operations
- Geometry Nodes sub-nodes
- Fix for appending custom nodegroups (see https://github.com/jiggymoon69/node_tabber/pull/10)
- Workaround for [this commit(Blender 3.4+)](https://github.com/blender/blender/commit/837144b4577f161baf1625f8a5478c83a088ea0f) which breaks the add-on with geonodes. See [D15973](https://developer.blender.org/D15973).