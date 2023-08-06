from setuptools import setup, find_packages
  
with open('README.md') as file:
    long_description = file.read()

short_description = 'An integrated quantum mechanics-machine learning approach for ultra-fast NMR structural elucidation.'
requirements = ['tk', 'pandas', 'numpy', 'sklearn', 'scipy', 'openpyxl']
  

setup(
        name ='ml-jdp4',
        version ='1.3.2',
        author='María M. Zanardi & Ariel M. Sarotti',
        author_email='zanardi@inv.rosario-conicet.gov.ar',
        url='https://github.com/Sarotti-Lab/ML_J_DP4',
        description =short_description	,
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        package_data={'': ['data/*.dat', 'examples/*', 'examples/menthol_ML_dJ-DP4/*', 'examples/menthol_ML_iJ-dJ-DP4/*']},
        entry_points = {'console_scripts': ['ml_jdp4 = ml_jdp4.ml_jdp4:main']},
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"],
        keywords ='NMR structural elucidation',
        install_requires = requirements
)


