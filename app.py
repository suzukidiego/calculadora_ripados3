from flask import Flask, render_template, request
import math

app = Flask(__name__)

maior_lado_ripa_interna = 2.6
menor_lado_ripa_interna = 0.122
maior_lado_ripa_externa = 2.90
menor_lado_ripa_externa = 0.219


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comp_parede = float(request.form['comprimento'])
        altu_parede = float(request.form['altura'])
        linha = request.form['linha']
        operation = request.form['direção']

        if linha == 'Ripado externo':
            pre_comp_ripa = maior_lado_ripa_externa
            pre_altu_ripa = menor_lado_ripa_externa
        else:
            pre_comp_ripa = maior_lado_ripa_interna
            pre_altu_ripa = menor_lado_ripa_interna

        if operation == 'vertical':
            comp_ripa = pre_altu_ripa
            altu_ripa = pre_comp_ripa
        else:
            comp_ripa = pre_comp_ripa
            altu_ripa = pre_altu_ripa
    
####

        horiz_fracionado = comp_parede / comp_ripa
        horiz_inteira = comp_parede // comp_ripa #quantas ripas inteiras cabem
        horiz_espaco_restante = horiz_fracionado - horiz_inteira #qual o tamanho do espaço que vai sobrar
        horiz_espaco_restante_m = comp_parede - (horiz_inteira * comp_ripa)
        if horiz_espaco_restante_m == 0:
            horiz_rendimento_ripa = 0
        else:
            horiz_rendimento_ripa = comp_ripa // horiz_espaco_restante_m #quantos pedaços deste espaço que sobrou, dá pra fazer com uma ripa inteira

        vert_fracionado = altu_parede / altu_ripa   
        vert_inteira = altu_parede // altu_ripa #quantas ripas inteiras cabem
        vert_espaco_restante = vert_fracionado - vert_inteira
        vert_espaco_restante_m = altu_parede - (vert_inteira * altu_ripa) #qual o tamanho do espaço que vai sobrar
        if vert_espaco_restante_m == 0:
            vert_rendimento_ripa = 0
        else:
            vert_rendimento_ripa = altu_ripa // vert_espaco_restante_m #quantos pedaços deste espaço que sobrou, dá pra fazer com uma ripa inteira

####

        if horiz_espaco_restante_m <= 0:
            horiz_pedacos_necessarios = 0
        else:
            horiz_pedacos_necessarios = math.ceil(vert_fracionado)

        if vert_espaco_restante_m <= 0:
            vert_pedacos_necessarios = 0 
        else:
            vert_pedacos_necessarios = horiz_inteira

####

        if horiz_pedacos_necessarios == 0:
            horiz_ripa_inteira_para_pedaco = 0
        else:
            horiz_ripa_inteira_para_pedaco = horiz_pedacos_necessarios / horiz_rendimento_ripa
        
        if vert_pedacos_necessarios == 0:
            vert_ripa_inteira_para_pedaco = 0
        else:
            vert_ripa_inteira_para_pedaco = vert_pedacos_necessarios / vert_rendimento_ripa
        
####

        total_ripas = (horiz_inteira * vert_inteira) + horiz_ripa_inteira_para_pedaco + vert_ripa_inteira_para_pedaco

        total_ripas_com_margem = total_ripas * 1.1
           
        result = round(total_ripas_com_margem,0)
        
        return render_template('index.html', result=result)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)