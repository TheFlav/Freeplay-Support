# Information about Ports

RetroPie has fairly good support for other games, including a large number that support controllers and can be installed relatively easily. We have currently tested the following as of June 20th, 2019, sorted by increasing installation difficulty:
- [Wolfenstein 3D](#Wolfenstein-3D)
- [Doom](#Doom)
- [Quake](#Quake)
- [Cave Story](#Cave-Story) (Classic indie platformer)
- [Solarus Engine](#Solarus-Engine) (Zelda-likes based on A Link to the Past)
- [Hydra Castle Labyrinth](#Hydra-Castle-Labyrinth) (Freely available Metroidvania)
- [Pico-8](#Pico-8) (Non-free, fantasy console with large community and built in development tools)
- [TexMaster2009](#TexMaster2009) (Tetris: The Grandmaster clone)

### Wolfenstein 3D ([Ports Page](https://github.com/RetroPie/RetroPie-Setup/wiki/Wolfenstein-3D))
Install `wolf4sdl` in RetroPie Setup under `Manage Packages`, `Optional Packages`. Installs free, shareware version by default, but supports full version WADs.

### Doom ([Ports Page](https://github.com/RetroPie/RetroPie-Setup/wiki/Doom))
Install `lr-prboom` in RetroPie Setup under `Manage Packages`, `Optional Packages`. Installs free, shareware version by default, but supports full version WADs.

### Quake ([Ports Page](https://github.com/RetroPie/RetroPie-Setup/wiki/Quake))
Install `lr-tyrquake` in RetroPie Setup under `Manage Packages`, `Optional Packages`. Installs free, shareware version by default, but supports full version WADs.

### Cave Story ([Ports Page](https://github.com/RetroPie/RetroPie-Setup/wiki/Cave-Story))
Install `lr-nxengine` in RetroPie Setup under `Manage Packages`, `Optional Packages`. Then copy the unzipped game files from [HERE](https://www.cavestory.org/download/cave-story.php) in the language of your choice to `/home/pi/RetroPie/roms/ports/CaveStory/`. We recommend using `wget` on your Pi to download the `.zip` directly instead of SCPing the file.

### Solarus Engine ([Ports Page](https://github.com/RetroPie/RetroPie-Setup/wiki/Solarus))
The version of Solarus Engine installed by the `solarus` package in RetroPie Setup (`Manage Packages`,`Optional Packages`) is not the current version, so not all games will work. It also takes some work to add external games. There is a rewrite of the installation script in the works that may allow for better game detection. Package also installs three games.

### Hydra Castle Labyrinth ([RGCD's Download Page for PC Version](https://www.rgcd.co.uk/2012/01/hydra-castle-labyrinth-pc.html))
Follow the guide at [THIS REPO](https://github.com/zerojay/RetroPie-Extra) to install the extra packages to RetroPie Setup's `Extra Packages` section. This repo is unmaintained, so we cannot attest to its long term usability, but the `hcl` package installs correctly with gamepad support.

### Pico-8 ([Official Website](https://www.lexaloffle.com/pico-8.php))
The Lexaloffle blog has a post detailing how to install Pico-8 as a system [HERE](https://www.lexaloffle.com/bbs/?tid=3935), but you need to use the `pico8_dyn` binary to make sure all games work and to prevent errors on boot.

If you would like the system to be in the Ports menu instead, all you have to do is install Pico-8 to a folder somewhere, just like the blog post, (we recommend `/home/pi/RetroPie/roms/ports/pico-8`), then make a short bash script in `/home/pi/RetroPie/roms/ports` that launches `/<absolute-path-to-binary>/pico8_dyn -splore`. There will be a menu item in the Ports menu the next time EmulationStation is started.

To make controllers work correctly, you will have to generate a mapping file using [THIS GUIDE](https://retropie.org.uk/forum/topic/15577/ppsspp-controller-setup-guide-for-when-nothing-else-works). Put the referenced `out.txt` file in `/home/pi/.lexaloffle/pico-8` with the name `sdl_controllers.txt`. For a Freeplay CM3 with full size buttons, our controller map is:

```
15000000010000000400000000010000,GPIO Controller 1,platform:Linux,a:b0,b:b3,x:b2,y:b1,back:b6,start:b7,leftshoulder:b4,rightshoulder:b5,dpup:-a1,dpdown:+a1,dpleft:-a0,dpright:+a0,
```

### TexMaster2009 ([Relevant RetroPie Forum Topic](https://retropie.org.uk/forum/topic/8745/texmaster-port/9))
You can follow the guide in the linked forum post. The tl;dr is like so:
- Download packaged release and decompress
- Decompress file that is marked with your desired version (e.g. `Texmaster2009.rpi2-ARMv7.tar.gz`) and move this entire folder where you want it.
- Make port config entry in `/opt/retropie/configs/ports/texmaster2009/emulators.cfg`
- Make script to launch binary via `runcommand`

This game unfortunately cannot be exit without the keyboard, so you will have to shutdown/restart your console unless you have a keyboard attached. If you find a way to circumvent this, please contact us.

It should also be noted that this is extremely themable, as almost all of the files in the `data/` folder can be replaced or edited to suit your preferences. Many use assets from the original Tetris: The GrandMaster games.
