from setuptools import setup, find_packages
import glob
  
with open("README.md", 'r') as f:
    long_description = f.read()
  
setup(
        name ='qetools',
        version ='1.1.1',
        author ='Harish PVV',
        author_email ='harishpvv@gmail.com',
        description ="A command line helper for QuantumEspresso calculations",
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'qetools = qetools.qetools:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='quantum espresso dft harishpvv',
        install_requires = ['ase', 'numpy', 'matplotlib'],
        zip_safe = False,
        data_files = [("pseudos/PBE_ONCV/", glob.glob("src/qetools/pseudos/PBE_ONCV/*.UPF")),
                      ("pseudos/LDA_ONCV/", glob.glob("src/qetools/pseudos/LDA_ONCV/*.UPF")),
                      ("pseudos/PBESOL_ONCV/", glob.glob("src/qetools/pseudos/PBESOL_ONCV/*.UPF"))],
        include_package_data = True

        )
