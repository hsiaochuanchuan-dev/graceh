from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Your Google Sheet published URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS1sC2-QtEOVimTbL8SWV974iaFbBrEsU9Q1J63d61L01jzL5FRsgQSGyIOpn8X6A/pubhtml?gid=1066747437&single=true"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            return jsonify({'error': 'No table found'}), 404
        
        table = tables[0]
        rows = []
        
        for tr in table.find_all('tr'):
            cells = []
            for cell in tr.find_all(['th', 'td']):
                cells.append(cell.get_text(strip=True))
            if cells:
                rows.append(cells)
        
        return jsonify({'data': rows})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates folder
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Move the HTML file to templates folder
    import shutil
    if os.path.exists('grace-dividend.html'):
        shutil.copy('grace-dividend.html', 'templates/index.html')
    
    print("Starting server at http://localhost:5000")
    app.run(debug=True, port=5000)