from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='viscad',
    version='0.0.1.2',
    description='python vision functions for robotics',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://robocadv.readthedocs.io/en/latest/docs/all_docs/viscad_docs/index.html',
    author='Abdrakov Airat',
    author_email='abdrakovairat@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['function', 'vision', 'opencv'],
    packages=find_packages(),
    install_requires=['numpy', 'opencv-python']
)
