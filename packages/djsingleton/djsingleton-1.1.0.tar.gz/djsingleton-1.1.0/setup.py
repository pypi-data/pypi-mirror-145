from setuptools import find_packages, setup

import djsingleton

setup(
    name=djsingleton.__name__,
    version=djsingleton.__version__,
    packages=find_packages(),
    url='https://github.com/sainipray/djsingleton',
    author=djsingleton.__author__,
    author_email=djsingleton.__author_email__,
    description=djsingleton.__description__,
    license='MIT',
    include_package_data=True,
    platforms=['any'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 2',
        'Framework :: Django :: 3',
        'Framework :: Django :: 4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
    ],
)
