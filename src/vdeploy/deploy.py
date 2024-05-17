import os.path

import paramiko
import subprocess
from urllib.parse import urlparse


def run_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.set_combine_stderr(True)
    while not stdout.channel.exit_status_ready():
        data = stdout.channel.recv(1024).decode()
        print(data, end="")
    exit_status = stdout.channel.recv_exit_status()
    print()
    if exit_status != 0:
        raise Exception("Command failed")


def attach_key(instance_id, key):
    subprocess.check_call(["vastai", "attach", "ssh", str(instance_id), key])


def get_ssh_url(instance_id):
    return (
        subprocess.check_output(["vastai", "ssh-url", str(instance_id)])
        .decode()
        .rstrip()
    )


def deploy_instance(offer_id: int, docker_image: str, timeout: int):
    with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as f:
        my_pub_key = f.read()

    # api.launch_instance(
    #      offer_id,
    #      docker_image_name=docker_image
    # )

    attach_key(offer_id, my_pub_key)
    ssh_url = urlparse(get_ssh_url(offer_id))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_url.hostname, port=ssh_url.port, username=ssh_url.username)
    run_command(
        client,
        "git clone https://github.com/acsresearch/vdeploy.git && cd vdeploy && pip3 install .",
    )

    # Generate special token to VASTAI API only for this instance, taken from https://vast.ai/faq
    run_command(
        client,
        "cat ~/.ssh/authorized_keys | md5sum | awk '{print $1}' > ssh_key_hv; echo -n $VAST_CONTAINERLABEL | md5sum | awk '{print $1}' > instance_id_hv; head -c -1 -q ssh_key_hv instance_id_hv > ~/.vast_api_key",
    )

    run_command(
        client,
        f"nohup /opt/conda/bin/python -m vdeploy start-watchdog --timeout={timeout} &> watchdog.log &",
    )
