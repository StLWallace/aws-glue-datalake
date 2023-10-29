import sys
import os

# Hacky way to add root directory to Python path during local execution
ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)
sys.path.append(ROOT_DIR)

from libs.aws_utils.glue import get_job_start_time


JOB_NAME = "meal-me-demo"
JOB_RUN_ID = "jr_94dc968403c10760c15ae5b11274c29f306d2d8f113bb36bb765bfcf9d28454e"

if __name__ == "__main__":

    start_time = get_job_start_time(JOB_NAME, JOB_RUN_ID)

    print(start_time)
