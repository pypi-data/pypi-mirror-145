import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='gen3rftools',
    version='0.2',
    author='falomsc',
    author_email='falomsc@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/falomsc/gen3rftools',
    packages=setuptools.find_packages(),
    license='MIT',
    keywords='',
    python_requires='>=3.4, <4',
    install_requires=['paramiko', 'pyvisa', 'pywinauto', 'goto-statement', 'goto-label', 'pyqt6']
)