from setuptools import setup

setup(
    name='tello-adv-aruco',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='patrick ryan',
    author_email='',
    description='Tello Advanced ArUco Markers',
    install_requires = [
        # pip install https://github.com/damiafuentes/DJITelloPy/archive/master.zip
        'opencv-python==4.4.0.46',
        'opencv-contrib-python==4.4.0.46',
        'jupyter==1.0.0',
        'imutils==0.5.3',
        'scipy==1.5.4'
    ]

)
