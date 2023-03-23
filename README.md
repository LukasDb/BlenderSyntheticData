# Synthetic Dataset Generation using Blender
This project provides a pipeline to create high-quality ray-traced synthetic data using Blender and Python. The images created are independently randomized and all objects and lights are randomly placed and rotated in the camera view. 
The following data is generated (only for objects included in the ID_dict):
- RGB (uint8)
- Depth (float32, in meters)
- Class Segmentation (ID definition in param.json)
- Camera and Object poses (json, in meter and quaternion)
- Camera Intrinsic Matrix
- Stereo Camera Baseline

File Structure:
```
blender/
├── <dataset_name>/
│   ├── 01/
|	|	├── depth/
|	|	|	├── depth_0000.exr 			-> depth from camera in meters
|	|	|	├── depth_0001.exr
|	|	|	├── ...
|	|	├── gt/
|	|	|	├── gt_0000.json 			-> camera and objects' poses
|	|	|	├── gt_0001.json
|	|	|	├── ...
|	|	├── mask/
|	|	|	├── segmentation_0000.exr 	-> object IDs
|	|	|	├── segmentation_0001.exr
|	|	|	├── ...
|	|	├── rgb/
|	|	|	├── rgb_0000.png 			-> RGB Image
|	|	|	├── [rgb_0000_R.png] 	(if stereo mode)
|	|	|	├── ...
|	|	├── gt.json 					-> Intrinsic Matrix, Stereo Baseline
|	|	└── params.json		  	-> Backup of Generation Parameters
│   ├── 02/
│   ├── 03/
│   └── ...
```

## Requirements
### Blender:
- Download Blender 3.3 LTS [here](https://www.blender.org/download/lts/3-3/). Do not install from apt or snap, 3.3 is required
- Install Scipy for built-in Python of Blender:
  - Navigate to your Blender 3.3 directory and run :
    ```
    cd 3.3/python/bin/
    ./python3.10 -m ensurepip
    ./python3.10 -m pip install scipy
    ```
- Run Blender and open the base scene `scene_linemod.blend`. On Opening, allow the exectution of scripts permanently.

## Setup
- Provide background images in the folder 'backgrounds'
- Download Blender scene and custom models and kpts from [here](https://drive.google.com/drive/folders/1RodFYe8YxojwDZ3UIDka-FkL9Sw9AiSq?usp=sharing)
- Download LineMod Models and pastte ply files into lm_obj_mesh
- Download ugreal_fg_objects and paste into ugreal_obj_mesh
- Download YCB models and paste 00*_** folders into ycb_obj_mesh
- Make sure the textures can be loaded when openening 'scene.blend' in Blender
- Generate a json file using one of the provided templates.

## Usage
The dataset generation can be launched in two ways:
(1) From within Blender using the GUI provided by the Randomizer Plugin (only singlethreaded, prone to crashing, use for testing)
(2) From launch_data_generation.py (supports multiprocessing, multi-GPU). Make sure to install `begins` for your Python Distribution that is used to launch the script (different to the built-in Python)
```
usage: launch_data_generation.py [-h] [--gpus GPUS] [--n-workers N_WORKERS] PARAM_FILE

launches multiple instances of blender to generate synthetic data creates n_workers per selected GPU

positional arguments:
  PARAM_FILE

optional arguments:
  -h, --help            show this help message and exit
  --gpus GPUS, -g GPUS  (default: 0) Select GPUS, e.g. first and second GPU: 0,1
  --n-workers N_WORKERS, -n Number of Workers per GPU
                        (default: 5)
```

## Caveats
- During setup, the script looks for GPUs that include 'nvidia' and 'optix' in their name. Make sure your GPU(s) can be found in Blender. In Blender's GUI: Edit->Preferences in the 'System' Tab, activate Optix Rendering device and check your device names. You can modify device detection in 'Scripting', choose the 'setup' script and make your changes at the bottom of the script.
- Too many background images seem to slow down rendering. However, too little background images and you will loose variety of lighting conditions.

## Extension and Customization
- Edit Randomizing script and settings from within Blender
- To introduce new objects:
	- import mesh into blender
	- define material shading; copy from other objects and make sure it contains the Mix and Shader Node
	- tweak material shading to resemble real object
	- save default material parameters to params within Blender scripting

## View Dataset
```
usage: viewDataset.py PARAM_FILE

Visualization of RGB images with pose annotations. Use the same params file as in data generation
```