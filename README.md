# UDMF Toolkit for Blender
UDMF Toolkit is a Blender Addon allows you to imports UDMF DOOM maps into Blender.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![CI](https://github.com/deviant-syndrome/blender-udmf-toolkit/actions/workflows/ci.yml/badge.svg?branch=main)

## Features
* **UDMF Map Importing**: Directly import your DOOM maps from PWADs into Blender.
* **Texture Baking (Upcoming)**: In the future, this feature will allow users to seamlessly bake the DOOM textures for better visualization and rendering in Blender.

## Installation

Blender does not support package management, so we had to bundle some of the addon dependencies into the `libs`. Since we are  
not sure, if this violates any licenses or not, you will need to install the addon manually.

To install the UDMF Toolkit addon, you have two options: using the bootstrap.sh script or using the provided Makefile.

### Using bootstrap.sh
1. Ensure you have git, python3, and poetry installed on your machine.

2. Download or clone the repository to your local machine.

3. Navigate to the root directory of the addon in your terminal.

4. Run the bootstrap script:
```bash
sh bootstrap.sh
```

This will automatically handle the cloning, dependency installation, bundling, and packaging of the addon. After the script completes, you'll find a udmf_toolkit_addon.zip file in the directory.

### Using Makefile
1. Ensure you have git, make, python3, and poetry installed on your machine.

2. Download or clone the repository to your local machine.

3. Navigate to the root directory of the addon in your terminal.

4. Run the make command:

* Download the latest version of UDMF Toolkit.
* Open Blender and navigate to Edit > Preferences > Add-ons.
* Click on Install and select the downloaded ZIP file.
* Enable UDMF Toolkit from the Add-ons list.

### Installing the Addon in Blender
After obtaining the udmf_toolkit_addon.zip file through either of the above methods:

1. Open Blender.

2. Go to Edit > Preferences > Add-ons.

3. Click on Install... and navigate to the udmf_toolkit_addon.zip file.

4. Select the ZIP file and click on Install Add-on.

5. Once installed, you should see the UDMF Toolkit in the list. Ensure it's enabled by checking the box next to it.

6. Unfold the UDMF Toolkit addon preferences and set the path to your texture directory. Note, in this directory you need to have all you PNG textures unpacked from your both your main IWAD and a mod you're working on.
7. You're all set! The UDMF Toolkit addon should now be available in Blender.

## Usage
1. Navigate to the Import option in Blender.
2. Select Import PWAD Map from the list.
3. Choose your desired PWAD file map in UDMF format and import.
4. Note: It's recommended to start with a fresh Blender scene to avoid conflicts.

## Future Plans
While the core functionality is focused on UDMF map importing, we have big plans for the future:

Texture Baking: Elevate your ZDoom maps in Blender with high-quality textures.
And more to come!

## Contributing
If you have suggestions, bug reports, or want to contribute to the code, feel free to open an issue or send a pull request on the project's GitHub page.

## License
BSD-3-Clause

## Acknowledgments
Special thanks to the DOOM community for the continuous support and inspiration.