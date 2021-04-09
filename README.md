# SmartWindow

A collective visual passenger information system that helps passenger to enrich aspect of particular things while traveling to their destination. This web application is a prototype and a part of `SmartWindow` project to demonstrate its functionality, which is also a part of [planspiel](https://vsr.informatik.tu-chemnitz.de/edu/2020/planspiel/). the application is written in [python](https://www.python.org/) using [django](https://www.djangoproject.com/) framework.

# Contributors

* [Emon Hossain](https://gitlab.hrz.tu-chemnitz.de/emon--tu-chemnitz.de) (emon.hossain@s2018.tu-chemnitz.de)
* [Md Atikul Islam](https://gitlab.hrz.tu-chemnitz.de/mdis--tu-chemnitz.de)  (md-atikul.islam@s2019.tu-chemnitz.de)
* [Abdullah-al-noman](https://gitlab.hrz.tu-chemnitz.de/abno--tu-chemnitz.de) (abdullah-al.noman@s2018.tu-chemnitz.de)

# Installation \& Run

Please go thorough the following steps to install and run the project

## Pre-requisite

* Must have [python](https://www.python.org/) version `3.7.x` installed in your machine, and
* package manager [pip](https://pip.pypa.io/en/stable/) `v20.x` or higher




## Download  
if you have required environment then download or clone whole project to your local machine from repository.

then, go to [https://drive.google.com/file/d/1-HdesmO3bs_Ocd-8ZUnk6erjpuKBkLWE/view?usp=sharing](https://drive.google.com/file/d/1-HdesmO3bs_Ocd-8ZUnk6erjpuKBkLWE/view?usp=sharing) and download the `weight.h5` file. After  finishing download please put the file into “model_data” directory. You will find the directory in the base directory of our project.
 the project structure will look like this.

```bash
\---seaquasar
    \---Smart Window
        +---.idea
        |   +---inspectionProfiles
        |   +---libraries
        |   \---snapshots
        +---model_data
        +---smart_window
        |   \---__pycache__
        +---stream
        |   +---geography
        |   |   \---__pycache__
        |   +---migrations
        |   |   \---__pycache__
        |   +---static
        |   |   \---stream
        |   |       +---css
        |   |       +---images
        |   |       \---js
        |   +---templates
        |   |   \---stream
        |   +---yolo
        |   |   \---__pycache__
        |   \---__pycache__
        \---yolo3
            \---__pycache__

```

## Creating a virtual environment

as next step, we are recommending you to create a virtual environment for the project. In order to do that please click on [this](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-20-04-quickstart) for linux distribution and click on [this](https://www.c-sharpcorner.com/article/steps-to-set-up-a-virtual-environment-for-python-development/) for windows.

Or just run the application using global environment 

in both way we are almost near to finish our installation process
next step is to install required libraries.

## Install required libraries 

use your `Command prompt` or `Terminal` and go to our project directory using `cd` command. it will look like this for ubuntu and windows respectively. 

```
(venv) .../smartwindow$ 
or 
(venv) .../smartwindow>
```
based on your operating system

now write the bellow `pip` command to install all required libraries
```
pip install -r requirements.txt
```
above command will allow you to download and install all required libraries automatically.

## run application
now we are ready to run our application by typing 

```
python manage.py runserver
```

## License
[MIT](https://choosealicense.com/licenses/mit/)