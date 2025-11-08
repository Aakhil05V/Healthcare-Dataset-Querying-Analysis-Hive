from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class HiveQueryExecutor:
    def __init__(self):
        self.query_history = []
        self.results_cache = {}
    
    def execute_query(self, query):
        try:
            self.query_history.append({
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
            
            sample_results = {
                'columns': ['ID', 'Patient_Name', 'Age', 'Diagnosis', 'Treatment'],
                'data': [
                    [1, 'John Doe', 45, 'Hypertension', 'Medication'],
                    [2, 'Jane Smith', 32, 'Diabetes', 'Diet & Exercise'],
                    [3, 'Bob Johnson', 58, 'Heart Disease', 'Surgery'],
                    [4, 'Alice Brown', 41, 'Cancer', 'Chemotherapy']
                ],
                'row_count': 4,
                'execution_time': '0.5s'
            }
            
            return {'success': True, 'results': sample_results}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_query_history(self):
        return self.query_history[-10:]

executor = HiveQueryExecutor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        query_text = data.get('query', '')
        
        if not query_text:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        result = executor.execute_query(query_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    return jsonify({'history': executor.get_query_history()})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
