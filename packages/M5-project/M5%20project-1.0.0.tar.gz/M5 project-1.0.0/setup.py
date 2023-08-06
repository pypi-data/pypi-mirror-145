import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="M5 project",
                 author='Boris',
                 version="1.0.0",
                 long_description=long_description,
                 scripts = ['src/M5_model/m5_initial_nn_model.py'],
                 description="Initial NN model for M5 project",
                 python_requires='>=3.7',
                 project_urls={
                     "Git url": "https://github.com/borisilin85/M5_project",
                 }

                 )