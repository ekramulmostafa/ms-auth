# ms-auth

## Conda

### Installation
https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation

### Create new environment
conda create -n {environment-name} python=3.7
ex: conda create -n ms-auth python=3.7

### Activate enviroment
source activate {environment-name}
ex: source activate ms-auth

### Deactivate enviroment
source deactivate

### Running app
python manage.py run

### Running test
python manage.py test

### Running lint
./lint.sh


## Container

### Installation
https://www.docker.com/products/docker-desktop
### Building a image:

docker build -t {image-name}:{version} .

Ex: docker build -t auth:latest .

### Execute container:

docker run -e ENV_VARS="{Value}" --name {service-name} -d -p {mapped-port}:5000 --rm {image-name}:{version} ./boot.sh

Ex: docker run -e DATABASE_URL='postgresql://postgres:12345678@host.docker.internal:5433/ms-auth' --name auth -d -p 8000:5000 --rm auth:latest ./boot.sh

This will run the service on:
http://localhost:8000/

### Run test:
docker run --entry-point "./test.sh" --name {service-name} --rm {image-name}:{version} ./test.sh
Ex:
docker run --name auth-test --rm auth:latest ./test.sh

### Run lint test:
docker run --entry-point "./lint.sh" --name {service-name} --rm {image-name}:{version} ./lint.sh
Ex:
docker run --name auth-lint --rm auth:latest ./lint.sh

### Stop a container:

docker stop {service-name}

Ex: docker stop auth

### Listing all running container:

docker ps

## Code static check
./lint.sh
Make sure you have executable permission on the file. If not provide permission
chmod 755 lint.sh

