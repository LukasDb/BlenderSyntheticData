# Synthetic Dataset Generation using Blender
This project provides a pipeline to create high-quality ray-traced synthetic data using Blender and Python. The images created are independently randomized and all objects and lights are randomly placed and rotated in the camera view. 
The following data is generated (only for objects included in the ID_dict):
- RGB (uint8)
- Depth (float32, in meters)
- Class Segmentation (ID definition in param.json)
- Camera and Object poses (json, in meter and quaternion)
- Camera Intrinsic Matrix
- Stereo Camera Baseline

Data Structure:
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
|	|	|	├── rgb_0001.png
|	|	|	├── ...
|	|	├── gt.json 					-> Intrinsic Matrix, Stereo Baseline
|	|	└── params.json					-> Backup of Generation Parameters
│   ├── 02/
│   ├── 03/
│   └── ...


validateDataset.py provides a showcase how to read and visualize the data.

## Requirements
- Blender 3.3
- Python

## Setup
- Provide background images in the folder 'backgrounds'
- Download LineMod Models and pastte ply files into lm_obj_mesh
- Download ugreal_fg_objects and paste into ugreal_obj_mesh
- Download YCB models and paste 00*_** folders into ycb_obj_mesh
- Make sure the textures can be loaded when openening 'scene.blend' in Blender
- Generate a json file using one of the provided templates.

## Usage
The dataset generation can be launched in two ways:
(1) From within Blender using the GUI provided by the Randomizer Plugin (only singlethreaded, prone to crashing, use for testing)
(2) From launch_data_generation.py (supports multiprocessing, multi-GPU)
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

## Extension and Customization
- Edit Randomizing script and settings from within Blender
- To introduce new objects:
	- import mesh into blender
	- define material shading; copy from other objects and make sure it contains the Mix and Shader Node
	- tweak material shading to resemble real object
	- save default material parameters to params within Blender scripting

## View Dataset
usage: viewDataset.py PARAM_FILE

Visualization of RGB images with pose annotations. Use the same params file as in data generation
