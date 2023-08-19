from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Usuario:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.relatorio_vendas = []
        self.relatorio_compras = []
        self.anuncios = []
        self.perguntas_respostas = []
        self.lista_favoritos = []

class Anuncio:
    def __init__(self, id, titulo, descricao, preco, data_criacao, categoria, proprietario):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.data_criacao = data_criacao
        self.categoria = categoria
        self.proprietario = proprietario
        self.perguntas_respostas = []

class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

# Exemplos de listas para simular o banco de dados
usuarios = []
anuncios = []
categorias = []

# Funções auxiliares

def encontrar_usuario_por_email(email):
    for usuario in usuarios:
        if usuario.email == email:
            return usuario
    return None

# Definindo rotas

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        novo_usuario = Usuario(id=len(usuarios) + 1, nome=nome, email=email, senha=senha)
        usuarios.append(novo_usuario)
        return render_template('menu.html')
    return render_template('cadastrar_usuario.html')

@app.route('/acessar_conta', methods=['GET', 'POST'])
def acessar_conta():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = encontrar_usuario_por_email(email)
        if usuario and usuario.senha == senha:
            return redirect(url_for('menu_usuario', usuario_id=usuario.id))
        else:
            return "Email ou senha incorretos"
    return render_template('acessar_conta.html')

@app.route('/menu_usuario/<int:usuario_id>')
def menu_usuario(usuario_id):
    usuario = None
    for user in usuarios:
        if user.id == usuario_id:
            usuario = user
            break
    
    if usuario:
        return render_template('menu_usuario.html', usuario=usuario)
    else:
        return "Usuário não encontrado"

@app.route('/criar_anuncio', methods=['GET', 'POST'])
def criar_anuncio():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        categoria_id = int(request.form['categoria_id'])
        proprietario_id = int(request.form['proprietario_id'])
        
        categoria = None
        for cat in categorias:
            if cat.id == categoria_id:
                categoria = cat
                break
        
        proprietario = None
        for user in usuarios:
            if user.id == proprietario_id:
                proprietario = user
                break
        
        if categoria and proprietario:
            novo_anuncio = Anuncio(id=len(anuncios) + 1, titulo=titulo, descricao=descricao, preco=preco, categoria=categoria, proprietario=proprietario)
            anuncios.append(novo_anuncio)
            return "Anúncio criado com sucesso!"
        else:
            return "Categoria ou proprietário não encontrado"
    
    categorias_disponiveis = categorias  # Passar a lista de categorias para o template
    usuarios_disponiveis = usuarios  # Passar a lista de usuários para o template
    return render_template('criar_anuncio.html', categorias=categorias_disponiveis, usuarios=usuarios_disponiveis)

@app.route('/visualizar_anuncio/<int:anuncio_id>')
def visualizar_anuncio(anuncio_id):
    anuncio = None
    for ad in anuncios:
        if ad.id == anuncio_id:
            anuncio = ad
            break
    
    if anuncio:
        return render_template('visualizar_anuncio.html', anuncio=anuncio)
    else:
        return "Anúncio não encontrado"

@app.route('/editar_anuncio/<int:anuncio_id>', methods=['GET', 'POST'])
def editar_anuncio(anuncio_id):
    anuncio = None
    for ad in anuncios:
        if ad.id == anuncio_id:
            anuncio = ad
            break
    
    if request.method == 'POST':
        anuncio.titulo = request.form['titulo']
        anuncio.descricao = request.form['descricao']
        anuncio.preco = float(request.form['preco'])
        anuncio.categoria.id = int(request.form['categoria_id'])
        
        return redirect(url_for('visualizar_anuncio', anuncio_id=anuncio.id))
    
    if anuncio:
        categorias_disponiveis = categorias  # Passar a lista de categorias para o template
        return render_template('editar_anuncio.html', anuncio=anuncio, categorias=categorias_disponiveis)
    else:
        return "Anúncio não encontrado"

@app.route('/excluir_anuncio/<int:anuncio_id>', methods=['POST'])
def excluir_anuncio(anuncio_id):
    anuncio = None
    for ad in anuncios:
        if ad.id == anuncio_id:
            anuncio = ad
            break
    
    if anuncio:
        anuncios.remove(anuncio)
        return redirect(url_for('menu_usuario', usuario_id=anuncio.proprietario.id))
    else:
        return "Anúncio não encontrado"

@app.route('/procurar_anuncios/<int:usuario_id>')
def procurar_anuncios(usuario_id):
    usuario = None
    for user in usuarios:
        if user.id == usuario_id:
            usuario = user
            break
    
    if usuario:
        anuncios_simulados = [
            Anuncio(id=1, titulo='Celular', descricao='Smartphone novo', preco=1000.00, data_criacao='2023-08-10', categoria='Eletrônicos', proprietario='Usuário 1'),
            Anuncio(id=2, titulo='Livro', descricao='Livro de ficção', preco=20.00, data_criacao='2023-08-11', categoria='Livros', proprietario='Usuário 2'),
            
        ]
    
        return render_template('procurar_anuncios.html', usuario=usuario, anuncios=anuncios_simulados)
    else:
        return "Usuário não encontrado"

@app.route('/ver_minhas_compras/<int:usuario_id>')
def ver_minhas_compras(usuario_id):
    usuario = None
    for user in usuarios:
        if user.id == usuario_id:
            usuario = user
            break
    
    if usuario:
        # Simulação de compras
        compras_simuladas = [
            {'produto': 'Smartphone', 'preco': 1000.00, 'data': '2023-08-12'},
            {'produto': 'Livro', 'preco': 20.00, 'data': '2023-08-13'},
        ]
    
        return render_template('ver_minhas_compras.html', usuario=usuario, compras=compras_simuladas)
    else:
        return "Usuário não encontrado"


@app.route('/ver_minhas_vendas')
def ver_minhas_vendas():
    vendas_simuladas = [
        {'produto': 'Smartphone', 'preco': 1000.00, 'data': '2023-08-12'},
        {'produto': 'Livro', 'preco': 20.00, 'data': '2023-08-13'},
        
    ]
    
    return render_template('ver_minhas_vendas.html', vendas=vendas_simuladas)

@app.route('/minhas_perguntas')
def minhas_perguntas():
    perguntas_simuladas = [
        {'produto': 'Smartphone', 'pergunta': 'O smartphone é desbloqueado?', 'resposta': 'Sim, o smartphone é desbloqueado.'},
        {'produto': 'Livro', 'pergunta': 'Esse livro tem versão em inglês?', 'resposta': 'Sim, o livro também está disponível em inglês.'},
        
    ]
    
    return render_template('minhas_perguntas.html', perguntas=perguntas_simuladas)

@app.route('/lista_favoritos')
def lista_favoritos():
    favoritos_simulados = [
        {'produto': 'Smartphone', 'preco': 1000.00, 'proprietario': 'Usuário 1'},
        {'produto': 'Livro', 'preco': 20.00, 'proprietario': 'Usuário 2'},
        
    ]
    
    return render_template('lista_favoritos.html', favoritos=favoritos_simulados)

@app.route('/criar_categoria', methods=['GET', 'POST'])
def criar_categoria():
    if request.method == 'POST':
        nome_categoria = request.form['nome_categoria']
        nova_categoria = Categoria(id=len(categorias) + 1, nome=nome_categoria)
        categorias.append(nova_categoria)
        return redirect(url_for('menu_usuario', usuario_id=nova_categoria.proprietario.id))
    return render_template('criar_categoria.html')

@app.route('/editar_categoria/<int:categoria_id>', methods=['GET', 'POST'])
def editar_categoria(categoria_id):
    categoria = None
    for cat in categorias:
        if cat.id == categoria_id:
            categoria = cat
            break
    
    if request.method == 'POST':
        categoria.nome = request.form['nome_categoria']
        
        return redirect(url_for('menu_usuario', usuario_id=categoria.proprietario.id))
    
    if categoria:
        return render_template('editar_categoria.html', categoria=categoria)
    else:
        return "Categoria não encontrada"

@app.route('/excluir_categoria/<int:categoria_id>', methods=['POST'])
def excluir_categoria(categoria_id):
    categoria = None
    for cat in categorias:
        if cat.id == categoria_id:
            categoria = cat
            break
    
    if categoria:
        categorias.remove(categoria)
        return redirect(url_for('menu_usuario', usuario_id=categoria.proprietario.id))
    else:
        return "Categoria não encontrada"

@app.route('/voltar_menu')
def voltar_menu():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
