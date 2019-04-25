import instagram_api.backend as backend
import threading
import time

class Searcher(backend.HashTagSearch):
    def __init__(self):
        super().__init__()

    def retrieve(self, results):
        super().retrieve(results)
        """
        results contains instagram post object
        """
        return results

class API():
    def __init__(self):
        self.searcher = Searcher()
        self.task = {}
        self.results = {}

    def fetch(self, request_id, query):
        print("Start Fetching {}".format(request_id))
        results = self.searcher.extract_recent_tag(query) # retrieve when done

        self.task[request_id]["is_running"] = False
        self.results[request_id] = results
        print(self.results[request_id])

    def get(self, request_id, query):
        if request_id in self.task: # already running
            pass
        else: # first time running
            fetching_thread = threading.Thread(target=self.fetch, args=(request_id, query), daemon=True)
            fetching_thread.start()

            self.task[request_id] = {
                "is_running" : True,
                "thread" : fetching_thread
            } # True : running (not done)
            print("Task: {}".format(self.task))

if __name__ == "__main__":
    api = API()
    hash_id = hash(time.time())
    print(api.get(hash_id, "한양대맛집"))