# High-Fidelity-Human-Avatar-Based-on-Gaussian-on-Mesh
> WANG Haowei, XU Xinmu, YANG Can

## Related Paper or Project
> [SplattingAvatar: Realistic Real-Time Human Avatars with Mesh-Embedded Gaussian Splatting](https://arxiv.org/abs/2403.05087)
>   
> Zhijing Shao, Zhaolong Wang, Zhuang Li, Duotun Wang, Xiangru Lin, Yu Zhang, Mingming Fan, Zeyu Wang

> [Animatable Neural Radiance Fields from Monocular RGB Videos](https://arxiv.org/abs/2106.13629)
>   
> Jianchuan Chen, Ying Zhang, Di Kang, Xuefei Zhe, Linchao Bao, Xu Jia, Huchuan Lu

> [Video based reconstruction of 3D people models](https://arxiv.org/abs/1803.04758)
> 
> Thiemo Alldieck, Marcus Magnor, Weipeng Xu, Christian Theobalt, Gerard Pons-Moll

> [Robust High-Resolution Video Matting with Temporal Guidance](https://arxiv.org/abs/2108.11515)
> 
> Shanchuan Lin, Linjie Yang, Imran Saleemi, Soumyadip Sengupta

> [InstantAvatar: Learning Avatars from Monocular Video in 60 Seconds](https://arxiv.org/abs/2212.10550)
> 
> Tianjian Jiang, Xu Chen, Jie Song, Otmar Hilliges

- Anim-NeRF
- InstantAvatar
- videoavatars
- RobustVideoMatting

## Requirements
- Python3.7 or later
- [PyTorch](https://pytorch.org/) 1.6 or later
- Pytorch-lightning
- [KNN_CUDA](https://github.com/unlimblue/KNN_CUDA)

### For visualization
- pyrender
- Trimesh
- PyMCubes
  
Run the following code to install all pip packages:
```sh
pip install -r requirements.txt
```

To install [KNN_CUDA](https://github.com/unlimblue/KNN_CUDA), we provide two ways:
* from source
  ```sh
  git clone https://github.com/unlimblue/KNN_CUDA.git
  cd KNN_CUDA
  make && make install
  ```
* from wheel
  ```sh
  pip install --upgrade https://github.com/unlimblue/KNN_CUDA/releases/download/0.2/KNN_CUDA-0.2-py3-none-any.whl
  ```

### SMPL models
To download the *SMPL* model go to [this](http://smpl.is.tue.mpg.de) (male, female and neutral models).

**Place them as following:**
```bash
smplx
└── models
    └── smpl
        ├── SMPL_FEMALE.pkl
        ├── SMPL_MALE.pkl
        └── SMPL_NEUTRAL.pkl
```

## Data Preparation
### iPER datasets or Custom datasets
* Prepare images

  First convert video to images, and crop the images to make the person as centered as possible.
  ```sh
  python -m tools.video_to_images --vid_file Anim-nerf-fyp/Anim-NeRF/data/iper/iper_yc/female_1_1.mp4 --output_folder Anim-nerf-fyp/Anim-NeRF/data/iper/iper_yc/cam000/images --img_wh 1080 1080 --offsets 0 0
  ```

* Images segmentation

  Here, we use [RVM](https://github.com/PeterL1n/RobustVideoMatting) to extact the foreground mask of the person.
  ```sh
  python -m tools.rvm --images_folder Anim-nerf-fyp/Anim-NeRF/data/iper/iper_yc/cam000/images --output_folder Anim-nerf-fyp/Anim-NeRF/data/iper/iper_yc/cam000/images
  ```

* SMPL estimation

  In our experiment, we use [VIBE](https://github.com/mkocabas/VIBE) to estimate the smpl parameters.
  ```sh
  python -m tools.vibe --images_folder data/iper/iper_yc/cam000/images --output_folder data/iper/iper_yc
  ```
  Then convert **vibe_output.pkl** to the format in our experiment setup.
  ```sh
  python -m tools.convert_vibe --data_root Anim-nerf-fyp/Anim-NeRF/data/iper --people_ID iper_yc --gender neutral
  ```

* Prepare template
  ```sh
  python -m tools.prepare_template --data_root Anim-nerf-fyp/Anim-NeRF/data/iper --people_ID iper_yc --model_type smpl --gender neutral --model_path Anim-nerf-fyp/Anim-NeRF/smplx/models
  ```

## Training
- Training on the training frames
  ```sh
  python train.py --cfg_file configs/iper/iper_yc.yaml
  ```
- Finetuning the smpl params on the testing frames
  ```sh
  python train.py --cfg_file configs/iper/iper_yc_refine.yaml train.ckpt_path checkpoints/iper/last.ckpt
  ```
Here, you should try the first command and modify the yaml file as you wish; Then run the second one and modify the refine yaml file as you wish (train and test frames are both use this)

## Acknowledgements
We would like to express my deepest gratitude to my supervisor, Dr. Xiao Dong, for her invaluable advice and guidance throughout this project. Her insights and encouragement were instrumental in bringing this work to fruition. We are also profoundly grateful to Mr. Sen Peng for his technical and theoretical clarifications, which greatly contributed to the success of this project. His expertise and willingness to assist were truly invaluable. Furthermore, we would like to extend our heartfelt thanks to our school BNU-HKBU UIC for providing the necessary resources and a conducive environment for this research. The support and facilities offered by the university played a critical role in the completion of this work. Lastly, great thanks go to our family for their unwavering support and understanding. Their encouragement and patience were essential in enabling us to focus on and complete this project. 

Also, great thanks go to those projects which functioned as backend of our projects!
