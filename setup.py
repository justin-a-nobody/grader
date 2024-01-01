from setuptools import setup

setup(
    name='LuckysTradingCardGrader',
    version='1.0.0',
    description='A Flask-based web application for grading cards with image processing and database interactions',
    url='https://theshamrock.shop',
    author='M McGehee',
    author_email='mmcgehee2010@gmail.com',
    license='Apache2',
    packages=['LuckysTradingCardGrader'],
    install_requires=[
        'flask',
        'tensorflow',
        'numpy',
        'Pillow',  # For PIL
        'mysql-connector-python',
        'requests',
        'requirement.txt' # File is included for setup  Add other necessary packages
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',  # Specify the Python versions you support
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Specify your Python version requirement
    # Include any package data, scripts, or other files here
)
