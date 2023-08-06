import requests
import os
import json

api_endpoint = "https://api.roboflow.com/oak/"
cache_dir = ".cache/roboflow"


def download_blob(project, version, api_key, device_id):

    # Establish request endpoint
    endpoint = api_endpoint+project+"/"+version+"?api_key="+api_key+"?device="+device_id
    api_data = requests.get(endpoint)

    # query weights and metadata
    if api_data.status_code != 200:
        return 'error retrieving model specifications from server - does ' + endpoint + ' exist?', 400
    api_data = api_data.json()
    if 'limit_hit' in api_data.keys():
        return 'you have hit the limit of deployments of ' + project+"/"+version + ' to OAK devices - please contact Roboflow to expand your deployment limitations.', 400
    if 'warning' in api_data.keys():
        print(api_data['warning'], flush=True)

    # cache weights and metadata
    model_objects = {}
    model_objects['class_names'] = api_data['oak']['classes']
    model_objects['colors'] = api_data['oak']['colors']
    model_objects['environment'] = requests.get(api_data['oak']['environment']).json()
    r = requests.get(api_data['oak']['model'])
    try:
        os.makedirs(os.path.join(cache_dir, project, version))
    except OSError as error:
        print(error)
    with open(os.path.join(cache_dir, project, version, 'roboflow.blob'), 'wb') as f:
        f.write(r.content)
    with open(os.path.join(cache_dir, project, version, 'config.txt'), 'w') as f:
        f.write(json.dumps(model_objects))

    return os.path.join(cache_dir, project, version)
