import configparser
import logging
import git
from git import Repo


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


# Abbreviate the long hash to a short hash (7 digits)
def get_short_hash(hash, ndigits=7):
    if len(hash) < ndigits:
        short = hash
    else:
        short = hash[:ndigits]
    return short


def extract_git_vars(path=None, github_url=None):
    github_org_name = None
    github_repo_name = None
    github_sha = None
    github_actor = None
    github_branch = None
    github_branch_detached = None
    try:
        if path is None:
            path = get_git_root(".")
        github_repo = Repo(path)
        if github_url is None:
            github_url = github_repo.remotes[0].config_reader.get("url")
        if "/" in github_url[-1:]:
            github_url = github_url[:-1]
        if "http" in github_url:
            github_org_name = github_url.split("/")[-2]
            github_repo_name = github_url.split("/")[-1].split(".")[0]
        else:
            github_url = github_url.replace(".git", "")
            github_org_name = github_url.split(":")[1].split("/")[0]
            github_repo_name = github_url.split(":")[1].split("/")[1]
        try:
            github_sha = get_short_hash(github_repo.head.object.hexsha)
        except ValueError as e:
            logging.debug(
                "Unable to detected github_sha. caught the following error: {}".format(
                    e.__str__()
                )
            )
        github_branch = None
        github_branch_detached = False
        try:
            github_branch = github_repo.active_branch
        except TypeError as e:
            logging.debug(
                "Unable to detected github_branch. caught the following error: {}".format(
                    e.__str__()
                )
            )
            github_branch_detached = True

        github_actor = None
        try:
            github_actor = github_repo.config_reader().get_value("user", "name")
        except configparser.NoSectionError as e:
            logging.debug(
                "Unable to detected github_actor. caught the following error: {}".format(
                    e.__str__()
                )
            )
            github_branch_detached = True
    except git.exc.InvalidGitRepositoryError as e:
        logging.debug(
            "Unable to fill git vars. caught the following error: {}".format(
                e.__str__()
            )
        )
        github_branch_detached = True
    return (
        github_org_name,
        github_repo_name,
        github_sha,
        github_actor,
        github_branch,
        github_branch_detached,
    )
