# easy-kubeflow

python sdk for kubeflow platform. use following func in .ipynb file

## docker

examples for use of docker

### initial

init docker client

Similar to cmd line ``docker login``

```python
from easy_kubeflow import EasyDocker
docker = EasyDocker()

2022-03-22 01:39:02.933 [INFO] Connected to host docker successfully !
```
### show images

show images in container's host node.

Similar to cmd line ``docker images | grep xxx``. when name none, show all images

```python
docker.show_images(grep="liuweibin")

REPOSITORY + TAG	IMAGE ID	CREATED	SIZE
harbor.stonewise.cn/kubeflow/liuweibin/notebook-image:base	f621486595fe	2022-03-17T02:02:18.143	8.1 GB
harbor.stonewise.cn/kubeflow/liuweibin/notebook-image:test	8491b7b97d72	2022-01-21T10:13:34.857	8.1 GB
```

### pull images

pull images from service.stonewise.cn:5000/ or harbor or harbor proxy (recommend)

Similar to cmd line ``docker pull xxx``

```python
docker.pull_images(repository="harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount", 
                   tag="0.0.3")

  0%|          | 0/3 [00:00<?, ?it/s]2022-03-22 01:53:12.543 [INFO] Pulling from proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount
 33%|███▎      | 1/3 [00:00<00:00,  9.84it/s]2022-03-22 01:53:12.646 [INFO] Digest: sha256:189270b1726e6764ebbcdfa72f1ba80fa8bc3945712afadc1adadfd3dfb741b4
 67%|██████▋   | 2/3 [00:00<00:00,  9.75it/s]2022-03-22 01:53:12.749 [INFO] Status: Downloaded newer image for harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount:0.0.3
100%|██████████| 3/3 [00:00<00:00,  9.69it/s]
2022-03-22 01:53:12.854 [INFO] Pull image successfully !
```

### tag images

tag images in container's host node.

```python
docker.tag_images(original_repository="harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount", 
                  original_tag="0.0.3",
                  target_repository="service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount", 
                  target_tag="0.0.3"
                 )

2022-03-22 02:03:55.017 [INFO] Tag repository successfully !

docker.show_images(grep="service.stonewise.cn")

REPOSITORY + TAG	IMAGE ID	CREATED	SIZE
service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount:0.0.3	d3838c66fc1e	2022-03-14T02:19:02.010	1.0 GB
```
### push images

push images to service.stonewise.cn:5000/ or harbor (recommend)

Similar to cmd line ``docker push xxx``

```python
docker.push_images(repository="service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount", 
                   tag="0.0.3")

  0%|          | 0/793 [00:00<?, ?it/s]2022-03-23 06:52:54.661 [INFO] The push refers to repository [service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount]
  0%|          | 1/793 [00:00<01:20,  9.83it/s]2022-03-23 06:52:54.764 [INFO] Preparing
  0%|          | 2/793 [00:00<01:21,  9.76it/s]2022-03-23 06:52:54.867 [INFO] Waiting
  3%|▎         | 20/793 [00:00<00:09, 85.39it/s]2022-03-23 06:52:54.970 [INFO] Pushing
  4%|▍         | 31/793 [00:00<00:08, 94.05it/s]2022-03-23 06:52:55.072 [INFO] Pushed
2022-03-23 06:52:55.173 [INFO] Pushing
  5%|▌         | 41/793 [00:00<00:10, 70.32it/s]2022-03-23 06:52:55.276 [INFO] Pushed
2022-03-23 06:52:55.377 [INFO] Pushing
  6%|▌         | 49/793 [00:00<00:13, 56.90it/s]2022-03-23 06:52:55.480 [INFO] Pushed
  8%|▊         | 60/793 [00:00<00:10, 68.78it/s]2022-03-23 06:52:55.583 [INFO] Pushing
2022-03-23 06:52:55.684 [INFO] Pushed
2022-03-23 06:52:55.786 [INFO] Pushing
  9%|▊         | 68/793 [00:01<00:15, 47.38it/s]2022-03-23 06:52:55.889 [INFO] Pushed
 10%|█         | 80/793 [00:01<00:11, 60.79it/s]2022-03-23 06:52:55.993 [INFO] Pushing
2022-03-23 06:52:56.095 [INFO] Pushed
2022-03-23 06:52:56.196 [INFO] Pushing
 11%|█         | 88/793 [00:01<00:15, 45.07it/s]2022-03-23 06:52:56.300 [INFO] Pushed
 50%|████▉     | 393/793 [00:01<00:00, 564.44it/s]2022-03-23 06:52:56.403 [INFO] Pushing
2022-03-23 06:52:56.504 [INFO] Pushed
2022-03-23 06:52:56.605 [INFO] Pushing
2022-03-23 06:52:56.707 [INFO] Pushed
2022-03-23 06:52:56.809 [INFO] Pushing
2022-03-23 06:52:56.910 [INFO] Pushed
2022-03-23 06:52:57.012 [INFO] Pushing
 62%|██████▏   | 488/793 [00:02<00:01, 289.57it/s]2022-03-23 06:52:57.115 [INFO] Pushed
2022-03-23 06:52:57.216 [INFO] Pushing
 70%|███████   | 558/793 [00:02<00:00, 300.54it/s]2022-03-23 06:52:57.320 [INFO] Pushed
 80%|███████▉  | 632/793 [00:02<00:00, 354.68it/s]2022-03-23 06:52:57.423 [INFO] Pushing
 88%|████████▊ | 695/793 [00:02<00:00, 394.87it/s]2022-03-23 06:52:57.526 [INFO] Pushed
2022-03-23 06:52:57.627 [INFO] Pushing
 96%|█████████▌| 758/793 [00:03<00:00, 368.36it/s]2022-03-23 06:52:57.730 [INFO] Pushed
2022-03-23 06:52:57.831 [INFO] 0.0.3: digest: sha256:189270b1726e6764ebbcdfa72f1ba80fa8bc3945712afadc1adadfd3dfb741b4 size: 4079
2022-03-23 06:52:57.933 [INFO] {}
100%|██████████| 793/793 [00:03<00:00, 235.06it/s]
2022-03-23 06:52:58.036 [INFO] Push image successfully !
```

### build images

build images for harbor or service.stonewise.cn:5000/

Similar to cmd line ``docker build -f Dockerfile -t xxx ./``

`tips:` use this fun in the same dir as Dockerfile, no extra file (or data file in the same dir)

```python
docker.build_images(path="/home/jovyan/image",
                    dockerfile="Dockerfile",
                    repository="service.stonewise.cn:5000/standalone-training",tag="0.0.1")

  0%|          | 0/14 [00:00<?, ?it/s]2022-03-23 07:35:22.763 [INFO] Step 1/3 : FROM harbor-qzm.stonewise.cn/proxy_cache/kubeflow/tensorflow:1.14.0-py3.6-cpu
  7%|▋         | 1/14 [00:00<00:01,  9.88it/s]2022-03-23 07:35:22.866 [INFO] 
 14%|█▍        | 2/14 [00:00<00:01,  9.75it/s]2022-03-23 07:35:22.970 [INFO]  ---> 3519b2e83423
 21%|██▏       | 3/14 [00:00<00:01,  9.73it/s]2022-03-23 07:35:23.073 [INFO] Step 2/3 : ADD main.py .
 29%|██▊       | 4/14 [00:00<00:01,  9.71it/s]2022-03-23 07:35:23.176 [INFO] 
 36%|███▌      | 5/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.279 [INFO]  ---> 755d86598819
 43%|████▎     | 6/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.382 [INFO] Step 3/3 : ENTRYPOINT ["python3", "main.py"]
 50%|█████     | 7/14 [00:00<00:00,  9.70it/s]2022-03-23 07:35:23.485 [INFO] 
 57%|█████▋    | 8/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.588 [INFO]  ---> Running in 0438ef9bc950
 64%|██████▍   | 9/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.691 [INFO] Removing intermediate container 0438ef9bc950
 71%|███████▏  | 10/14 [00:01<00:00,  9.71it/s]2022-03-23 07:35:23.794 [INFO]  ---> 9a41289aed98
 79%|███████▊  | 11/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:23.897 [INFO] {'ID': 'sha256:9a41289aed98e3e715fd91a21625c621dd697e49d632e2e06d3564bfc77c5e88'}
 86%|████████▌ | 12/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:24.000 [INFO] Successfully built 9a41289aed98
 93%|█████████▎| 13/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:24.103 [INFO] Successfully tagged service.stonewise.cn:5000/standalone-training:0.0.1
100%|██████████| 14/14 [00:01<00:00,  9.70it/s]
2022-03-23 07:35:24.208 [INFO] Build image successfully !

docker.push_images(repository="service.stonewise.cn:5000/standalone-training", tag="0.0.1")

  0%|          | 0/525 [00:00<?, ?it/s]2022-03-23 07:37:37.084 [INFO] The push refers to repository [service.stonewise.cn:5000/standalone-training]
  0%|          | 1/525 [00:00<00:53,  9.88it/s]2022-03-23 07:37:37.186 [INFO] Preparing
  0%|          | 2/525 [00:00<00:53,  9.81it/s]2022-03-23 07:37:37.289 [INFO] Waiting
  2%|▏         | 11/525 [00:00<00:11, 45.49it/s]2022-03-23 07:37:37.392 [INFO] Pushing
  3%|▎         | 16/525 [00:00<00:10, 46.73it/s]2022-03-23 07:37:37.495 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
2022-03-23 07:37:37.596 [INFO] Pushing
2022-03-23 07:37:37.698 [INFO] Pushed
  4%|▍         | 21/525 [00:00<00:18, 27.66it/s]2022-03-23 07:37:37.800 [INFO] Pushing
2022-03-23 07:37:37.902 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
  5%|▍         | 25/525 [00:00<00:20, 24.64it/s]2022-03-23 07:37:38.005 [INFO] Pushing
2022-03-23 07:37:38.106 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
2022-03-23 07:37:38.207 [INFO] Pushing
  6%|▌         | 29/525 [00:01<00:25, 19.51it/s]2022-03-23 07:37:38.310 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
2022-03-23 07:37:38.412 [INFO] Pushing
  6%|▌         | 32/525 [00:01<00:27, 18.07it/s]2022-03-23 07:37:38.516 [INFO] Pushed
100%|█████████▉| 523/525 [00:01<00:00, 854.64it/s]2022-03-23 07:37:38.620 [INFO] 0.0.1: digest: sha256:0fe6eaa12c2e4409f2b20f089dca83e8f0b4480b60405dcbb102a00185b2070c size: 2215
2022-03-23 07:37:38.721 [INFO] {}
100%|██████████| 525/525 [00:01<00:00, 301.85it/s]
2022-03-23 07:37:38.825 [INFO] Push image successfully !
```

### commit containers

commit containers to images in  harbor or service.stonewise.cn:5000/

Similar to cmd line ``docker commit <container_id> xxx``

if `push_image=True` committed image will be pushed

```python
docker.commit_containers(
    container="e96742819503",
    repository="service.stonewise.cn:5000/notebook-server",
    tag="base",
    push_image=True
)

2022-04-06 10:58:31.417 [INFO] Commit container sucessfully !
  0%|          | 0/5561 [00:00<?, ?it/s]2022-04-06 11:02:32.232 [INFO] The push refers to repository [service.stonewise.cn:5000/notebook-server]
  0%|          | 1/5561 [00:00<09:24,  9.86it/s]2022-04-06 11:02:32.336 [INFO] Preparing
  0%|          | 2/5561 [00:00<09:28,  9.77it/s]2022-04-06 11:02:32.438 [INFO] Waiting
  0%|          | 23/5561 [00:00<00:56, 98.81it/s]2022-04-06 11:02:32.541 [INFO] Preparing
2022-04-06 11:02:32.642 [INFO] Waiting
2022-04-06 11:02:32.744 [INFO] Preparing
2022-04-06 11:02:32.846 [INFO] Waiting
2022-04-06 11:02:32.947 [INFO] Preparing
  1%|          | 33/5561 [00:00<02:24, 38.30it/s]2022-04-06 11:02:33.051 [INFO] Waiting
2022-04-06 11:02:33.152 [INFO] Preparing
2022-04-06 11:02:33.253 [INFO] Waiting
  1%|          | 40/5561 [00:01<02:51, 32.20it/s]2022-04-06 11:02:33.356 [INFO] Preparing
2022-04-06 11:02:33.457 [INFO] Waiting
2022-04-06 11:02:33.559 [INFO] Preparing
  1%|          | 46/5561 [00:01<03:19, 27.66it/s]2022-04-06 11:02:33.662 [INFO] Waiting
2022-04-06 11:02:33.763 [INFO] Preparing
2022-04-06 11:02:33.865 [INFO] Waiting
  1%|          | 51/5561 [00:01<03:51, 23.81it/s]2022-04-06 11:02:33.968 [INFO] Pushing
  1%|          | 66/5561 [00:01<02:14, 40.96it/s]2022-04-06 11:02:34.071 [INFO] Pushed
  2%|▏         | 86/5561 [00:01<01:22, 66.65it/s]2022-04-06 11:02:34.173 [INFO] Pushing
  2%|▏         | 97/5561 [00:02<01:13, 74.45it/s]2022-04-06 11:02:34.276 [INFO] Pushed
  2%|▏         | 113/5561 [00:02<00:59, 92.01it/s]2022-04-06 11:02:34.379 [INFO] Pushing
2022-04-06 11:02:34.480 [INFO] Pushed
2022-04-06 11:02:34.581 [INFO] Pushing
  2%|▏         | 126/5561 [00:02<01:19, 68.38it/s]2022-04-06 11:02:34.684 [INFO] Pushed
  3%|▎         | 148/5561 [00:02<00:56, 95.62it/s]2022-04-06 11:02:34.787 [INFO] Pushing
2022-04-06 11:02:34.888 [INFO] Pushed
2022-04-06 11:02:34.989 [INFO] Pushing
  3%|▎         | 162/5561 [00:02<01:13, 73.56it/s]2022-04-06 11:02:35.093 [INFO] Pushed
  3%|▎         | 178/5561 [00:02<01:01, 87.92it/s]2022-04-06 11:02:35.195 [INFO] Pushing
2022-04-06 11:02:35.297 [INFO] Pushed
2022-04-06 11:02:35.398 [INFO] Pushing
2022-04-06 11:02:35.500 [INFO] Pushed
2022-04-06 11:02:35.601 [INFO] Pushing
  3%|▎         | 191/5561 [00:03<01:40, 53.42it/s]2022-04-06 11:02:35.704 [INFO] Pushed
  4%|▎         | 204/5561 [00:03<01:24, 63.47it/s]2022-04-06 11:02:35.807 [INFO] Pushing
2022-04-06 11:02:35.908 [INFO] Pushed
2022-04-06 11:02:36.009 [INFO] Pushing
2022-04-06 11:02:36.111 [INFO] Pushed
2022-04-06 11:02:36.212 [INFO] Pushing
  4%|▍         | 215/5561 [00:04<02:04, 42.83it/s]2022-04-06 11:02:36.315 [INFO] Pushed
  4%|▍         | 230/5561 [00:04<01:35, 55.73it/s]2022-04-06 11:02:36.417 [INFO] Pushing
2022-04-06 11:02:36.518 [INFO] Pushed
2022-04-06 11:02:36.620 [INFO] Pushing
2022-04-06 11:02:36.721 [INFO] Pushed
  4%|▍         | 240/5561 [00:04<02:04, 42.87it/s]2022-04-06 11:02:36.824 [INFO] Pushing
  4%|▍         | 248/5561 [00:04<01:52, 47.43it/s]2022-04-06 11:02:36.926 [INFO] Pushed
  5%|▍         | 257/5561 [00:04<01:38, 53.71it/s]2022-04-06 11:02:37.029 [INFO] Pushing
2022-04-06 11:02:37.131 [INFO] Pushed
2022-04-06 11:02:37.232 [INFO] Pushing
  5%|▍         | 266/5561 [00:05<02:00, 43.99it/s]2022-04-06 11:02:37.336 [INFO] Pushed
  8%|▊         | 430/5561 [00:05<00:17, 293.56it/s]2022-04-06 11:02:37.438 [INFO] Pushing
2022-04-06 11:02:37.540 [INFO] Pushed
2022-04-06 11:02:37.641 [INFO] Pushing
  9%|▊         | 483/5561 [00:05<00:20, 244.70it/s]2022-04-06 11:02:37.749 [INFO] Pushed
 32%|███▏      | 1767/5561 [00:05<00:01, 2223.95it/s]2022-04-06 11:02:37.852 [INFO] Pushing
2022-04-06 11:02:37.954 [INFO] Pushed
2022-04-06 11:02:38.055 [INFO] Pushing
2022-04-06 11:02:38.158 [INFO] Pushed
2022-04-06 11:02:38.259 [INFO] Pushing
2022-04-06 11:02:38.361 [INFO] Pushed
2022-04-06 11:02:38.462 [INFO] Pushing
 39%|███▊      | 2153/5561 [00:06<00:02, 1187.40it/s]2022-04-06 11:02:38.568 [INFO] Pushed
 49%|████▉     | 2730/5561 [00:06<00:01, 1680.97it/s]2022-04-06 11:02:38.671 [INFO] Pushing
2022-04-06 11:02:38.772 [INFO] Pushed
2022-04-06 11:02:38.874 [INFO] Pushing
2022-04-06 11:02:38.976 [INFO] Pushed
2022-04-06 11:02:39.077 [INFO] Pushing
2022-04-06 11:02:39.179 [INFO] Pushed
2022-04-06 11:02:39.281 [INFO] Pushing
2022-04-06 11:02:39.383 [INFO] Pushed
2022-04-06 11:02:39.484 [INFO] Pushing
2022-04-06 11:02:39.587 [INFO] Pushed
2022-04-06 11:02:39.689 [INFO] Pushing
 56%|█████▌    | 3095/5561 [00:07<00:03, 818.68it/s] 2022-04-06 11:02:39.795 [INFO] Pushed
 71%|███████   | 3930/5561 [00:07<00:01, 1377.31it/s]2022-04-06 11:02:39.898 [INFO] Pushing
 78%|███████▊  | 4353/5561 [00:07<00:00, 1644.97it/s]2022-04-06 11:02:40.005 [INFO] Pushed
 94%|█████████▎| 5201/5561 [00:07<00:00, 2452.10it/s]2022-04-06 11:02:40.109 [INFO] Pushing
2022-04-06 11:02:40.210 [INFO] Pushed
2022-04-06 11:02:40.312 [INFO] Pushing
2022-04-06 11:02:40.414 [INFO] Pushed
2022-04-06 11:02:40.516 [INFO] base: digest: sha256:60ae6bf7977b719155119ae9eb0e36605227bb867a97b612a4d3f437e3bf9410 size: 7864
2022-04-06 11:02:40.618 [INFO] {}
100%|██████████| 5561/5561 [00:08<00:00, 655.23it/s] 
2022-04-06 11:02:40.725 [INFO] Push image successfully !
```