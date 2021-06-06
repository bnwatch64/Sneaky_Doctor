# Sneaky_Doctor
You are working on the 10th floor of your workplace, the city hospital, when you heard the big news - the new virus **Python-19** is causing a world-wide pandemic, infecting everyone who comes into contact with it. You quickly grab your coat and run to the elevatot, but it's too late: Everyone in the hospital is already infected!

You figure there's only one chance to escape this hell:  
**Sneaking your way through all of the 10 floors without touching anyone!**

![](assets/Background.png?raw=true)

# Installation
You need to have Python Version 3.6+ and a compatible version of pip installed on your system. We recommend downloading a stable realease from the official Python Website: [Mac](https://www.python.org/downloads/mac-osx/) / [Windows](https://www.python.org/downloads/windows/)

To further install all the required packages for the game, navigate your command line to the repository and run following command:

```
pip install -r requirements.txt
```

> Note that this installs the required packages into your global python installation. If you want to install packages into a virtual environment instead, follow [these](https://docs.python.org/3/tutorial/venv.html) steps.

Once you've followed the above steps, you are ready to play Sneaky Doctor!

# How to play
To run the game, navigate your command line to the repository and run following command:

```
python3 main.py
```

From the main menu you can now start a new game.

### Controls
* Use `W` `A` `S` `D` or the arrow keys to move the Doctor up, left, down and right
* Press the Speaker Icon in the upper right corner of the screen to mute/unmute the game sound
* Press `Esc` or the home icon in the upper left corner to save and return to the main menu

### The goal
As you might know from our little introduction at the top, your goal is to reach the exit on each floor of the hospital without touching any infected people on the way. There are 11 levels as there are 11 storages in your hospital.  
If you die, you will have to restart the current level. You can see your total number of deaths in the bottom right corner.  
> Pro Tip: On some maps you can find masks on the floor. Picking these up may help you in some close-call situations...

Once you've completed the 11th level (which is really hard, you should really give it a try) you effectively win the game!  
We would really appreciate you sharing your end score (Number of Deaths) with us by sending a screenshot to benniader@gmail.com!

# Design tools
A big part of this programming project was the creation of the levels. We thought that instead of wasting hours designing levels with hit-box dimensions etc., it would be better to waste even more hours by making some kind of a level designer. The positive thing about it?

**You can use it too!**

## How to create your own levels in Sneaky Doctor
If you want to add your own level into the game all you have to do is to take a look at our own levels under the `assets/levels` directory.

A level `x` consists of a folder `level_x` holding at least a map file `mapx.png`.  
So if you for example want to add a 12th level to our game, you will have to add the folder `level_12` to the `assets/levels` directory, containing an image `map12.png`.

### About map images
A map image always has to be 32 pixels wide and 31 pixels high, as this is the size of our playing field in order of _blocks_ if you was to be looking at it from above. One block can hold exactly one game object, like a wall, Enemy or mask. The positions are later translated by the game to create a 2.5D like perspective.

Different pixel colors in a map image translate to different game objects. A
* **Black** (0, 0, 0) pixel translates to a wall.
* **Green** (0, 255, 0) pixel translates to the exit and must be used once and only once in a map image.
* **Blue** (0, 0, 255) pixel translates to the start position of the player in the level and must be used once and only once in a map image.
* **Red** (255, 0, 0) pixel translates to a mask object.

> Every other pixel color will be ignored by the level parser of the game and can be differed accordingly.

If you create a level containing a map image as described above, you should be able to walk around and even complete it by walking through the exit. But how can you add some action - namely some infectious patients into your own level?

### About NPC paths
In addition to your map image you have the option to add as many NPC path images to your level folder as you want. Just like the map image, all NPC path images have to be 32x31 pixels and follow a naming scheme:

`npcx.png`, where x has to be the number of the NPC. So if you for example wanted to create two NPCs walking through your level, you would want to create a `npc1.png` and `npc2.png` file in your level folder.

Like in the map image, different pixel colors translate to different functionalities.
* **Black** (0, 0, 0) and **Blue** (0, 0, 255) pixels build the path that the corresponding NPC is going to walk on. All the black pixels in a NPC path image have to form one continuous path. Diagonal connections are also possible.
* A **Green** (0, 255, 0) pixel indicates the start position of the NPC on a path, so it has to substitute one of the black pixels in a path. It must be used once and only once per NPV path image.

> Attention!  
> A pixel on the path must not be surrounded by more than three other pixels of the path (also diagonally). In this case the path parser of the game can't synthesize a deterministic path and throws an error.

If you followed the above steps correctly, Congratulations! - you've just created your very own Sneaky Doctor level!

> Disclaimer:
> The level design workflow is generally not intended to be used by the end user of the game. It should be a tool for potential level designers to be able to focus on the act of designing the actual level, rather than dealing with all sorts of different challanges when designing right in code. Therefor it is indeed possible to e.g. let a NPC walk through walls. In the process of creating our own levels it definately turned out to be very helpful... and to be honest, it's kinda' cool to 😉

### Best practice
In the process of creating our own levels with the explained workflow we found, that the best workflow for creating the required images for a level is to create a multi-layered image in an application like Adobe Photoshop or GIMP. This way you can draw the NPC paths directly on top of the map image and e.g. avoid collisions with walls etc. In the end you just have to export every layer by itself and there you have it - a complete Sneaky Doctor level ready to be played!

Feel free to take a deeper look at our map and NPC path images in the `assets/levels` directory!
