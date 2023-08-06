# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_slurm', 'easy_slurm.templates']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easy-slurm',
    'version': '0.2.1',
    'description': 'Easily manage and submit robust jobs to Slurm using Python and Bash.',
    'long_description': '# Easy Slurm\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![PyPI](https://img.shields.io/pypi/v/easy-slurm)](https://pypi.org/project/easy-slurm)\n\nEasily manage and submit robust jobs to Slurm using Python and Bash.\n\n## Features\n\n - **Freezes** source code and assets by copying to separate `$JOB_DIR`.\n - **Auto-submits** another job if current job times out.\n - **Exposes hooks** for custom bash code: `setup`/`setup_resume`, `on_run`/`on_run_resume`, and `teardown`.\n - [**Format job names**](#formatting) using parameters from config files.\n - **Interactive** jobs supported for easy debugging.\n\n## Installation\n\n```bash\npip install easy-slurm\n```\n\n## Usage\n\nTo submit a job, simply fill in the various parameters shown in the example below.\n\n```python\nimport easy_slurm\n\neasy_slurm.submit_job(\n    job_dir="$HOME/jobs/{date}-{job_name}",\n    src="./src",\n    assets="./assets",\n    dataset="./data.tar.gz",\n    setup="""\n        virtualenv "$SLURM_TMPDIR/env"\n        source "$SLURM_TMPDIR/env/bin/activate"\n        pip install -r "$SLURM_TMPDIR/src/requirements.txt"\n    """,\n    setup_resume="""\n        # Runs only on subsequent runs. Call setup and do anything else needed.\n        setup\n    """,\n    on_run="python main.py",\n    on_run_resume="python main.py --resume",\n    teardown="""\n        # Do any cleanup tasks here.\n    """,\n    sbatch_options={\n        "job-name": "example-simple",\n        "account": "your-username",\n        "time": "3:00:00",\n        "nodes": "1",\n    },\n    resubmit_limit=64,  # Automatic resubmission limit.\n)\n```\n\nAll job files will be kept in the `job_dir` directory. Provide directory paths to `src` and `assets` -- these will be archived and copied to the `job_dir` directory. Provide a file path to an archive containing the `dataset`. Also provide Bash code in the hooks, which will be run in the following order:\n\n| First run: | Subsequent runs: |\n| ---------- | ---------------- |\n| `setup`    | `setup_resume`   |\n| `on_run`   | `on_run_resume`  |\n| `teardown` | `teardown`       |\n\nFull examples can be found [here](./examples), including a [simple example](./examples/simple) to run "training epochs" on a cluster.\n\nJobs can also be fully configured using YAML files. See [`examples/simple_yaml`](./examples/simple-yaml).\n\n```yaml\njob_dir: "$HOME/jobs/{date}-{job_name}"\nsrc: "./src"\nassets: "./assets"\ndataset: "./data.tar.gz"\nsetup: |\n  virtualenv "$SLURM_TMPDIR/env"\n  source "$SLURM_TMPDIR/env/bin/activate"\n  pip install -r "$SLURM_TMPDIR/src/requirements.txt"\nsetup_resume: |\n  # Runs only on subsequent runs. Call setup and do anything else needed.\n  setup\non_run: "python main.py"\non_run_resume: "python main.py --resume"\nteardown: |\n  # Do any cleanup tasks here.\nsbatch_options:\n  job-name: "example-simple"\n  account: "your-username"\n  time: "3:00:00"\n  nodes: 1\nresubmit_limit: 64  # Automatic resubmission limit.\n```\n\n### Formatting\n\nOne useful feature is formatting paths using custom template strings:\n```python\neasy_slurm.submit_job(\n    job_dir="$HOME/jobs/{date:%Y-%m-%d}-{job_name}",\n)\n```\n\nThe job names can be formatted using a config dictionary:\n```python\njob_name = easy_slurm.format.format_with_config(\n    "bs={hp.batch_size:04},lr={hp.lr:.1e}",\n    config={"hp": {"batch_size": 32, "lr": 1e-2}},\n)\n\neasy_slurm.submit_job(\n    job_dir="$HOME/jobs/{date:%Y-%m-%d}-{job_name}",\n    sbatch_options={\n        "job-name": job_name,  # equals "bs=0032,lr=1.0e-02"\n        ...\n    },\n    ...\n)\n```\n\nThis helps in automatically creating descriptive, human-readable job names.\n\nSee documentation for more information and examples.\n',
    'author': 'Mateen Ulhaq',
    'author_email': 'mulhaq2005@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YodaEmbedding/easy-slurm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
