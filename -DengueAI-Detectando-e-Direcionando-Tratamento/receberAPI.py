# from flask import Flask, request, jsonify
# from predicaoSintomas import dataAcess

# app = Flask(__name__)


# @app.route('/receber_dados', methods=['POST'])
# def receber_dados():
#     if request.method == 'POST':
#         data = request.json
#         resultado_previsao = dataAcess(data)
#         return jsonify({'resultado_previsao': resultado_previsao})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from opencage.geocoder import OpenCageGeocode
from predicaoSintomas import dataAcess


app = Flask(__name__)
CORS(app)

key = 'c098a7b3be6c4b4f9f14160c422559d5'
geocoder = OpenCageGeocode(key)

@app.route('/receber_data', methods=['POST'])
def receber_dados():
    dados_recebidos = request.json

    dados_transformados = {
        "nome": f"{dados_recebidos.get('nome', '')} {dados_recebidos.get('sobrenome', '')}",
        "febre": int(dados_recebidos.get('febre', 0)),
        "dor_cabeca": int(dados_recebidos.get('dor_de_cabeca', 0)),
        "dor_articulacoes": int(dados_recebidos.get('dor_nas_articulacoes', 0)),
        "sangramento": int(dados_recebidos.get('sangramento', 0)),
        "idade": int(dados_recebidos.get('idade', 0))
    }

    endereco_completo = f"{dados_recebidos.get('endereco', '')}, {dados_recebidos.get('numero', '')}, {dados_recebidos.get('bairro', '')}, {dados_recebidos.get('cidade', '')}, {dados_recebidos.get('estado', '')}, Brasil"

    resultados = geocoder.geocode(endereco_completo)

    if resultados:
        latitude = resultados[0]['geometry']['lat']
        longitude = resultados[0]['geometry']['lng']

        # Adicionar latitude, longitude e idade aos dados transformados
        dados_transformados["latitude"] = latitude
        dados_transformados["longitude"] = longitude

        print(dados_transformados)  # Imprimir os dados transformados
        resultado_previsao = dataAcess(dados_transformados)

        return jsonify({'resultado_previsao': resultado_previsao})
    else:
        print("Endereço não encontrado.")
        return jsonify({"error": "Endereço não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)



