import json
import pathlib
from typing import Optional

import cowsay
from kubernetes import client, config
from yaspin import yaspin

from now.deployment.deployment import cmd
from now.dialog import prompt_plus
from now.gke_deploy import create_gke_cluster

cur_dir = pathlib.Path(__file__).parent.resolve()


def create_local_cluster(kind_path):
    out, err = cmd(f'{kind_path} get clusters')
    if err and 'No kind clusters' not in err.decode('utf-8'):
        print(err.decode('utf-8'))
        exit()
    if 'jina-now' in out.decode('utf-8'):
        questions = [
            {
                'type': 'list',
                'name': 'proceed',
                'message': 'The local cluster is running already. '
                'Should it be recreated?',
                'choices': [
                    {'name': '⛔ no - stop', 'value': False},
                    {'name': '✅ yes - recreate', 'value': True},
                ],
            },
        ]
        recreate = prompt_plus(questions, 'proceed')
        if recreate:
            with yaspin(text="Remove local cluster", color="green") as spinner:
                cmd(f'{kind_path} delete clusters jina-now')
                spinner.ok('💀')
        else:
            cowsay.cow('see you soon 👋')
            exit(0)
    with yaspin(text="Setting up local cluster", color="green") as spinner:
        cmd(
            f'{kind_path} create cluster --name jina-now --config {cur_dir}/kind.yml',
        )
        spinner.ok("📦")


def is_local_cluster(**kwargs):
    out, error = cmd(f'{kwargs["kubectl_path"]} get nodes -o json')
    out = json.loads(out)
    addresses = out['items'][0]['status']['addresses']
    is_local = len([a for a in addresses if a['type'] == 'ExternalIP']) == 0
    return is_local


def setup_cluster(
    cluster_name: Optional[str],
    provider: str,
    kubectl_path='kubectl',
    kind_path='kind',
    **kwargs,
):
    if cluster_name is not None:
        cmd(f'{kubectl_path} config use-context {cluster_name}')
        ask_existing(kubectl_path)
    else:
        if provider == 'local':
            create_local_cluster(kind_path)
        elif provider == 'gke':
            create_gke_cluster()


def ask_existing(kubectl_path):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    if 'nowapi' in [item.metadata.name for item in v1.list_namespace().items]:
        questions = [
            {
                'type': 'list',
                'name': 'proceed',
                'message': (
                    'jina-now is deployed already. Do you want to remove the '
                    'current data?'
                ),
                'choices': [
                    {'name': '⛔ no - stop', 'value': False},
                    {'name': '✅ yes - remove', 'value': True},
                ],
            },
        ]
        remove = prompt_plus(questions, 'proceed')
        if remove:
            with yaspin(text="Remove old deployment", color="green") as spinner:
                cmd(f'{kubectl_path} delete ns nowapi')
                spinner.ok('💀')
        else:
            cowsay.cow('see you soon 👋')
            exit(0)
