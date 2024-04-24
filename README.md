This repository contains the code described in the **Spotting Culex pipiens from Satellite: modeling environmental suitability in central Italy with Sentinel-2 and Deep Learning methods** scientific paper.

### Prepare the environment 
The most convenient way to run the scripts is to use the provided **devcontainer**, which automatically sets up the python environment required for the code to function properly. To launch the devcontainer, you will need Docker Desktop (or Rancher) and Visual Studio Code with the Dev Containers extension installed.

After starting Docker on your machine, clone this repository on your computer and launch Visual Studio Code within the obtained folder. The editor will recognize the *.devcontainer/devcontainer.json* configuration file and initiate the development environment, installing by itself the packages listed in *requirements.txt* file.

If you prefer not to use the devcontainer, you can install the Python environment as you like (Anaconda, Pyenv, Poetry, etc.). Refer to the requirements.txt file for the list of required packages.

### Sentinel 2 Preprocessing code used to generate ML input data
At the path *src/EO*, you will find the scripts used for downloading and preprocessing satellite data.

 * MODIS sample data is provided

 * Sentinel-2 sample data is NOT provided due to its size (about 600/1200 MB). You can download a sample Sentinel-2 archive using the 01b_DOWNLOAD_S2_CDSE.py script. It requires your Copernicus Data Space Ecosystem credentials (register [here](https://tinyurl.com/yw69kbuj))

 * The script used to download the Sentinel-2 data for the paper scope relies on the [SentinelSat](https://sentinelsat.readthedocs.io/en/stable/index.html) package, which is **no longer functional**. You can read the project development team's announcement [here](https://github.com/sentinelsat/sentinelsat/blob/main/README.rst). We have also included the sentinelsat based script (01a_DOWNLOAD_S2.py) in the repository for completeness, but we did not include the sentinelsat package in the requirements.txt file, so this script will not work.

 ### Run the EO pipeline
 Follow this steps to run the EO data download and preprocessing pipeline:
  * cd to *src/EO/script* path
  * run 01b_DOWNLOAD_S2.py to download a sample Sentinel-2 archive (you need to create a CDSE account first!)
  * run 02_EXTRACT_S2_20M.py to extract the archive to SAFE folder
  * run 03_CROP_NORM_S2_GDAL.py to create Sentinel-2 crops
  * run 04_CROP_RESIZE_MODIS.py to create MODIS LSTD/LSTN crops
