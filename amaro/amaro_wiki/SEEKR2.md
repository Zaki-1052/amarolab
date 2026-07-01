# SEEKR2

Docker: 

`docker run --rm -ti --gpus device=1 -u "$(id -u)":"$(id -g)" -v "$PWD":/home/seekr2/data -w /home/seekr2/data seekr2`

**\--rm** Automatically remove the container when it exits 

**-ti** Runs container in foreground with a pseudo-tty 

**\--gpus device=X,Y,Z** Specifies which GPU(s) to use in the container. The device ID is obtained by running nvidia-smi on the host system. Set to **\--gpus all** to expose all GPUs on the host system to the container. 

**-u "$(id -u)":"$(id -g)"** Takes the uid and gid of the current user on the host system and passes it to the container. This is useful to keep your hosts system uid/gid while working in the container. This allows you to write to the host system's mount that you specified with -v, provided that you have write access to that area of the filesystem. 

**-v "$PWD":/home/seekr2/data** Mount the current working directory on the host system to /home/seekr2/data in the container 

**-w /home/seekr2/data** Set /home/seekr2/data as the entry point when the container is launched. 

**seekr2** Name of Docker image 

  
Notes: 

When you enter the container, you will see something like: 

`groups: cannot find name for group ID 704022404 I have no name!@241b97218b29:/home/seekr2/data$`

This is due to the container not knowing the host user's uid and gid mappings. This can be ignored.
