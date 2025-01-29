class FakeTask:
    """
    Fake celery task.
    """

    def __getattr__(self, name: str):
        return self

    def __call__(self, *args, **kwargs):
        return self


fake_task = FakeTask()
