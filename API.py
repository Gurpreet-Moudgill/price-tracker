from flask import Flask, request, jsonify
from price_comparison import PriceCompare

app = Flask(__name__)
price_compare = PriceCompare()

@app.route('/api/find_price', methods=['POST'])
def find_price():
    data = request.json
    product = data.get('product')
    result = price_compare.find_price(product)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)