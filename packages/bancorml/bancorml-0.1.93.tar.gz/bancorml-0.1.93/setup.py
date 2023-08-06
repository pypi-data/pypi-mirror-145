from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_require = {}
extras_require['complete'] = sorted(set(sum(extras_require.values(), [])))

setup(
    name='bancorml',
    version='0.1.93',
    author='Bancor Network',
    author_email='mike@bancor.network',
    description='BancorML is a library that builds, optimizes, and evaluates machine learning pipelines in the context of a multi-agent system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/gcode-ai/bancorml',
    install_requires=open('requirements.txt').readlines(),
    extras_require=extras_require,
    tests_require=open('test-requirements.txt').readlines(),
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
          'bancorml = bancorml.__main__:cli'
        ]
    },
    data_files=[
        ('bancorml/tests/data', [
                                'bancorml/tests/environment_tests/data/withdrawal_algorithm_tests.json'
                              ])
                ],
)
