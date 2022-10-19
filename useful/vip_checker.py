from datetime import datetime

from data_base.db_functions import get_vip_project_list


def check_vip():
    vip_projects = get_vip_project_list()
    now = datetime.now().date()
    for project in vip_projects:
        if project.vip_ending < now:
            project.vip_ending = datetime(year=1900, month=1, day=1)
            project.status_id = 0
            project.status = "REGULAR"
            project.save_changes_to_existing_project()
