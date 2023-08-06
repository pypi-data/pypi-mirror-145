#  Apache License Version 2.0
#
#  Copyright (c) 2021., Redis Labs Modules
#  All rights reserved.
#

import argparse
import json
import logging
import os
import sys

import requests
import toml

from speedscope_to_codeperf import __version__
from speedscope_to_codeperf.git import extract_git_vars
from speedscope_to_codeperf.schema.speedscope import (
    validate_speedscope_json,
    get_cpu_by_function,
    get_flamegraph,
)

LOG_LEVEL = logging.DEBUG
if os.getenv("VERBOSE", "0") == "0":
    LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)-4s %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

LONG_DESCRIPTION = """                  __                     ____        _
  _________  ____/ /__  ____  ___  _____/ __/       (_)___
 / ___/ __ \\/ __  / _ \\/ __ \\/ _ \\/ ___/ /_        / / __ \\
/ /__/ /_/ / /_/ /  __/ /_/ /  __/ /  / __/  _    / / /_/ /
\\___/\\____/\\__,_/\\___/ .___/\\___/_/  /_/    (_)  /_/\\____/
                    /_/
Export and persist speedscope's profiling data locally, or into https://codeperf.io for FREE."""


def populate_with_poetry_data():
    project_name = "speedscope-to-codeperf"
    project_version = __version__
    project_description = None
    try:
        poetry_data = toml.load("pyproject.toml")["tool"]["poetry"]
        project_name = poetry_data["name"]
        project_version = poetry_data["version"]
        project_description = poetry_data["description"]
    except FileNotFoundError:
        pass

    return project_name, project_description, project_version


def main():
    (
        github_org_name,
        github_repo_name,
        github_sha,
        github_actor,
        github_branch,
        github_branch_detached,
    ) = extract_git_vars()
    project_name, project_description, project_version = populate_with_poetry_data()
    parser = argparse.ArgumentParser(
        description=project_description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # common arguments to all tools
    parser.add_argument(
        "--version", default=False, action="store_true", help="print version and exit"
    )
    parser.add_argument(
        "--git-commit", type=str, default=github_sha, help="git commit hash"
    )
    parser.add_argument("--git-org", type=str, default=github_org_name, help="git org")
    parser.add_argument(
        "--git-repo", type=str, default=github_repo_name, help="git repo"
    )
    parser.add_argument(
        "--codeperf-url", type=str, default="https://codeperf.io", help="codeperf URL"
    )
    parser.add_argument(
        "--api-codeperf-url",
        type=str,
        default="https://api.codeperf.io",
        help="codeperf URL",
    )
    parser.add_argument(
        "--bench", type=str, default=None, required=True, help="Benchmark name"
    )
    parser.add_argument(
        "--input", type=str, default=None, required=True, help="input filename"
    )

    args = parser.parse_args()
    if args.version:
        print_version(project_name, project_version)
        sys.exit(0)

    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    print(LONG_DESCRIPTION)
    log_version(project_name, project_version)

    if args.git_commit is None:
        logging.error("git commit cannot be None. Exiting...")
        sys.exit(1)
    if args.git_org is None:
        logging.error("git org cannot be None. Exiting...")
        sys.exit(1)
    if args.git_repo is None:
        logging.error("git repo cannot be None. Exiting...")
        sys.exit(1)

    with open(args.input, "r") as speedscope_fd:
        speedscope_json = json.load(speedscope_fd)
        res_validate = validate_speedscope_json(speedscope_json)
        logging.info("Validating input file schema")
        if res_validate is False:
            logging.error(
                "The provided file {} does not contain a valid speedscope schema. Exiting...".format(
                    args.input
                )
            )
        else:
            codeperf_url = args.codeperf_url
            api_codeperf_url = args.api_codeperf_url
            git_org = args.git_org
            git_repo = args.git_repo
            git_commit = args.git_commit
            bench = args.bench
            for granularity in ["functions", "lines"]:
                cpu_by_function_json = get_cpu_by_function(speedscope_json, granularity)
                endpoint = "{}/v1/gh/{}/{}/commit/{}/bench/{}/cpu/{}".format(
                    api_codeperf_url, git_org, git_repo, git_commit, bench, granularity
                )
                resp = requests.post(endpoint, json=cpu_by_function_json)
                if resp.status_code == 200:
                    logging.info(
                        "Successfully published profile data in granularity: {}".format(
                            granularity
                        )
                    )
            flamegraph = get_flamegraph(speedscope_json)
            granularity = "flamegraph"
            endpoint = "{}/v1/gh/{}/{}/commit/{}/bench/{}/cpu/{}".format(
                api_codeperf_url, git_org, git_repo, git_commit, bench, granularity
            )
            resp = requests.post(endpoint, json=flamegraph)
            if resp.status_code == 200:
                logging.info(
                    "Successfully published profile data in granularity: {}".format(
                        granularity
                    )
                )

            logging.info(
                "Check it at: {}/gh/{}/{}/commit/{}/bench/{}/cpu".format(
                    codeperf_url,
                    git_org,
                    git_repo,
                    git_commit,
                    bench,
                )
            )


def print_stdout_effective_log_level():
    effective_log_level = "N/A"
    effective_log_level = logging.getLogger().getEffectiveLevel()
    if effective_log_level == logging.DEBUG:
        effective_log_level = "DEBUG"
    if effective_log_level == logging.INFO:
        effective_log_level = "INFO"
    if effective_log_level == logging.WARN:
        effective_log_level = "WARN"
    if effective_log_level == logging.ERROR:
        effective_log_level = "ERROR"
    print("Effective log level set to {}".format(effective_log_level))


def print_version(project_name, project_version):
    print(
        "{project_name} {project_version}".format(
            project_name=project_name, project_version=project_version
        )
    )


def log_version(project_name, project_version):
    logging.info(
        "Using {project_name} {project_version}".format(
            project_name=project_name, project_version=project_version
        )
    )
