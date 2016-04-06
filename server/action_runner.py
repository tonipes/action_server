import subprocess

def run_action(action):
    process = subprocess.Popen(action['exec'].split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output
