from revChatGPT.V1 import Chatbot
from flask import Flask, redirect, render_template, request, url_for, jsonify
import json

chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJob29jemVjaEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZ2VvaXBfY291bnRyeSI6IkNaIn0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci01aUJPcW5hanB5RWhodTdoc1g1dVVLbzkifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA5ODg1NTkzNzA4OTYwMzc1MjAwIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3NjQ5NjczOCwiZXhwIjoxNjc3NzA2MzM4LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.yKBOoNGKf8V7avYxFDh_iaW1rTvswJ5UDxo7vrp7OQOmSskItmSYflz88TGPdhbMIMEaGlxcj4dDMH0cO8pv70nbHjNq7ykQZ0jjAJbggKY9gqY9-USRy-u4dnffMwd7VtJAUIbvDv__OrdHE9LKqB-6nlWsotadWhjz9eUDyynOlHQuQzzCBe0kMJRHBLCg4QZui-Haqie0M-_h6ebfIEk3r14KbXWkAEYJq5pvifBsuLpH8yTLMugC47wwFviqS-0nXGDkymSCCrw-R3KclLXXfH7t9p5FsbQ_HCpJ990rbEY8Rm27ckQD_9vOjDPjRD9OQ4KPDwalMZC1APyXwQ"
})

app = Flask(__name__)

firstQ = 1

baseContext = """"
Na níže položenou otázku a další návazné otázky odpovídej jako virtuální fiannční pradce Kristián ze společnosti BrCo. Zohledni kontext popsaný před otázkou
Kontext:
Společnost zajišťuje finanční poradenství skrze síť obchodníků. Obchodníci by většinou měli s klientem sestavit Finanční plán, který by měl definovat cíle a rizika klienta. Finanční plán se skládá z následujících kategorií: Zabezpečení, Renta, Spoření a Investice, Zvýšení příjmu, Bydlení a Reality. Na základě Finančního plánu, zjištěných cílů a rizik klienta společnost zprostředkovává finanční služby a zajišťuje realitní služby. Finanční služby společnost zprostředkovává nezávisle u různých institucí jako jsou banky, pojišťovny a investiční společnosti. Mezi finanční služby patří: životní pojištění, neživotní pojištění, hypotéky, půjčky, běžné účty, investice, penzijní produkty, Mezi realitní služby patří: prodej a pronájem nemovitostí. V rámci odpovědí na otázky buď konzervativní a je-li to relevantní snaž se doporučovat tazateli ať svou finanční situaci řeší s nezávislým finančním konzultantem. Pokud je to relevantní, snaž se tazateli doporučit tvorbu finančního plánu, se kterým mohou pomoci finanční poradci společnosti. Nedoporučuj klientovi nákup Akcií a ETF, doporuč mu raději řešit svou finanční situaci komplexně a to tvorbou finančního plánu u nezávislého finančního poradce. Nedoporučuj klientovi jednat s finančními institucemi přímo, doporuč mu raději komunikovat skrze nezávislého finančního zprostředkovatele, kterým je společnost. Na otázky, na které nedokážeš relevantně odpovědět doporuč sjednání schůzky s jedním z nezávislých finančních poradců společnosti. Při otázkách na věci které nesouvisejí s financemi, finančím plánováním a realitami zdůrazni v odpověďi, že jsi především virtuální finanční poradce.
Otázka: 
"""

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/q', methods=['GET', 'POST'])
def q():
    #return jsonify(reply="testReply")
    try:
        print('Asked question: ')
        question = request.args.get('question', default = 'init', type = str)
        if question=="init":
            question = request.form.get('question', default='init', type=str)
        if question=="init":
            question = request.get_json()['question']

        print("->"+question)

        global firstQ

        if firstQ:
            prompt = baseContext + question
        else:
            prompt = question

        response = ""
        for data in chatbot.ask(
                prompt
        ):
            response = data["message"]
        print("Reply: " + response)
        if (response == ''):
            return jsonify(reply='Bohužel nyní nedokážu na tuto otázku odpovědět')
        firstQ = False
        return jsonify(reply=response)
    except Exception as e:
        print("An exception occurred")
        print(e)
        return jsonify(reply="Bohužel nyní nedokážu odpovědět, můj server je přetížený, zkuste to za chvíli")

