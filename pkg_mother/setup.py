from setuptools import setup
<<<<<<< HEAD
import os
from glob import glob

package_name = 'tuto_sim'
=======

package_name = 'pkg_mother'
>>>>>>> 93e912270b2cc7070f456acf3f454cddeab5b6c0

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
<<<<<<< HEAD
        (os.path.join('share',package_name),glob('launch/*launch.[pxy][yma]*'))
=======
>>>>>>> 93e912270b2cc7070f456acf3f454cddeab5b6c0
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bot',
    maintainer_email='bot@mb6.imt-nord-europe.fr',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
<<<<<<< HEAD
            'move_rnd = pkg_mother.cmove_randomly:main'
=======
>>>>>>> 93e912270b2cc7070f456acf3f454cddeab5b6c0
        ],
    },
)
