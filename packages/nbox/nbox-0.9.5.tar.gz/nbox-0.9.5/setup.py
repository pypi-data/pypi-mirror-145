# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbox', 'nbox.framework', 'nbox.hyperloop', 'nbox.nbxlib', 'nbox.sub_utils']

package_data = \
{'': ['*'], 'nbox': ['assets/*'], 'nbox.framework': ['protos/*']}

install_requires = \
['Jinja2==3.0.3',
 'dill==0.3.4',
 'grpcio==1.43.0',
 'mypy-protobuf==3.2.0',
 'python-json-logger==2.0.2',
 'randomname>=0.1.3,<0.2.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate==0.8.9']

setup_kwargs = {
    'name': 'nbox',
    'version': '0.9.5',
    'description': 'ML Inference 🥶',
    'long_description': '<a href="https://nimblebox.ai/" target="_blank"><img src="./assets/built_at_nbx.svg" align="right"></a>\n\n# 🏖️ Nbox\n\npypi `nbox` is stable for SSH and other APIs. Check out [v1](https://github.com/NimbleBoxAI/nbox/tree/v1) for the latest code and APIs!\n\nA library that makes using a host of models provided by the opensource community a lot more easier. \n\n> The entire purpose of this package is to make using models 🥶.\n\n```\npip install nbox\n```\n\n#### Current LoC\n\n```\nSLOC\tDirectory\tSLOC-by-Language (Sorted)\n996     top_dir         python=996\n88      framework       python=88\n\nTotals grouped by language (dominant language first):\npython:        1084 (100.00%)\n```\n\n## 🔥 Usage\n\n```python\nimport nbox\n\n# As all these models come from the popular frameworks you use such as \n# torchvision, efficient_pytorch or hf.transformers\nmodel = nbox.load("torchvision/mobilenetv2", pretrained = True)\n\n# nbox makes inference the priority so you can use it\n# pass it a list for batch inference \nout_single = model(\'cat.jpg\')\nout = model([Image.open(\'cat.jpg\'), np.array(Image.open(\'cat.jpg\'))])\ntuple(out.shape) == (2, 1000)\n\n# deploy the model to a managed kubernetes cluster on NimbleBox.ai\nurl_endpoint, nbx_api_key = model.deploy()\n\n# or load a cloud infer model and use seamlessly\nmodel = nbox.load(\n  model_key_or_url = url_endpoint,\n  nbx_api_key = nbx_api_key,\n  category = "image"\n)\n\n# Deja-Vu!\nout_single = model(\'cat.jpg\')\nout = model([Image.open(\'cat.jpg\'), np.array(Image.open(\'cat.jpg\'))])\ntuple(out.shape) == (2, 1000)\n```\n\n## ⚙️ CLI\n\nJust add this to your dockerfile or github actions.\n\n```\nNBX_AUTH=1 python -m nbox deploy --model_path=my/model.onnx --deployment_type="nbox"\n\n# or for more details\n\npython -m nbox --help\n```\n\n## ✏️ Things for Repo\n\n- Using [`poetry`](https://python-poetry.org/) for proper package management as @cshubhamrao says.\n  - Add new packages with `poetry add <name>`. Do not add `torch`, `tensorflow` and others, useless burden to manage those.\n  - When pushing to pypi just do `poetry build && poetry publish` this manages all the things around\n- Install `pytest` and then run `pytest tests/ -v`.\n- Using `black` for formatting, VSCode to the moon.\n- To make the docs:\n  ```\n  # from current folder\n  sphinx-apidoc -o docs/source/ ./nbox/ -M -e\n  cd docs && make html\n  cd ../build/html && python3 -m http.server 80\n  ```\n\n# 🧩 License\n\nThe code in thist repo is licensed as [BSD 3-Clause](./LICENSE). Please check for individual repositories for licenses.\n',
    'author': 'NBX Research',
    'author_email': 'research@nimblebox.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NimbleBoxAI/nbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
