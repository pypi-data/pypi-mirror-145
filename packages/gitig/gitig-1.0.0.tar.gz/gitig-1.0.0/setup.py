# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gitig']
entry_points = \
{'console_scripts': ['gi = gitig:cli']}

setup_kwargs = {
    'name': 'gitig',
    'version': '1.0.0',
    'description': 'Generate .gitignore files from the command-line',
    'long_description': "# gitig\n\nGenerate `.gitignore` files from the command-line\n\n[![PyPI Version](https://img.shields.io/pypi/v/gitig.svg)](https://pypi.org/project/gitig/)\n\n`gitig` writes its output to stdout. Redirect the results to wherever makes sense for you, for example:\n\n```bash\ngi python > .gitignore\n```\n\n## Installation\n\n### With `pipx`\n\n`gitig` is intended to be used as an **end-user command-line application** (i.e. not as a package's dependecy). The easiest way to get started is with `pipx`:\n\n```bash\npipx install gitig\n```\n\n### With `pip`\n\n`gitig` can also be installed via vanilla pip (or poetry, etc.):\n\n```bash\npip install gitig\n```\n\n## Usage\n\n```text\n$ gi -h\nusage: gi [-h] [-v] [--completion {bash,fish}] [--no-pager]\n          [template [template ...]]\n\npositional arguments:\n  template              Template(s) to include in the generated .gitignore\n                        file. If no templates are specified, display a list of\n                        all available templates.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --version         show program's version number and exit\n  --completion {bash,fish}\n                        Generate a completion file for the selected shell.\n  --no-pager            Write template list to stdout. By default, this\n                        program attempts to paginate the list of available\n                        templates for easier reading.\n```\n\n## Examples\n\n- List all available gitignore templates (using a pager if one is available):\n\n  ```bash\n  gi\n  ```\n\n- Generate a gitignore file for Python and Jupyter:\n\n  ```bash\n  gi python jupyternotebooks\n  ```\n\n## Enable tab completion for Bash or Fish\n\n`gitig` supports generating completion scripts for Bash and Fish. Below are commands to generate completion scripts for the various shells\n\n> For **Bash**, you will likely have to `source` (`.`) the generated tab completion script for it to take effect.\n>\n> To enable tab completion on startup you can source the completion generated completion script in your `.bashrc` or `.bash_profile`.\n\n### Bash\n\n```bash\ngi --completion bash > /etc/bash_completion.d/gi.bash-completion\n```\n\n### Bash (Homebrew)\n\n```bash\ngi --completion bash > $(brew --prefix)/etc/bash_completion.d/gi.bash-completion\n```\n\n### Fish\n\n```fish\ngi --completion fish > ~/.config/fish/completions/gi.fish\n```\n\n### Fish (Homebrew)\n\n```fish\ngi --completion fish > (brew --prefix)/share/fish/vendor_completions.d/gi.fish\n```\n\n## API\n\n### CLI\n\n```bash\ngi # query gitignore.io and list available options\n```\n\n```bash\ngi python jupyternotebooks # write a .gitingore file for python and jupyter to stdout\n```\n\n```bash\ngi --completion bash # write generated bash autocompletion script to stdout\ngi --completion fish # write generated fish autocompletion script to stdout\n```\n\n```bash\ngi --version # write gitig version info to stdout\n```\n\n### Autocompletion\n\n```bash\ngi <TAB><TAB>\n1c                         1c-bitrix                  actionscript\nada                        adobe                      advancedinstaller          adventuregamestudio\nagda                       al                         alteraquartusii            altium\n...\n```\n\n```bash\n$ gi python j<TAB><TAB>\njabref  jboss6          jekyll         jetbrains+iml  joe     jupyternotebooks\njava    jboss-4-2-3-ga  jenv           jgiven         joomla  justcode\njboss   jboss-6-x       jetbrains      jigsaw         jspm\njboss4  jdeveloper      jetbrains+all  jmeter         julia\n```\n\n### Python API\n\n```python\nimport gitig\n\ngitig.list()  # same as `gi`\ngitig.create(['python', 'jupyter'])  # same as `gi python jupyter`\ngitig.bash_completion()  # same as `gi --completion bash`\ngitig.fish_completion()  # same as `gi --completion fish`\ngitig.__version__\n```\n\n## Contributing\n\n1. Have or install a recent version of `poetry` (version >= 1.1)\n1. Fork the repo\n1. Setup a virtual environment (however you prefer)\n1. Run `poetry install`\n1. Run `pre-commit install`\n1. Add your changes (adding/updating tests is always nice too)\n1. Commit your changes + push to your fork\n1. Open a PR\n",
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/gitig',
    'package_dir': package_dir,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
