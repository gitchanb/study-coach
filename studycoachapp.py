from flask import Flask, render_template,request
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api_key =os.getenv ('GROQ_API_KEY')
client = Groq(api_key=api_key)

@app.route('/',methods=['GET','POST'])
def home():
    result = None
    if request.method == 'POST':
        topic = request.form['topic']
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert study coach. When given a topic, create a structured study plan with key concepts, resources, and daily schedule. Be specific and practical also at end concisely use 80/20 rule,prerequisite,metalearning ideas."},
                {"role": "user", "content": topic}
            ]
        )
        return render_template('index.html', response=response.choices[0].message.content)
    return render_template('index.html', response=None)
if __name__ == '__main__':
    app.run(debug=True)
