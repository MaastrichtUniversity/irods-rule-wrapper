import re


def check_project_id_format(project):
    if re.search("^P[0-9]{9}$", project) is not None:
        return True
    else:
        return False


def check_project_path_format(project):
    if re.search("^/nlmumc/projects/P[0-9]{9}$", project) is not None:
        return True
    else:
        return False


def check_project_collection_path_format(project):
    if re.search("^/nlmumc/projects/P[0-9]{9}$", project) is not None:
        return True
    else:
        return False
