import subprocess

def run_batch_script(script_path):
    result = subprocess.run([script_path], shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"O script falhou com o código de saída {result.returncode}")

run_batch_script('setup_and_run.bat')
