from setuptools import setup

setup(
    name='tello_adv_setup',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='patrick ryan',
    author_email='',
    description='Tello Advanced Project Development Setup ',
    install_requires = [
        # pip install https://github.com/damiafuentes/DJITelloPy/archive/master.zip
        'opencv-python==4.8.0.76',
        'opencv-contrib-python==4.6.0.66',
        'jupyter==1.0.0',
        'imutils==0.5.4',
        'scipy==1.12.0',
        'DJITelloPy==2.4.0'
    ]

)
