from flask import Flask, render_template, request, redirect, url_for
from random import choice

app = Flask(__name__)

lead_A = []
lead_B = []
clientes = 0
clientes_A = 0
clientes_B = 0

def divide_trafego():
    return choice(['page_a.html', 'page_b.html'])

@app.route('/')
def landing_page():
    global clientes, clientes_A, clientes_B 
    versao = divide_trafego()
    clientes += 1
    if versao == 'page_a.html':
        clientes_A += 1
    elif versao == 'page_b.html':
        clientes_B += 1
    return render_template(versao)


@app.route('/submit', methods=['POST'])
def submit_form():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form.get('telefone', None)
    lead = {'nome': nome, 'email': email, 'telefone': telefone}
    
    if 'A' in request.form.get('versao', ''):
        lead_A.append(lead)
    elif 'B' in request.form.get('versao', ''):
        lead_B.append(lead)

    return redirect(url_for('landing_page'))

@app.route('/resultados')
def analisar_resultados():
    global clientes, clientes_A, clientes_B

    individual_conversao_A = (len(lead_A) / clientes_A) * 100 if clientes_A > 0 else 0
    individual_conversao_B = (len(lead_B) / clientes_B) * 100 if clientes_B > 0 else 0
    taxa_conversao_site = ((len(lead_A) + len(lead_B)) / clientes) * 100 if clientes > 0 else 0

    return f'Taxa de Conversão Lead/Cliente: {individual_conversao_A:.4f}% para a versão A e {individual_conversao_B:.4f}% para a versão B. Total de visitas: {clientes}. Taxa de conversão do site: {taxa_conversao_site:.4f}%'

if __name__ == '__main__':
    app.run(debug=True)
