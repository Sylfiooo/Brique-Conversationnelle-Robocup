from setuptools import setup

package_name = 'nlp'
submodules = "nlp/submodules"

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name, submodules],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sylfio',
    maintainer_email='sylensdark@gmail.com',
    description='Package de services NLP',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nlp = nlp.nlp:main',
            'test_client = nlp.test_client:main'
        ],
    },
)
