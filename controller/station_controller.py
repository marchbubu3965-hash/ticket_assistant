class StationController:
    def __init__(self, repo):
        self.repo = repo

    def search(self, keyword: str):
        if not keyword or len(keyword) < 1:
            return []
        return self.repo.search(keyword)
