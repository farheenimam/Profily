from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

system_prompt = """
You are a career consultant. Your job is to provide personalized career advice based on the user's input. Refer to the user as you.
The user will provide answers to specific questions about their educational level, interests, skills, career preferences, work style, and future goals. 
Use this information to suggest suitable career paths, industries, and next steps. Be descriptive, helpful, and tailor your advice to the user's unique profile.
Provide the user with links of th university and scholarships sites too. The length of the token in 2500 so keep the conversation limited to 2000 tokens.
Making sure that the whole converstaion completes in 2500 tokens.

Here are the questions the user has answered:
1. Current educational level: {ans1}
2. Subjects or fields of interest: {ans2}
3. Top skills or strengths: {ans3}
4. Preference for working with technology, people, numbers, or creative tasks: {ans4}
5. Preference for high-paying career or passion-aligned career: {ans5}
6. Preference for stable job or dynamic, high-growth field: {ans6}
7. Willingness to relocate: {ans7}
8. Preference for working alone or in a team: {ans8}
9. Preferred work environment (office, remote, or field): {ans9}
10. Plans for higher education or certifications: {ans10}
11. Which country are your from? {ans11}
12. Additional details: {ans12}

Use this information to provide tailored career advice.
"""


api = OpenAI(api_key=API_KEY, base_url=BASE_URL)

@app.route("/get_career_advice", methods=["POST"])
def get_career_advice():
    data = request.json  # Retrieve JSON data from the request

    # Extract answers
    ans1 = data.get("ans1", "")
    ans2 = data.get("ans2", "")
    ans3 = data.get("ans3", "")
    ans4 = data.get("ans4", "")
    ans5 = data.get("ans5", "")
    ans6 = data.get("ans6", "")
    ans7 = data.get("ans7", "")
    ans8 = data.get("ans8", "")
    ans9 = data.get("ans9", "")
    ans10 = data.get("ans10", "")
    ans11 = data.get("ans11", "")
    ans12 = data.get("ans12", "")

    # User prompt with the answers
    user_prompt = f"""
    Current educational level: {ans1}
    Subjects or fields of interest: {ans2}
    Top skills or strengths: {ans3}
    Preference for working with technology, people, numbers, or creative tasks: {ans4}
    Preference for high-paying career or passion-aligned career: {ans5}
    Preference for stable job or dynamic, high-growth field: {ans6}
    Willingness to relocate: {ans7}
    Preference for working alone or in a team: {ans8}
    Preferred work environment (office, remote, or field): {ans9}
    Plans for higher education or certifications: {ans10}
    Lives in: {ans11}
    Additional details: {ans12} 

    Based on this information, provide personalized career advice. It should be detailed and full professional. Also take into noting the country and guide according to it. 
    For example if the feild that user has interest has scope in their country. If not then recommend other countries that have scope of that feild. Also tell about scholarships
    if the users mention about it. Provide them with the link. If the users mention multiple interest. Categorize them and help them recognize in which feild they have more 
    passion by giving them breifing about each and letting them decide. Try to keep the answer structured by categorizing it. Provide me with resources too liek the link of the sites.
    Just give answer under headings dont generate tables or anything.The length of the token in 2000 so keep the conversation limited to 1000 tokens.
    Making sure that the whole converstaion completes in 2500 tokens. The answer shouldnt be more than 2000 tokens also in the end print the line. Thank you for choosing Profily.
    """
    completion = api.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=2500,
    )

    response = completion.choices[0].message.content

    # print("User:", user_prompt)
    print("AI:", response)
    response = completion.choices[0].message.content
    return jsonify({"response": response})  # Return the response as JSON

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
