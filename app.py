from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
from opencage.geocoder import OpenCageGeocode
from pages.Algoritmos.Otimization_Clustering import general
from pages.Algoritmos.predicaoSintomas import dataAcess
import os

app = Flask(__name__)
CORS(app)

key = 'c098a7b3be6c4b4f9f14160c422559d5'
geocoder = OpenCageGeocode(key)

root_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pages/<path:filename>')
def serve_static_pages(filename):
    return send_from_directory(os.path.join(app.root_path, 'pages'), filename)


@app.route('/pages/js/<path:filename>')
def serve_static_js(filename):
    return send_from_directory(os.path.join(app.root_path, 'pages', 'js'), filename)


@app.route('/pages/styles/<path:filename>')
def serve_static_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'pages', 'styles'), filename)

@app.route('/pages/images/<path:filename>')
def serve_static_images(filename):
    return send_from_directory(os.path.join(app.root_path, 'pages', 'images'), filename)


@app.route('/consulta')
def consulta():
    return render_template('index_consulta.html')

@app.route('/painel')
def painel():
    return render_template('index_painel.html')

@app.route('/hospitais')
def hospitais():
    return render_template('index_hospitais.html')

@app.route('/contaminacao')
def contaminacao():
    return render_template('index_contaminacao.html')

@app.route('/unidades')
def unidades():
    return render_template('index_unidades.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/mapa_hospitais')
def mapa_hospitais():
    return render_template('mapa_clusters_e_otimizacao1.html')

@app.route('/mapa_contaminacao')
def mapa_contaminacao():
    return render_template('mapa_clusters_e_otimizacao2.html')

@app.route('/mapa_unidades')
def mapa_unidades():
    return render_template('mapa_clusters_e_otimizacao3.html')


@app.route('/receber_data', methods=['POST'])
def receber_dados():
    try:
        dados_recebidos = request.json
        print(dados_recebidos)  # Imprimir os dados recebidos
        # Verificar se todos os campos necessários estão presentes nos dados recebidos
        campos_obrigatorios = ['nome', 'sobrenome', 'idade', 'endereco', 'numero', 'bairro', 'cidade', 'estado']
        for campo in campos_obrigatorios:
            if campo not in dados_recebidos:
                print(f'O campo obrigatório {campo} está ausente')
                return jsonify({'error': f'O campo obrigatório {campo} está ausente'}), 400

        dados_transformados = {
            "nome": f"{dados_recebidos.get('nome', '')} {dados_recebidos.get('sobrenome', '')}",
            "febre": int(dados_recebidos.get('febre', 0)),
            "dor_cabeca": int(dados_recebidos.get('dor_de_cabeca', 0)),
            "dor_articulacoes": int(dados_recebidos.get('dor_nas_articulacoes', 0)),
            "sangramento": int(dados_recebidos.get('sangramento', 0)),
            "idade": int(dados_recebidos.get('idade', 0))
        }
        print (dados_transformados)
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

    except Exception as e:
        print(f"Erro ao processar solicitação: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500
    



@app.route('/rodar_modelo', methods=['POST'])
def rodar_modelo():
    print("Modelo rodado com sucesso!")
    general()
    return jsonify({"message": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
