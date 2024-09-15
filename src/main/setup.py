from setuptools import find_packages, setup

package_name = 'main'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sylfio',
    maintainer_email='sylensdark@gmail.com',
    description='Package d\'interfaçage entre les différents noeuds de la brique conversationnelle.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = main.main:main'
        ],
    },
)
