from flask import Flask, request, render_template, jsonify
from datetime import datetime
from MongoDBConnection import MongoDBConnection
from bson import ObjectId  

# Criação de uma instância do Flask
app = Flask(__name__)

# Conexão com o MongoDB
mongo_connection = MongoDBConnection("mongodb+srv://") # Sua URL de conexão

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para registrar um novo resultado de teste
@app.route('/api/test_results', methods=['POST'])
def record_test_result():
    try:
        # Obtenção dos dados do JSON enviado na requisição
        data = request.json
        test_name = data.get("test_name")
        status = data.get("status")
        comparison_variable = data.get("comparison_variable")
        content = data.get("content")
        expected = data.get("expected")

        # Obtenção da data e hora atuais
        date_time = datetime.now()
        
        # Construção do documento a ser inserido no MongoDB
        result_data = {
            "test_name": test_name,
            "status": status,
            "datetime": date_time,
            "comparison_variable": comparison_variable,
            "content": content,
            "expected": expected,
        }

        # Inserção do documento na coleção do MongoDB
        inserted_result = mongo_connection.collection.insert_one(result_data)
        result_id = str(inserted_result.inserted_id)

        return jsonify({"message": "Test result recorded successfully", "result_id": result_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter um resultado de teste pelo ID
@app.route('/api/test_results/<result_id>', methods=['GET'])
def get_test_results_by_ID(result_id):
    try:
        # Consulta ao MongoDB para obter um resultado pelo ID
        result = mongo_connection.collection.find_one({"_id": ObjectId(result_id)})

        if result:
            # Converta o ObjectId para str antes de retornar
            result['_id'] = str(result['_id'])
            return jsonify({"test_result": result}), 200
        else:
            return jsonify({"message": "Test result not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Rota para obter todos os resultados de teste
@app.route('/api/test_results', methods=['GET'])
def get_test_results():
    try:
        # Consulta ao MongoDB para obter todos os resultados
        results = list(mongo_connection.collection.find())
        # Converta o ObjectId para str em cada documento
        for result in results:
            result['_id'] = str(result['_id'])
        return jsonify({"test_results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para deletar um resultado de teste pelo ID
@app.route('/api/test_results/<result_id>', methods=['DELETE'])
def delete_test_result(result_id):
    try:
        # Deleção do resultado pelo ID
        deleted_result = mongo_connection.collection.delete_one({"_id": ObjectId(result_id)})

        if deleted_result.deleted_count == 1:
            return jsonify({"message": "Test result deleted successfully"}), 200
        else:
            return jsonify({"message": "Test result not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para atualizar um resultado de teste pelo ID
@app.route('/api/test_results/<result_id>', methods=['PUT'])
def update_test_result(result_id):
    try:
        
        date_time = datetime.now()
        
        # Obtenção dos dados do JSON enviado na requisição
        data = request.json
        updated_data = {
            "test_name": data.get("test_name"),
            "status": data.get("status"),
            "comparison_variable": data.get("comparison_variable"),
            "content": data.get("content"),
            "expected": data.get("expected"),
            "updateAt": date_time,
        }

        # Atualização do resultado pelo ID
        updated_result = mongo_connection.collection.update_one({"_id": ObjectId(result_id)}, {"$set": updated_data})

        if updated_result.modified_count == 1:
            return jsonify({"message": "Test result updated successfully"}), 200
        else:
            return jsonify({"message": "Test result not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Execução da aplicação Flask
if __name__ == '__main__':
    app.run(debug=False)
