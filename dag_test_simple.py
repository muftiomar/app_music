from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Définition du DAG
with DAG(
    dag_id="dag_test_simple",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",  # Exécution quotidienne
    catchup=False,  # Pas de rattrapage des dates passées
    tags=["demo"],
    description="Un DAG très simple pour test Airflow"
) as dag:

    # Tâche 1 : afficher la date
    afficher_date = BashOperator(
        task_id="afficher_date",
        bash_command="date"
    )

    # Tâche 2 : afficher un message
    dire_bonjour = BashOperator(
        task_id="dire_bonjour",
        bash_command="echo 'Bonjour depuis Airflow !'"
    )

    # Définir l'ordre d'exécution
    afficher_date >> dire_bonjour
