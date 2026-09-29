from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert 'EduGenie' in response.text


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_validation():
    response = client.post('/qa', json={'question': ''})
    assert response.status_code == 422


def test_quiz_schema_validation():
    from quiz_module import QuizResponse
    data = {
        'questions': [
            {'question': 'Q1', 'options': ['A', 'B', 'C', 'D'], 'correct_answer': 'A', 'explanation': 'Because A.'},
            {'question': 'Q2', 'options': ['A', 'B', 'C', 'D'], 'correct_answer': 'B', 'explanation': 'Because B.'},
            {'question': 'Q3', 'options': ['A', 'B', 'C', 'D'], 'correct_answer': 'C', 'explanation': 'Because C.'},
        ]
    }
    assert len(QuizResponse.model_validate(data).questions) == 3
