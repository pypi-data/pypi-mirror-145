from magniv.export.airflow import export_to_airflow
from magniv.utils.utils import _get_tasks_json


def export(gcp):
    task_list = _get_tasks_json("./dump.json")
    export_to_airflow(task_list, gcp)
