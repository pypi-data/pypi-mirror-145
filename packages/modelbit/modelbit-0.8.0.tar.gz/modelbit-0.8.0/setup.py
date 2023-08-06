from setuptools import setup

setup(
    name='modelbit',
    version='0.8.0',
    description='Python package to connect Jupyter notebooks to Modelbit',
    url='https://www.modelbit.com',
    author='Modelbit',
    author_email='tom@modelbit.com',
    license='MIT',
    packages=['modelbit', 'pyaes'],
    # Note: Keep these deps in sync with snowpark config
    install_requires=['pycryptodomex',
                      'pandas',
                      'tqdm',
                      'requests',
                      'types-requests',
                      'ipython',
                      'markdown',
                      'types-markdown'
                      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3',
    ],
)
