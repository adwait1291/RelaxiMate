from flask import Flask, request, jsonify
from semantic_search import SemanticSearch
from gpt_caller import generate_answer
from gpt_caller import load_recommender

app = Flask(__name__)
initialized = False 
recommender = None

with app.app_context():
    if not initialized:
        recommender = SemanticSearch()
        book_path = "Mindfulness for Teen Anxiety. A Workbook for Overcoming Anxiety at Home, at School, and Everywhere Else.pdf"
        load_recommender(book_path, recommender)
        print("Initialization code executed once.")
        initialized = True

@app.route('/')
def ok():
    return "Hello!"

@app.route('/ask')
def answer():
    input_string = request.args.get('input_string')
    
    if input_string is None:
        return jsonify({'error': 'Input string is required'}), 400
    
    output_string = generate_answer(input_string, recommender)
    
    response = {'answer': input_string, 'reversed_string': output_string}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='10.0.4.140', port=5000, debug=True)
