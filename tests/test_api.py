from app import app


def test_get_gene_suggest():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/gene_suggest?species=homo_sapiens&query=te&limit=3')
        assert response.status_code == 200
        assert response.json == {"gene_names": [{"0": "ASTE1"}, {"1": "ATE1"}, {"2": "ATE1-AS1"}]}

        # Test wrong 'sepecies' parameter
        response = test_client.get('/gene_suggest?species=homo_sapient&query=te&limit=3')
        assert response.status_code == 400
        assert response.json == {"description": "Species does not exist", "error": 400, "name": "Bad Request"}