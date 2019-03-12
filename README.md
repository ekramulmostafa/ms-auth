# ms-template

## Conda

### Installation
https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation

### Create new environment
conda create -n {environment-name} python=3.7
ex: conda create -n ms-template python=3.7

### Activate enviroment
source activate {environment-name}
ex: source activate ms-template

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

Ex: docker build -t template:latest .

### Execute container:

docker run --name {service-name} -d -p {mapped-port}:5000 --rm {image-name}:{version} -e ENV_VARS="{Value}"

Ex: docker run -e DATABASE_URL='postgresql://postgres:12345678@host.docker.internal:5433/ms-template' --name template -d -p 8000:5000 --rm template:latest

This will run the service on:
http://localhost:8000/

### Run test:
docker run --entry-point "./test.sh" --name {service-name} --rm {image-name}:{version}
Ex:
docker run --entrypoint "./test.sh" --name template-test --rm template:latest

### Run lint test:
docker run --entry-point "./lint.sh" --name {service-name} --rm {image-name}:{version}
Ex:
docker run --entrypoint "./lint.sh" --name template-lint --rm template:latest

### Stop a container:

docker stop {service-name}

Ex: docker stop template

### Listing all running container:

docker ps

## Code static check
./lint.sh
Make sure you have executable permission on the file. If not provide permission
chmod 755 lint.sh

