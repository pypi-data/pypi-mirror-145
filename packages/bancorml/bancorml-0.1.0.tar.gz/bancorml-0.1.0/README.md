<p align="center">
<img width="300" src="https://bancorml.s3.us-east-2.amazonaws.com/images/bancorml_horizontal.png" alt="bciAVM" height="150"/>
</p>

[![PyPI](https://vsrm.dev.azure.com/gcode-ai/_apis/public/Release/badge/52109c77-be71-4849-9d35-4fc861db41a6/1/1)](https://vsrm.dev.azure.com/gcode-ai/_apis/public/Release/badge/52109c77-be71-4849-9d35-4fc861db41a6/1/1)
[![bancorml-0.1.0-py3-none-any.whl package in bancorml@Release feed in Azure Artifacts](https://feeds.dev.azure.com/gcode-ai/52109c77-be71-4849-9d35-4fc861db41a6/_apis/public/Packaging/Feeds/bancorml@Release/Packages/0926c7d3-1ac4-4316-a132-cf9867850696/Badge)](https://dev.azure.com/gcode-ai/BancorML/_artifacts/feed/bancorml@Release/UPack/bancorml-0.1.0-py3-none-any.whl/0.0.16)

**BancorML** is a DeFi multi-agent-reinforcement-learning (MARL) simulation library that builds, optimizes, and evaluates machine learning pipelines using domain-specific objective functions.

Combined with [Gym](https://gym.openai.com/docs/), BancorML can be used to create end-to-end MARL solutions.

The library demonstrates the following features:

 
**Key Functionality**


* **Gym Environments** - Gym Environment API based trading simulator with continuous observation space and discrete action space. 

    - ***Obsevation Space*** - Observation at a time step is the relative

    - ***Action Space*** - Action space is *discrete* with distinct possible actions

* **MARL Solvers** - High-level multi-agent reinforcement learning components, written in pytorch.

* **Component Graphs** - A component graph is comprised of nodes representing components, and edges between pairs of nodes representing where the inputs and outputs of each component should go.

* **TrainableAgent** - Agent object inheritance
 
 
 
 
 

First time using **Azure Artifacts** with pip on this machine?

### Get the tools
The easiest way to use Python packages from the command line is with pip (19.2+) and the Azure Artifacts keyring.
 
 
### Step 1
Download Python
 
 
### Step 2
Update pip
````{tab} PyPI
```console
$ python -m pip install --upgrade pip
```
````
 
 
### Step 3
Install the keyring
````{tab} PyPI
```console
$ pip install keyring artifacts-keyring
```
````
 
 
### Step 4
If you're using Linux, ensure you've installed the prerequisites, which are required for artifacts-keyring.
 
 
 

### Project setup

Ensure you have installed the latest version of the Azure Artifacts keyring from the "Get the tools" section above.
If you don't already have one, create a virtualenv using [these instructions](https://docs.python.org/3/library/venv.html) from the official Python documentation. Per the instructions, "it is always recommended to use a virtualenv while developing Python applications."

Add a pip.ini (Windows) or pip.conf (Mac/Linux) file to your virtualenv
````{tab} PyPI
```console
[global]
index-url=https://pkgs.dev.azure.com/gcode-ai/BancorML/_packaging/bancorml/pypi/simple/
```
````


# Install

bancorml is available for Python 3.7, 3.8, and 3.9. It can be installed from [pypi](https://pypi.org/project/bancorml/), [conda-forge](https://anaconda.org/conda-forge/bancorml), or from [Azure Artifacts](https://dev.azure.com/gcode-ai/BancorML/_artifacts/feed/bancorml/).

To install bancorml with all dependencies using Azure Artifacts, Run this command in your project directory:

````{tab} PyPI
```console
$ pip install
```
````

TODO: Setup private conda
````{tab} Conda
```console
$ conda install -c conda-forge bancorml
```
````

TODO: Setup private pypi
````{tab} Conda
```console
$ pip install bancorml
```
````
 
 
## Windows Additional Requirements & Troubleshooting

If you are using `pip` to install bancorml on Windows, it is recommended you first install the following packages using conda:
* `numba` (needed for `shap` and prediction explanations). Install with `conda install -c conda-forge numba`
* `graphviz` if you're using bancorml's plotting utilities. Install with `conda install -c conda-forge python-graphviz`

The [XGBoost](https://pypi.org/project/xgboost/) library may not be pip-installable in some Windows environments. If you are encountering installation issues, please try installing XGBoost from [Github](https://xgboost.readthedocs.io/en/latest/build.html) before installing bancorml or install bancorml with conda.
 
 
 
## Mac Additional Requirements & Troubleshooting

In order to run on Mac, [LightGBM](https://pypi.org/project/lightgbm/) requires the `OpenMP` library to be installed, which can be done with [HomeBrew](https://brew.sh/) by running:

```bash
brew install libomp
```

Additionally, `graphviz` can be installed by running:

```bash
brew install graphviz
```



#### Start


```python
import bancorml
from bancorml.utils import converters, parse_json_tests, load_test_data
from bancorml.environments import Bancor3

X, indx = load_test_data().sample(1), 0

a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = bancorml.utils.parse_json_tests(X, indx)
t_is_surplus = True if X['is_tkn_surplus'].values[0]=='True' else False

protocol = Bancor3(is_solidity=False)
is_surplus, is_deficit = protocol.check_surplus(b, c, e, n)
assert is_surplus == t_is_surplus, f"is_surplus={is_surplus} != t_is_surplus={t_is_surplus} on index={indx}"

```


## Next Steps

Read more about bancorml on our [documentation page](https://docs.google.com/document/d/138RXcc2FXLmsracebYDDmavh7bmgC3BpEFGy8RB63xA/edit?usp=sharing):


* [Installation](https://gcodeai-bancorml-docs.readthedocs-hosted.com/en/latest/install.html) and [getting started](https://gcodeai-bancorml-docs.readthedocs-hosted.com/en/latest/start.html).

* [Tutorials](https://gcodeai-bancorml-docs.readthedocs-hosted.com/en/latest/tutorials.html) on how to use bancorml.

* [User guide](https://gcodeai-bancorml-docs.readthedocs-hosted.com/en/latest/user_guide.html) which describes bancorml's features.

* Full [API reference](https://gcodeai-bancorml-docs.readthedocs-hosted.com/en/latest/api_index.html)


## Roadmap Algorithm Support
 
 
### Single-agent algorithms

| **Q-learning**    | **DQN**            | **Actor-Critic**    | **DDPG**           |**TD3**            |
| ----------------- | ------------------ | ------------------- | ------------------ |------------------- | 
| :x:  | :x:  | :x:    | :x:   |:x:  |


### Multi-agent algorithms

| **minimaxQ**        | **PHC**      | **JAL** | **MAAC**             | **MADDPG**         | 
| ------------------- | ------------------- | ------- |  -------------------- |  ----------------- | 
|  :x:  | :x:   |  :x:    |  :x:     | :x:   |

 
 
## Support

Project support can be found in four places depending on the type of question:

1. For bugs, issues, or feature requests start a [Github issue](https://github.com/gcode-ai/bancorml-docs/issues).
2. For everything else, the core developers can be reached by email at mike@bancor.network

 
 
## Built by Bancor Research Team

**bancorml** is a project built by [bancor.network](https://try.bancor.network). 


<a href="https://try.bancor.network">
<img width="75" height="75" src="https://130351921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LjjvEh4hW5E6OcD80nn%2Fuploads%2FjyKAdivy42MaSH2SXGgp%2FBNT%20Token.png?alt=media&token=ada4053a-d1a7-4e79-a071-38985420d463" alt="bancorml" />
</a>


