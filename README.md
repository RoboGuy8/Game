TWO PLAYER PVP SHOOTER GAME

Requirements to run:
  - newest version of python with pygame and csv installed
  - make sure to have all the files, not just Pygame.py
  - Windows 11 (other OS's should work but not guaranteed)
  - minimum display resolution of 720p. (1080p reccomended)
  - minimum specs:
     - RAM: 4GB
     - CPU: Intel 4770K or AMD equivalent
     - GPU: integrated
     - EMPTY STORAGE: 500MB
     - OS: Win 11
  - reccomended specs:
     - RAM: 32GB
     - CPU: Intel 13600K or AMD equivalent
     - GPU: AMD RX 7900XT 20GB, Intel A770 16GB or NVIDIA RTX 4080 16GB
     - EMTY STORAGE 500TB
     - OS: Win 12++ PRO ULTRA MAX XL

How to run:
  - install all the files in one folder without any other files
  - make sure to have python, csv and pygame installed and updated
  - run the Pygame.py file
  - Enjoy ♥

Controlls:
  - Player 1:
    - W,A,D,SPACEBAR (jump, move left, move right, shoot)
  - Player 2:
    - I,J,L,ENTER (jump, move left, move right, shoot)
  - Start:
    - press the start button to start the game
  - End:
    - close the game by clicking on the X in the right top corner of the window

Features:
  - Simple PVP shooter game for 2 players (4 player support coming in the future updates)
  - Each player has 5 lives and unlimited shots, which are however under cooldown
  - can create own map by editing csv file (-1 for air and 4 for block)
  - customizable game parameters.
  - customizable looks, try replacing the texture or img files

Code parts:
  1) imports of pygame and csv and initialization of pygame 
  2) setting basic variables such as gravity, fps,... and setting title of the game window
  3) importing images and transforming them to needed size, settings, format
  4) defing classes (Player, World and Bullet) and functions
  5) creation of bullet group, where all existing bullets will be allocated for easier collision handleling, creation of player 1 and 2 with their parameters
  6) loading data from map.scv and numbering sectors of the map
  7) main game loop, start button
  8) setting cotrolls for movement (event handlerer)
  9) shooting cooldown and spawning position for bullets and hit registring (lives)
  10) adding some fog to the edges of the screen, updating screen and ending game
