# Speeding Up Your Dockerized Development Workflow

## Problem Statement:

Development in Docker locally can be a big pain. It is slow. A developer is waiting a painful amount of time for the container to restart after every small code change.

## Solution:

What if there was a way to bind mounts to share your project directory with a running container so that you can reuse your dev Docker image more frequently in a painless manner? Continue reading to find out how!

### Place Your Project Directory Into Docker

Typically, your developement environment should be designed for fast iterations. However, with Docker, many believe you must create a complete Docker image when deploying your code in the dev environment. That's not needed.

Instead, you can share your code with a started container by using [bind mounts](https://docs.docker.com/storage/bind-mounts/) This'll prevent you from creating a new image on each code change.

By design, Docker containers do not store persistent data. Any data written to a container's writable layer will no longer be available once the container stops running. Also, getting data written to a container back out of it for another process can be difficult. To solve the issue of persisting data from a container, Docker has two options.

Bind mounts: A bind mount is a file or folder stored anywhere on the container host filesystem, mounted into a running container. The main difference a bind mount has from a volume is that since it can exist anywhere on the host filesystem, processes outside of Docker can also modify it. 

![mount bind](https://docs.docker.com/storage/images/types-of-mounts-bind.png)

Volumes: Volumes are the preferred way to store persistent data Docker containers create or use. The host filesystem also stores volumes, similar to bind mounts. However, Docker completely manages them and stores them under C:\ProgramData\docker\volumes by default. 

![volume](https://i.ytimg.com/vi/6rKg9xuWr5Q/maxresdefault.jpg)

When starting a new container using Docker CLI, here's how you mount a local "./source_dir":
  
   **Mounting Ubuntu host directory to docker (For Ubuntu):**
  
  > $ docker run -it -v "$(pwd)/source_dir:/app/target_dir" ubuntu bash
  
  > $ docker run -it --mount "type=bind,source=$(pwd)/source_dir,target=/app/target_dir" ubuntu bash
  
   **Mounting Windows host directory to docker (For Windows):**
   
   Local path mounting is not possible without enabling [file share](https://docs.docker.com/docker-for-windows/#file-sharing) on Windows. The File sharing tab is only available in Hyper-V mode, because in WSL 2 mode and Windows container mode all files are automatically shared by Windows.
   
   > docker run --mount type=bind,source="%CD%\ames_dataset",target=/mnt/data -it datapreparation --input-file-path=/mnt/data --output-train-path=/tmp/train.csv --output-test-path=/tmp/test.csv
    
To bind mount, you can provide it an absolute path to a host directory and direct where it should be mounted inside the container once you've coloned using **--mount.**

Further, to be more efficient, you may consider utilizing **docker-compose** and using **docker-compose.yml** files to configure the Docker container. The goal is to use bind mounts to share your project directory with a running container. This will allow you to reuse your development Docker image with every code iteration and a lot more frequently. The content of the local directory overwrites the content from the image when the container has started. All you need to do is build the image once with the required dependencies and OS requirements until either dependencies or OS versions have change (this can be done with a requirements.txt file too). Otherwise, there's no need to recreate a new image when you modify your code.

Here's an example of creating a new file in a common folder and by running docker-compose up it will exit the container. This can be done like this:

(A simple example of a docker-compose.yml file to mount a local directory)
    
    > Version: '3'
    
    > Services:
       
       > example
    
    > image: ubuntu
    
    > volumes:
    
      > - ./source_dir:/app/target_dir
      
    > command: touch /app/target_dir/hello
    
Thus, when building with Docker in your dev environment, you can see results right away by using bind mounts to share code between your local machine and the Docker container. This will ensure that you will no longer need to rebuild your Docker image in development for every small code change. 

This makes iterating a lot faster and makes local developement experience better!
