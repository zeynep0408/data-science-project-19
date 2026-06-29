import pytest
import pandas as pd
import numpy as np
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks.task_manager import *

def test_generate_magic_power_scores():
    scores = generate_magic_power_scores(100)
    assert len(scores) == 100
    assert isinstance(scores, np.ndarray)

def test_standardize_scores():
    result = standardize_scores(np.array([70, 75, 80]))
    assert np.isclose(result[0], -1.0)

def test_assign_house():
    assert assign_house(95) == "Gryffindor"
    assert assign_house(60) == "Ravenclaw"

def test_calculate_z_score():
    assert calculate_z_score(85, 75, 5) == 2.0

def test_get_top_n_characters_by_power():
    result = get_top_n_characters_by_power(np.array([80, 55, 90]), ["Harry", "Ron", "Hermione"], 2)
    assert result == ["Hermione", "Harry"]

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://kaizu-api-8cd10af40cb3.herokuapp.com/projectLog"
    payload = {
        "user_id": 403,
        "project_id": 667,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()
