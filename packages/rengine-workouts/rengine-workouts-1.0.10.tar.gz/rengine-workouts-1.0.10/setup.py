import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rengine-workouts",
    version="1.0.10",
    description="Tools to generate workouts",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/noahsolomon0518/rengine",
    author="noahsolomon0518",
    author_email="noahsolomon0518@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    packages=["rengine", "rengine.scripts"],
    include_package_data=True,
    package_data={"rengine.data":["*"]},
    entry_points={
        "console_scripts": [
            "generate-exercise=rengine.scripts.generate_exercise:run",
            "generate-plan=rengine.scripts.generate_workout_plan:run",
        ]
    }
)