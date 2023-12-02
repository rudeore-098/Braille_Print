from flask import Flask, request, render_template
from googletrans import Translator
import subprocess
import setup
import code_3rd
import dot_data
#지금 안되는거 : 한번 번역해서 출력하면 다음번역이 제대로 안됨..ㅠ 
app = Flask(__name__)

def braille_translate(text):
    code_3rd.init(text)
    setup.start()
    code_3rd.end()
    setup.end()

# Function to translate text between Korean and English using Google Translate API
def translate_text(text, source_language='ko', target_language='en'):
    translator = Translator()
    try:
        translated_text = translator.translate(text, src=source_language, dest=target_language)
        # braille_translate(translated_text.text)
        return translated_text.text
    except Exception as e:
        return f"Translation Error: {e}"

def run_runcode():
    subprocess.run(["python3", "Runcode.py"])




# Route for the home page
@app.route("/", methods=['GET', 'POST'])
def index():
    input_text = ''
    translated_text = '번역 결과'
    if request.method == 'POST':
        if 'trans_button' in request.form:

            input_text = request.form['input_text']
            source_language = request.form['source_language']
            target_language = request.form['target_language']

            # 번역 결과를 가져와서 전역 변수에 저장
            translated_text = translate_text(input_text, source_language, target_language)

        elif 'print_button' in request.form:
            translated_text = request.form['output_text']
            print('번역된 언어 :', translated_text, '번역 시작 ~!')
            braille_translate(translated_text)
            print("Braille_Print 버튼이 클릭되었습니다.")



    # HTML에 전달
    return render_template("index.html", input_text=input_text, translated_txt=translated_text)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
