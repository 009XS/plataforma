
import sys
import os
import unittest

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class SecurityTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing

    def test_protected_routes(self):
        """Verify that routes are protected against unauthenticated access"""
        endpoints = [
            ('/panel-alumno', 302, 'GET'),
            ('/panel-docente', 302, 'GET'),
            ('/api/crear-usuario', 302, 'POST'), # Should redirect if login_required works
            ('/api/crear-tarea', 302, 'POST'),
        ]

        for endpoint, expected_status, method in endpoints:
            with self.subTest(endpoint=endpoint):
                if method == 'GET':
                    response = self.client.get(endpoint)
                else:
                    response = self.client.post(endpoint)
                
                # We expect redirect (302) to login page
                self.assertEqual(response.status_code, expected_status, 
                                 f"Endpoint {endpoint} returned {response.status_code} instead of {expected_status}")

    def test_crear_usuario_method_not_allowed(self):
        """Test GET request to POST-only route"""
        # GET to /api/crear-usuario should return 405 Method Not Allowed
        # BUT since it has @login_required, it might redirect (302) FIRST if decorators run before method check?
        # Actually in Flask, simple method check happens at routing.
        response = self.client.get('/api/crear-usuario')
        self.assertIn(response.status_code, [405, 302], 
                      f"GET to /api/crear-usuario returned {response.status_code}")

if __name__ == '__main__':
    unittest.main()
