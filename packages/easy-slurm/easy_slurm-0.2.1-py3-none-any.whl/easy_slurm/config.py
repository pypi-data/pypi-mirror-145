import os
import shutil
from copy import deepcopy
from glob import glob

import tomlkit
import yaml

from .format import format_with_config
from .jobs import submit_job


def submit_configs(base_job_config, hparams_configs, tmp_configs_root):
    """Submits a job for each hparams config.

    Job config variables such as `job_dir` and `job_name` are formatted
    based on the provided template using information from a given
    `hparams_config`. For instance:

    ```toml
    job_dir = "/home/user/jobs/{bs:hp.batch_size},{lr:hp.opt.learning_rate}"
    ```

    The above formatting template will generate the string
    `"/home/user/jobs/lr=0.001,bs=32"` when given the hparams config:

    ```json
    {
        "hp": {
            "batch_size": 32,
            "opt": {
                "learning_rate": 0.001
            }
        }
    }
    ```
    """
    shutil.rmtree(tmp_configs_root, ignore_errors=True)
    os.makedirs(tmp_configs_root, exist_ok=True)

    # Write configs to "assets" subfolders.
    for i, hparams_config in enumerate(hparams_configs):
        job_config = deepcopy(base_job_config)
        job_dir = format_with_config(job_config["job_dir"], hparams_config)
        job_name = format_with_config(
            job_config["sbatch_options"]["job-name"], hparams_config
        )
        assets_dir = f"{tmp_configs_root}/{i:03}_{job_name}"
        job_config["job_dir"] = job_dir
        job_config["assets"] = assets_dir
        job_config["sbatch_options"]["job-name"] = job_name
        os.makedirs(assets_dir)
        with open(f"{assets_dir}/job.toml", "w") as f:
            f.write(tomlkit.dumps(job_config, sort_keys=False))
        with open(f"{assets_dir}/hparams.yaml", "w") as f:
            yaml.safe_dump(hparams_config, f, sort_keys=False)

    # Submit each "assets" subfolder.
    for assets_dir in sorted(glob(f"{tmp_configs_root}/*")):
        with open(f"{assets_dir}/job.toml") as f:
            job_config = tomlkit.loads(f.read())
        job_name = job_config["sbatch_options"]["job-name"]
        print(f"Submitting {job_name}...")
        submit_job(**job_config)
        print(f"Submitted {job_name}.")
