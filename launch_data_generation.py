import os
import time

import numpy as np
import subprocess
import signal
from subprocess import Popen, TimeoutExpired
import begin
import json

@begin.start
def main(param_file, gpus='0', n_workers=5, blender_scene='scene_linemod.blend'):
    """ launches multiple instances of blender to generate synthetic data
        creates n_workers per selected GPU
    """
    with open(param_file) as F:
        base_params = json.load(F)
        
    n_frames = base_params["n_frames"]
    resume_from = base_params["resume_from"]

    n_workers = int(n_workers)

    gpus = [int(x) for x in gpus.split(',')]
    n_workers = n_workers * len(gpus)
    if n_workers>1:
        work_distribution = np.array_split(np.arange(resume_from, resume_from+n_frames), n_workers)
    else:
        work_distribution = [np.arange(resume_from, resume_from+n_frames)]

    gpu_inds = np.tile(gpus, n_workers)

    my_env = os.environ
    params = base_params
    param_files = []
    if not os.path.isdir("jobs"):
        os.makedirs("jobs")
    envs = []
    for idx, (inds, gpu) in enumerate(zip(work_distribution, gpu_inds)):
        params['resume_from'] = int(inds[0])
        params['n_frames'] = len(inds)
        params['GPU'] = 0 # int(gpu)
        param_path = os.path.join("jobs", f"job_{idx:02}.json")
        with open(param_path, 'w') as F:
            json.dump(params, F, indent=2)
        param_files.append(param_path)
        env = my_env.copy()
        env['CUDA_VISIBLE_DEVICES'] = str(gpu)
        envs.append(env)

    blender_base_command = f"blender -b {blender_scene} -- "

    commands = [blender_base_command + f"--params {p}" for p in param_files]

    commands = [i.split(' ') for i in commands]

        
    procs = [ Popen(com, shell=False, preexec_fn=os.setsid, env=env) for com,env in zip(commands, envs)]

    t = time.perf_counter()
    try:
        for p in procs:
            p.wait()
    except (KeyboardInterrupt, TimeoutExpired):
        print("Terminating...")
        for p in procs:
            os.killpg(p.pid, signal.SIGINT)
        time.sleep(0.5) # kill again because blender
        for p in procs:
            os.killpg(p.pid, signal.SIGINT)
            
    total = time.perf_counter()-t
    print()
    print()
    print(f"DONE. Total time: {total:.2f}sec ({int(total//3600):02d}h:{int(total//60%60):02d}m:{int(total%60):02d}sec), {total/n_frames} sec/frame, {n_frames/total} frames/sec")
    

