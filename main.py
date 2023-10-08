import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    for script in ["task_1.py", "task_2.py", "task_3.py"]:
        run_script(script)
