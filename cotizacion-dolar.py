import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = 'https://www.rofex.com.ar/cem/Spot.aspx'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'ctl00_gvwDDF'})
        data = []

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0:
                posicion = cells[0].get_text()
                ajuste = cells[1].get_text()
                var_porcentaje = cells[2].get_text()
                data.append({'Posición': posicion, 'Ajuste': ajuste, 'Var. %': var_porcentaje})

        return jsonify(data)
    else:
        return jsonify({'error': 'Error al obtener la página web.'})

if __name__ == '__main__':
    app.run(debug=True)
