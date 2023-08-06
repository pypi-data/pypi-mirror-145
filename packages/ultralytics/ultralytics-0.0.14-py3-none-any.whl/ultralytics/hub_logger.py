import threading
import time

import requests

from .config import HUB_API_ROOT
from .utils.general import PREFIX


class HUBLogger:
    api_url = HUB_API_ROOT + "model-checkpoint"

    def __init__(self, model_id, auth):
        self.model_id = model_id
        self.auth = auth
        self.rate_limit = 60.0  # minimum seconds between checkpoint uploads
        self.t = time.time()  # last upload time

    def on_model_save(self, *args, **kwargs):
        """
        Runs after each model save

        Args:
             *args     last, epoch, final_epoch, best_fitness, fi
        """

        # Set args
        last, epoch, final_epoch, best_fitness, fi = args[:5]
        is_best = best_fitness == fi

        if (time.time() - self.t) > self.rate_limit:
            print(f"{PREFIX}Uploading checkpoint for " + self.model_id)
            threading.Thread(target=self._upload_model, args=(epoch, is_best, last), daemon=True).start()
            self.t = time.time()

    def _upload_model(self, epoch, is_best, weights):
        payload = {"modelId": self.model_id, "epoch": epoch, "isBest": bool(is_best), "type": "epoch"}
        payload.update(self.auth.get_auth_string())

        with open(weights, "rb") as last:
            r = requests.post(self.api_url, data=payload, files={"last.pt": last})
            if r.status_code != 200:
                print(f"{PREFIX}Unable to upload checkpoint!")

    def on_pretrain_routine_end(self, *args, **kwargs):
        # Tell HUB that training has started
        payload = {"modelId": self.model_id, "type": "initial"}
        payload.update(self.auth.get_auth_string())
        requests.post(self.api_url, data=payload, files={"void": None})

    def on_train_end(self, *args, **kwargs):
        """"
        Args:

            *args   last, best, plots, epoch
        """
        # Set args
        last, best, plots, epoch, results = args[:5]

        # mAP0.5:0.95
        map_new = results[3]

        payload = {"modelId": self.model_id, "epoch": epoch, "map": map_new, "type": "final"}
        payload.update(self.auth.get_auth_string())

        print(f"{PREFIX}Uploading final models for " + self.model_id)
        with open(best, "rb") as best:
            r = requests.post(self.api_url, data=payload, files={"best.pt": best})
            if r.status_code != 200:
                print(f"{PREFIX}Unable to upload final models!")
