from flask import Flask, render_template, request
import openai
from serpapi import GoogleSearch
from flask_cors import CORS,cross_origin
from config import OPENAI_API_KEY
import re
app = Flask(__name__)

openai.api_key = OPENAI_API_KEY

@app.route("/")
@cross_origin()
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
@cross_origin()
def generate():
    try:
        query = ""
        gift_description = request.form["gift_description"] + "Please suggest me a gift and please provide only gift name not other sentence"
        response = openai.Completion.create(engine="text-davinci-002", prompt=gift_description, max_tokens=1024)
        text = response["choices"][0]['text']
        match = re.search(r".*?\r\n\r\n(.*)", text)
        if match:
            query = match.group(1)
        params = {
            "engine": "google_shopping",
            "q": query,
            "location": "INDIA",
            "hl": "en",
            "gl": "in",
            "api_key": "67b1821bbf042d3b8f144d8a8489a1133f74d01833f537ae388dab09b3947500"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        shopping_results = results["shopping_results"]
        return render_template("product.html", product_name=shopping_results, quer = query)
    except Exception as e:
        print("the Exception message is: ", e)
        return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)



