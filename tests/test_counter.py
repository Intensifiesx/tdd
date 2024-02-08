"""
Test Cases for Counter Web Service

Create a service that can keep track of multiple counters:
-API must be RESTful, following the guidelines specified in status.py.
-The endpoint should be called /counters.
-When creating a counter, specify the name in the path.
-Duplicate names must return a conflict error code.
-The service must be able to update a counter by name.
-The service must be able to read the counter.
"""

from unittest import TestCase
# Import the unit under test - counter
from src.counter import app
# Import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""
    
    def setUp(self):
        """Test setup"""
        self.client = app.test_client()
        self.client.testing = True
        
    def test_create_counter(self):
        """Test creating a counter"""
        response = self.client.post('/counters/foo')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_duplicate_counter(self):
        """Test handling duplicate counters"""
        self.client.post('/counters/bar')
        response = self.client.post('/counters/bar')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_update_counter(self):
        """Test updating a counter"""
        # Create a counter
        self.client.post('/counters/updating')
        # Update the counter
        response = self.client.post('/counters/updating')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the updated counter value
        updated_response = self.client.get('/counters/updating')
        updated_data = updated_response.get_json()
        self.assertEqual(updated_data['value'], 1)  # Assuming the initial value is 0
    
    def test_read_counter(self):
        """Test reading a counter"""
        self.client.post('/counters/read')
        response = self.client.get('/counters/read')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_counter(self):
        """Test deleting a counter"""
        self.client.post('/counters/foo_delete')
        response = self.client.delete('/counters/foo_delete')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if counter exists after deletion
        response = self.client.get('/counters/foo_delete')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
