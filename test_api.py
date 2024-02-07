import unittest
from flask import Flask
from api import app
from MongoDBConnection import MongoDBConnection

mongo_connection = MongoDBConnection("mongodb+srv://") # Sua URL de conexão

class TestApp(unittest.TestCase):

    def setUp(self):
        # Configuração inicial antes de cada teste
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        # Limpeza após cada teste
        pass

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Results', response.data)

    def test_record_test_result(self):
        # Simula um novo resultado de teste
        test_data = {
            "test_name": "Unit Test 1",
            "status": "Approved",
            "comparison_variable": {"key": "value"},
            "content": "Test content",
            "expected": "Expected result"
        }

        response = self.app.post('/api/test_results', json=test_data)
        self.assertEqual(response.status_code, 201)
        result_id = response.json['result_id']

        # Tenta obter o resultado recém-registrado
        response = self.app.get(f'/api/test_results/{result_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['test_result']['test_name'], "Unit Test 1")

    def test_invalid_test_result(self):
        # Tenta registrar um resultado de teste inválido (sem test_name)
        invalid_test_data = {
            "status": "Failed",
            "comparison_variable": {"key": "value"},
            "content": "Test content",
            "expected": "Expected result"
        }

        response = self.app.post('/api/test_results', json=invalid_test_data)
        self.assertEqual(response.status_code, 500)

    def test_delete_test_result(self):
        # Simula um novo resultado de teste
        test_data = {
            "test_name": "Unit Test 2",
            "status": "Approved",
            "comparison_variable": {"key": "value"},
            "content": "Test content",
            "expected": "Expected result"
        }

        response = self.app.post('/api/test_results', json=test_data)
        self.assertEqual(response.status_code, 201)
        result_id = response.json['result_id']

        # Tenta excluir o resultado recém-registrado
        response = self.app.delete(f'/api/test_results/{result_id}')
        self.assertEqual(response.status_code, 200)

        # Tenta obter o resultado excluído
        response = self.app.get(f'/api/test_results/{result_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
