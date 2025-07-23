# ops/definitions.py
from dagster import Definitions, op, job, ScheduleDefinition
import app

@op
def run_app_op():
    # Llama a la función principal de tu script
    app.main()

@job
def daily_app_job():
    run_app_op()

# Schedule cada hora, minuto 0, zona Monterrey
daily_app_schedule = ScheduleDefinition(
    job=daily_app_job,
    cron_schedule="0 0 * * *",
    execution_timezone="America/Monterrey",
)

defs = Definitions(
    jobs=[daily_app_job],
    schedules=[daily_app_schedule],
)

