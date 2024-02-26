import requests
import json
import time
import os 
import hashlib

from config import config

class StableController():
    def __init__(self):
        self.url = config.stable_url

    def txt2img(self, payload):
        r = requests.post(self.url + "/sdapi/v1/txt2img", json=payload) 
        r = r.json()
        hash = hashlib.sha256(payload["prompt"].encode('UTF-8')).hexdigest()
        save_location = os.path.join(os.getcwd(), "data", "stable", "outputs", "txt2img-images", hash[0:8])
        files = []
        for file in os.listdir(save_location):
            file = {
                "num":int(file.split("-")[0]),
                "loc":os.path.join(save_location, file)
            }
            files.append(file)
        files.sort(key=lambda x: x["num"], reverse=True)
        return [file["loc"] for file in files][0:payload["batch_size"]*payload["n_iter"]]


    '''
    def process_request(self, r):
        images = []
        for img in r["images"]:
            image = Image.open(io.BytesIO(base64.b64decode(img.split(",",1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + img
            }
            response2 = requests.post(url=f'{self.url}/sdapi/v1/png-info', json=png_payload)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            img_loc = f"db/samples/{uuid4()}.png"
            image.save(img_loc, pnginfo=pnginfo)
            images.append(img_loc)
        return images
    '''
    
    def txt2gif(self, payload):
        r = requests.post(self.url + "/sdapi/v1/txt2img", json=payload)
        print(r.json())
        #wait for file to be created
        time.sleep(1)
        save_location = os.path.join(os.getcwd(), "data", "stable", "outputs", "txt2img-images", "travels")
        # get the most recent folder
        folders = [os.path.join(save_location, folder) for folder in os.listdir(save_location)]
        folders.sort(key=os.path.getmtime)
        folder = folders[-1]
        # get mp4 file
        files = [os.path.join(folder, file) for file in os.listdir(folder)]
        for file in files:
            if file.endswith(".mp4"):
                return [file]
        return None
    
    def is_server_ready(self):
        try:
            r = requests.get(self.url + "/", timeout=1)
            return True
        except:
            return False
        
    def get_scripts(self):
        r = requests.get(self.url + "/sdapi/v1/scripts")
        scripts = json.loads(r.text)
        script_list = []
        for value in scripts.values():
            script_list.extend(value)
        return script_list
    
    def get_script_args(self, script):
        r = requests.get(self.url + "/sdapi/v1/script-info")
        scripts = json.loads(r.text)
        for key, value in scripts.items():
            if key == "name" and value == script:
                return scripts["args"]
    
    def get_models(self):
        r = requests.get(self.url + "/sdapi/v1/sd-models")
        models = json.loads(r.text)
        return models
    
    def check_unfinished(self):
        r = requests.get(self.url + "/sdapi/v1/unfinished")
        return json.loads(r.text)