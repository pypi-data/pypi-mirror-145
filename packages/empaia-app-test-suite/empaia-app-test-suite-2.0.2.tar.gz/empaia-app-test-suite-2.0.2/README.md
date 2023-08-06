# EMPAIA App Test Suite (EATS)

## Requirements

* The EMPAIA App Test Suite requires Python 3.8.
* Supported Operating Systems are Linux, Windows and MacOS
  * for **Windows** the EATS requires the usage of WSL 2 (Windows Subsystem for Linux) with Docker for Windows
  
## Installation

There are different possibilities to install the EMPAIA App Test Suite depending on your intended use:

* Installation as App Developer
  * Latest stable release
  * Latest test release
* Build and installation as EATS Developer

### Installation as App Developer - Latest stable release

Installation via `pip` from Python Package Index (PyPI).

```bash
# create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# install with pip
pip install empaia-app-test-suite
```

### Installation as App Developer - Latest test release

Installation via `pip` from Python Package Index Test Repository (Test.PyPI).

```bash
# create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# install with pip from test.pypi.org
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ empaia-app-test-suite
```

### Build and installation as EATS Developer

Clone the EATS source code repository.

This module uses submodules, i.e. references to other git repositories. Add `--recurse-submodule` to your clone command to also get all submodules, e.g.

```bash
git clone --recurse-submodule https://gitlab.cc-asp.fraunhofer.de/empaia/app-test-suite/empaia-app-test-suite.git
cd empaia-app-test-suite
### also after changing branch
git submodule update --init --recursive
```

Build the EATS CLI app and install all needed dependencies:

```bash
# create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# build / install EATS and dependencies
poetry install
```

## Run EATS

Run the EATS CLI app with

```bash
eats
```

To force pull and build services and submodules:

```bash
eats services up ./wsi-mount-points.json --build --pull
```

## Usage

**For detailed instructions take a look at the [App Developer Documentation](https://developer.empaia.org/app_developer_docs/#/)**

Define absolute paths to directories containing WSIs in a `./wsi-mount-points.json` file as follows:

```json
{
    "/absolute/local/path/to/wsis/dir1": "/absolute/container/mount/dir1/",
    "/absolute/local/path/to/wsis/dir2": "/absolute/container/mount/dir2/"
}
```

Start all backend services in Docker containers using the `eats services up` command. WSI directories are mounted into the WSI Service container. Only WSIs contained in one of the specified directories can be used as a job input.

```bash
eats services up ./wsi-mount-points.json
```

You can perform health checks of running backend services.

```bash
eats services health
```

Register your app with its `<docker-image-name>` (can be fully qualified docker registry url, e.g. `registry.gitlab.com/empaia/integration/sample-apps/org-empaia-vendor_name-tutorial_app_01:v1`). Also provide the path to you `ead.json`. If your app required configuration parameters, use the `--config-file` flag to specify the path to you `configuration.json`.

```bash
eats apps register <path-to-ead.json> <docker-image-name>
```

resp.

```bash
eats apps register <path-to-ead.json> <docker-image-name> --config-file <path-to-configuration.json> > app.env
export $(xargs <job.env)
echo $APP_ID
```

Use the APP_ID together with your JSON files for your data inputs in a `job-inputs` directory to register ar new job.

```bash
eats jobs register <path-to-job-inputs> $APP_ID --v1 > ./job.env
```

The generated `job.env` file contains the `EMPAIA_JOB_ID`, `EMPAIA_TOKEN`, and `EMPAIA_APP_API` environment variables, that are handed to your app during the `eats jobs run` step.

```bash
eats jobs run ./job.env
```

The job ID can be retrieved from the `job.env` file to be used in other commands.

```bash
export $(xargs <job.env)
echo $EMPAIA_JOB_ID
```

Regularly check the jobs status until it is `COMPLETED`.

```bash
eats jobs status ${EMPAIA_JOB_ID}
```

The job ID is used as the container name. It can be used to retrieved docker logs.

```bash
docker logs ${EMPAIA_JOB_ID}
```

Open `localhost:8080` in a Browser to review job results using the EATS Web Client.

In addition, the job results can be exported to JSON files in a `job-outputs` directory.

```bash
eats jobs export ${EMPAIA_JOB_ID} ./job-outputs
```

If a job is taking too long or is stuck, the job can be aborted.

```bash
eats jobs abort ${EMPAIA_JOB_ID}
```

To inspect backend service logs the `docker logs` command can used directly. The names of all service containers can be retrieved using the `eats services containers` command.

```bash
eats services list  # print list of service names
docker logs ${SERVICE_NAME}
```

It is possible to register and run multiple jobs without restart backend services. The services can be stopped, if they are not needed anymore.

```bash
eats services down
```

To erase all cached data of service databases `docker volume rm` can be used directly.

```bash
docker volume rm $(eats services volumes)
```

## Executing Your App without Job Execution Service

The command `eats jobs run $EMPAIA_JOB_ID <job.env-file>` sends a request to the Job Execution Service, which start your containerized app. Debugging your app this way can be tedious and time consuming. To speed up the debugging process, you can also start your app natively:

1. Start services as usual.

```bash
eats services up ./wsi-mount-points.json
```

2. Register app as usual, receiving the `APP_ID`

```bash
eats apps register <path-to-ead.json> <docker-image-name> --config-file <path-to-configuration.json> > app.env
export $(xargs <app.env)
echo $APP_ID
```

3. Register job and export to `job.env`, e.g.

```bash
eats jobs register $APP_ID <eats-inputs-folder> --v1 > job.env
export $(xargs <job.env)
echo $EMPAIA_JOB_ID
```

4. Overwrite the `EMPAIA_APP_API` value with `localhost:<NGINX-PORT>/app-api` (the exposed port of the NGINX proxy server is `8888` by default):

```bash
export EMPAIA_APP_API=http://localhost:8888/app-api
```

5. Set job to status `RUNNING` (without actually running it):

```bash
eats jobs set-running $EMPAIA_JOB_ID
```

6. Run your app, e.g.:

```bash
python3 <path-to-app.py>
```

7. Make changes to your app.py and **GO TO 3.**

## For EATS Developers

### Code Checks

Check your code before committing.

* always format code with `black` and `isort`
* check code quality using `pycodestyle` and `pylint`
  * `black` formatting should resolve most issues for `pycodestyle`

```bash
isort .
black empaia_app_test_suite tests check_version.py
pycodestyle empaia_app_test_suite tests check_version.py
pylint empaia_app_test_suite tests check_version.py
```

### Tests

Create `./wsi-mount-points.json`:

```JSON
{
  "/path/to/testdata/Aperio/": "/data",
  "/path/to/testdata/Fluorescence OME-Tif/": "/data2"
}
```

```bash
eats services up ./wsi-mount-points.json --build --pull

# run cli command tests
pytest tests/commands --maxfail=1 -s -v

# run sample apps tests
pytest tests/sample_apps_tests --maxfail=1 -s -v
```

If a test from `tests/sample_apps` fails, use `docker logs <servicename>` for debugging.
