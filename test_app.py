import unittest
import json
from app import create_app
from models import db, User, Challenge, Pilot, Application

class GovPilotIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_01_public_routes(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GovPilot', response.data)

        response = self.client.get('/demo-tour')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Demo Tour', response.data)

        response = self.client.get('/knowledge-library')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/search?q=bus')
        self.assertEqual(response.status_code, 200)

    def test_02_ai_challenge_assistant(self):
        # Login as gov officer
        self.client.get('/quick-login/government', follow_redirects=True)
        response = self.client.post(
            '/challenges/ai-assist',
            data=json.dumps({'prompt': 'We have frequent potholes and manual road inspections take 3 weeks per zone.'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('title', data)
        self.assertIn('expected_outcome', data)
        self.assertIn('suggested_kpis', data)

    def test_03_government_workflow(self):
        self.client.get('/quick-login/government', follow_redirects=True)
        
        # Dashboard
        r = self.client.get('/dashboard/government')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Government Innovation Command Center', r.data)

        # Challenges
        r = self.client.get('/challenges')
        self.assertEqual(r.status_code, 200)

        # View Hero Challenge
        r = self.client.get('/challenges/1')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'CH-TRANS-2026-001', r.data)

        # Comparison Matrix
        r = self.client.get('/challenges/1/comparison')
        self.assertEqual(r.status_code, 200)

        # Pilot Passport (10 tabs)
        r = self.client.get('/pilots/1')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'GP-MH-2026-00421', r.data)

        # Scale Pack HTML & PDF
        r = self.client.get('/pilots/1/scale-pack')
        self.assertEqual(r.status_code, 200)

        r_pdf = self.client.get('/pilots/1/scale-pack/download-pdf')
        self.assertEqual(r_pdf.status_code, 200)
        self.assertEqual(r_pdf.content_type, 'application/pdf')
        self.assertTrue(len(r_pdf.data) > 1000)

    def test_04_startup_workflow(self):
        self.client.get('/quick-login/startup', follow_redirects=True)
        r = self.client.get('/dashboard/startup')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/startups/1')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'TransitAI Labs', r.data)

    def test_05_evaluator_workflow(self):
        self.client.get('/quick-login/evaluator', follow_redirects=True)
        r = self.client.get('/dashboard/evaluator')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/evaluations')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/applications/1/evaluate')
        self.assertEqual(r.status_code, 200)

    def test_06_validator_workflow(self):
        self.client.get('/quick-login/validator', follow_redirects=True)
        r = self.client.get('/dashboard/validator')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/validation')
        self.assertEqual(r.status_code, 200)

    def test_07_admin_and_api(self):
        self.client.get('/quick-login/admin', follow_redirects=True)
        r = self.client.get('/dashboard/admin')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/admin/users')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/admin/audit-logs')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/admin/departments')
        self.assertEqual(r.status_code, 200)

        # API Endpoints
        r = self.client.get('/api/challenges')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/api/startups')
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/api/pilots/1/kpis')
        self.assertEqual(r.status_code, 200)
        kpi_json = json.loads(r.data)
        self.assertEqual(kpi_json['pilot_code'], 'GP-MH-2026-00421')
        self.assertEqual(len(kpi_json['kpis']), 4)

if __name__ == '__main__':
    unittest.main()
