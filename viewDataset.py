import json
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import begin



def main(param_file):
    with open(param_file) as F:
        params = json.load(F)

    obj_dict = params['id_dict']
    main_obj = params['main_obj_name']
    img_dir = os.path.join(os.curdir, "blender", params['dataset'], f"{obj_dict[main_obj]:02}")
    
    with open(os.path.join(img_dir, "gt.json")) as F:
        glob_gt = json.load(F)

    cam_matrix = np.array(glob_gt['camera_matrix'])
    print("Found camera matrix:\n", cam_matrix)

    n_images = glob_gt["n_images"]

    alpha_mask = 0.3

    idxs = [int(x.split("_")[1].split(".")[0]) for x in os.listdir(os.path.join(img_dir, "rgb"))]

    np.random.shuffle(idxs)
    
    try:
        for idx in idxs:
            with open(os.path.join(img_dir, "gt", f"gt_{idx:05}.json")) as F:
                shot = json.load(F)
            id = shot['id']
            cam_quat = shot['cam_rotation']

            cam_rot = R.from_quat([*cam_quat[1:], cam_quat[0]]).as_matrix()
            cam_pos = np.array(shot['cam_location'])

            objs = shot['objs']
            rgb = cv2.imread(os.path.join(img_dir, "rgb", f"rgb_{id:04}.png"), cv2.IMREAD_ANYCOLOR).astype(float)
            mask = cv2.imread(os.path.join(img_dir, "mask", f"segmentation_{id:04}.exr"), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

            mask = np.where(mask>0, 1, alpha_mask).astype(float)

            rgb *= mask
            rgb = rgb.astype(np.uint8)

            if rgb is None:
                print(f"Could not load image for {id:04}")
                continue

            assert rgb is not None, f"Could not load image for {id:04}"

            for obj in objs:                
                obj_pos = np.array(obj['pos'])
                quat = obj['rotation']
                obj_rot = R.from_quat([*quat[1:], quat[0]]).as_matrix() # w, x, y, z -> x, y, z, w

                t = cam_rot.T @ (obj_pos - cam_pos)
                RotM = cam_rot.T @ obj_rot

                rotV, _ = cv2.Rodrigues(RotM)
                cv2.drawFrameAxes(rgb, cameraMatrix=cam_matrix, rvec=rotV, tvec=t, distCoeffs=0, length = 0.1)


            print(f"Showing image: {id:04}")
            cv2.imshow(f"Preview", rgb)

            key = cv2.waitKey(0)

            if key == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()



@begin.start
def run(param_file: str):   
    main(param_file)
