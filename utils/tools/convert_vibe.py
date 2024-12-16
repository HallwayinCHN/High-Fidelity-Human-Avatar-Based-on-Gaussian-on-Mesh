import os
import numpy as np
import shutil
import cv2
import argparse
import joblib
from tqdm import tqdm
from utils.util import load_pickle_file, write_pickle_file

def get_opts():
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_root', type=str, default='data/iper',
                        help='people snapshot datasets root')
    parser.add_argument('--people_ID', type=str, default='iper_023_1_1',
                        help='people id')
    parser.add_argument('--gender', type=str, default='neutral',
                        help='gender')

    return parser.parse_args()

if __name__ == "__main__":
    args = get_opts()
    data_root = args.data_root
    people_ID = args.people_ID
    gender = args.gender

    images_dir = os.path.join(data_root, people_ID, 'cam000', 'images')
    smpls_dir = os.path.join(data_root, people_ID, 'smpls')
    if os.path.exists(smpls_dir):
        shutil.rmtree(smpls_dir)
    os.makedirs(smpls_dir, exist_ok=True)

    focal = 2000
    img = cv2.imread(os.path.join(images_dir, '000001.png'))
    H, W = img.shape[:2]

    camera = {
        'R': np.eye(3),
        't': np.zeros(3),
        'camera_f': np.array([focal, focal]),
        'camera_c': np.array([H//2, W//2]),
        'camera_k': np.zeros((5,)),
        'height': H,
        'width': W,
    }
    write_pickle_file(os.path.join(data_root, people_ID, 'cam000', 'camera.pkl'), camera)

    vibe_output = joblib.load(os.path.join(data_root, people_ID, 'vibe_output.pkl'))

    cams = vibe_output[1]['orig_cam']
    betas = vibe_output[1]['betas']
    poses = vibe_output[1]['pose']
    frame_ids = vibe_output[1]['frame_ids']
    #print(frame_ids)
    #检查是否一一对应
    missing_frames = [fid for fid in frame_ids if fid >= len(cams)]

    if missing_frames:
        print(f"缺失的帧索引: {missing_frames}")
    else:
        print("orig_cam 和 frame_ids 长度一致且对应")


    for i in tqdm(range(len(frame_ids)), desc=people_ID):
        frame_id = frame_ids[i]
        cam = cams[frame_id]
        pose = poses[frame_id]

        # #调试
        # print("frame_ids:", frame_ids)
        # print("最大 frame_id:", max(frame_ids))
        # print("cams 的大小:", cams.shape[0])

        beta = betas[frame_id] 
        global_orient = pose[:3]
        body_pose = pose[3:]
        transl = np.array([cam[2], cam[3], 2*focal/(cam[0]*H)])
        
        params = {
            'betas': beta,
            'global_orient': global_orient,
            'body_pose': body_pose,
            'transl': transl,
            'model_type': 'smpl',
            'gender': gender,
        }

        write_pickle_file(os.path.join(smpls_dir, '{:06d}.pkl'.format(frame_id+1)), params)
