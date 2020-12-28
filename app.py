import requests
import pickle as pk
import cloudpickle as cp
import urllib.request
import flask
from multiprocessing import Pool
from simpletransformers.language_generation import LanguageGenerationModel

"""cp_model = cp.load(open("cp_model.pickle", 'rb'))
jb_model = cp.load(open("jb_model.pickle", 'rb'))
adele_model = cp.load(open("adele_model.pickle", 'rb'))
bm_model = cp.load(open("bm_model.pickle", 'rb'))
mj_model = cp.load(open("mj_model.pickle", 'rb'))"""

app = flask.Flask(__name__, template_folder='templates')


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: 
                f.write(chunk)


@app.route('/', methods=['GET', 'POST'])
def main():
    res = ""
    if flask.request.method == 'GET':
        return(flask.render_template('main.html', vis="hidden"))
    if flask.request.method == 'POST':

        if flask.request.form["Artist"] == "Justin Beiber":
            jb_model = cp.load(open("jb_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = jb_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res + "\n \n -JUSTIN BIEBER",)

        if flask.request.form["Artist"] == "MIX!!":
            file_id = '1WXcesEjsVX0GPg6i5ARd_bMUFo7RgJS_'
            destination = 'D:\ML-Projects\gpt2-lyrics-generator\mix_model.pickle'
            download_file_from_google_drive(file_id, destination)
            mix_model = cp.load(open("mix_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = mix_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res,)

        if flask.request.form["Artist"] == "Eminem":
            em_model = cp.load(open("em_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = em_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res + "\n\n - Eminem",)

        if flask.request.form["Artist"] == "ColdPlay":
            cp_model = cp.load(open("cp_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = cp_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res + "\n \n (COLDPLAY)",)

        if flask.request.form["Artist"] == "Adele":
            adele_model = cp.load(open("adele_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = adele_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res+"\n \n  (ADELE)",)

        if flask.request.form["Artist"] == "Bruno Mars":
            bm_model = cp.load(open("bm_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = bm_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res + "\n \n  (BRUNO MARS)",)

        if flask.request.form["Artist"] == "Michael Jackson":
            mj_model = cp.load(open("mj_model.pickle", 'rb'))
            prompt = flask.request.form['prompt']
            max_len = flask.request.form['length']
            gen = mj_model.generate(
                prompt, args={"max_length": int(max_len)}, verbose=True)
            for line in gen[0].split('.')[:-1]:
                res = res + line + "\n"
                print(line)
            return flask.render_template('main.html', vis="hidden", result=res + "\n \n (MICHAEL JACKSON)",)

        return flask.render_template('main.html', vis="hidden", result="NOTHING :(",)


if __name__ == '__main__':
    app.run()
