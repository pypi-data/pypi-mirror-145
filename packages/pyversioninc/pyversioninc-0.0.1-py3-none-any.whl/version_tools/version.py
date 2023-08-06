import os
import errno
from pathlib import Path
def get_releases(project_dir):
    """

    :param project_dir:
    :return:
    """

    #defining the distributions path
    dist_path=os.path.join(project_dir,'dist')
    try:
        #getting distibution by date order
        releases=sorted(Path(dist_path).iterdir(), key=os.path.getmtime)
    except:
        #Raising an exception if the path is not found
        raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), dist_path)

    return [str(release) for release in releases]
def get_current_version(project_dir: str = '.'):
    """
    Function to get the current version of the package.

    :param project_dir: The project directory path.
    :return:

    #Note that at the begining ther may not be a dist folder containing the releases.
    """

    return get_releases(project_dir)[-1].split('-')[1]

def get_previous_version(project_dir: str = '.'):
    """
    Function to get the previous version of the package.
    :param project_dir: The project directory path.
    :return:
    #Note that at the begining ther may not be a dist folder containing the releases.
    """
    len_releases=len(get_releases(project_dir))
    return get_releases(project_dir)[len_releases-2].split('-')[1]

def increment_version(version : str,level: str ='patch' ):
    """
    Function to increment the valeur of the package version
    :param version: The current version
    :return:

    """
    major,minor,patch=version.split(".")

    if level == 'patch':
        patch=int(patch)+1
    elif level=='minor':
        minor=int(minor)+1
    else :
        major=int(major)+1
    return '{}.{}.{}'.format(major,minor,patch)


