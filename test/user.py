import traceback
from locust import HttpUser, task, between, TaskSet


class UserTest(TaskSet):
    ...