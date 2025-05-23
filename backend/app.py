from flask import Flask, request, jsonify
from flask_cors import CORS
from qa_bot import build_qa_bot
import os 

app = Flask(__name__)
CORS(app)
upload_folder="uploads/"
os.makedirs(upload_folder,exist_ok=True)
qa_chain = None

@app.route('/upload', methods=['POST'])
def upload():
    global qa_chain
    file= request.files['file']
    fp =os.path.join(upload_folder,file.filename)
    file.save(fp)
    qa_chain=build_qa_bot(fp)
    return jsonify({"status":"uploaded","file":file.filename})

@app.route('/ask', methods=['POST'])

def ask():
    if not qa_chain:return jsonify({"error": "No document uploaded yet."}), 400
    query= request.json.get("query")
    res=qa_chain.run(query)
    return jsonify({"query": query,"response": result})

if __name__=='__main__':app.run(debug=True, port=5000)