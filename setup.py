from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    """ 
    THIS FUNCTION WILL RETURN THE LIST OF THE FILE 
    """
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n"," ") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements
        
setup(
    project_name = "Deployment Project",
    author="Rahul Kumar Singh",
    author_email="javarahul04@gmail.com",
    version="0.0.1",
    date = "30-01-2024",
    packages=find_packages(),
    install_required = get_requirements('requirements.txt'))