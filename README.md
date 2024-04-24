### Repository content description

This repository contains the code described in the **Spotting Culex pipiens from Satellite: modeling environmental suitability in central Italy with Sentinel-2 and Deep Learning methods** scientific paper for EO data download and preprocessing. At the path *src/EO*, you will find the scripts used for downloading and preprocessing satellite data.

 * MODIS sample data is provided

 * Sentinel-2 sample data is NOT provided due to its size (about 600/1200 MB). You can download a sample Sentinel-2 archive for testing, running the 01b_DOWNLOAD_S2_CDSE.py script. It requires your Copernicus Data Space Ecosystem credentials (register [here](https://tinyurl.com/yw69kbuj))

 * The python script used to download the Sentinel-2 data described in the paper relies on the [SentinelSat](https://sentinelsat.readthedocs.io/en/stable/index.html) package, which is **no longer functional**, since the Copernicus SciHub was permanently closed. Read the project development team's announcement [here](https://github.com/sentinelsat/sentinelsat/blob/main/README.rst). Nonetheless, we have included the sentinelsat based script (01a_DOWNLOAD_S2.py) in the repository for completeness and informational purposes, but we did not include the sentinelsat package in the *requirements.txt* file because it would be pointless.
   
### Prepare the environment

##### VS Code DevContainer
The most convenient way to run the scripts is to use the provided container, which automatically sets up the python environment required for the code to function properly. To launch the devcontainer, you will need:
 * Docker Desktop (or Rancher)
 * Visual Studio Code with the *Dev Containers* extension installed.

After starting Docker on your machine, clone this repository on your computer and launch Visual Studio Code within the obtained folder. The editor will recognize the *.devcontainer/devcontainer.json* configuration file and initiate the development environment, installing by itself the packages listed in *requirements.txt* file.

##### Other methods
If you prefer not to use the devcontainer, you can install the python environment as you like (Anaconda, Pyenv, Poetry, etc.). Always refer to the *requirements.txt* file for the list of required packages.

 ### Run the EO pipeline
 Follow this steps to run the EO data download and preprocessing pipeline:
  * cd to *src/EO/script* path
  * run 01b_DOWNLOAD_S2_CDSE.py to download a sample Sentinel-2 archive (you need to create a CDSE account first!)
  * run 02_EXTRACT_S2_20M.py to extract the archive to SAFE folder
  * run 03_CROP_NORM_S2_GDAL.py to create Sentinel-2 crops
  * run 04_CROP_RESIZE_MODIS.py to create MODIS LSTD/LSTN crops

All the needed folders not already included in this repo will be automatically created during the process.

##### Note
The *.tif* crops generated by this collection of scripts are the input data used to feed the ML model described in the scientific paper. The ML model codebase is available at https://github.com/loribonna/release_frontiers_wnv 
