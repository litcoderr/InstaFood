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
        raw_results = self.searcher.extract_recent_tag(query) # retrieve when done
        result = self.extract_result(raw_results) # preprocess and make in to json object

        self.task[request_id]["is_running"] = False
        self.results[request_id] = result
        # print(self.results[request_id])

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

    def extract_result(self, raw_result):
        results = []
        for post in raw_result: # for every instagram post object
            post_object = {}
            post_object["post_id"] = post.post_id
            post_object["code"] = post.code
            post_object["caption"] = post.processed_text()
            post_object["user"] = self.extract_user(post.user)
            post_object["display_src"] = post.display_src
            post_object["is_video"] = post.is_video
            post_object["created_at"] = post.created_at
            results.append(post_object)

        return results
    
    def extract_user(self, user):
        result = {}
        # process user info
        result["id"] = user.id
        result["username"] = user.username
        result["bio"] = user.bio
        result["followers_count"] = user.followers_count
        result["following_count"] = user.following_count
        result["is_private"] = user.is_private
        return result

if __name__ == "__main__":
    api = API()
    hash_id = hash(time.time())
    print(api.get(hash_id, "한양대맛집"))