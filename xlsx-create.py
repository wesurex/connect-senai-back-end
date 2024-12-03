import pandas as pd
import random
import string
import bcrypt

# Função para gerar uma senha aleatória de 6 caracteres (letras e números)
def gerar_senha(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

# Função para criptografar a senha
def criptografar_senha(senha):
    senha_bytes = senha.encode('utf-8')  # Converter para bytes
    salt = bcrypt.gensalt()             # Gerar um salt
    senha_hash = bcrypt.hashpw(senha_bytes, salt)
    return senha_hash.decode('utf-8')   # Retornar o hash como string

# Processar a planilha e gerar o dicionário
def processar_planilha(caminho_arquivo):
    try:
        # Ler os dados da planilha
        df = pd.read_excel(caminho_arquivo)
        
        # Validar se as colunas necessárias existem
        colunas_necessarias = ['nome', 'email', 'ativo']
        if not all(col in df.columns for col in colunas_necessarias):
            raise ValueError(f"A planilha deve conter as colunas: {', '.join(colunas_necessarias)}")
        
        # Criar o dicionário para armazenar os usuários
        usuarios = []
        
        # Iterar pelas linhas do DataFrame
        for _, row in df.iterrows():
            nome = row['nome']
            email = row['email']
            ativo = row['ativo']
            
            # Gerar e criptografar a senha
            senha = gerar_senha()
            senha_criptografada = criptografar_senha(senha)
            
            # Adicionar ao dicionário
            usuarios.append({
                'nome': nome,
                'email': email,
                'ativo': ativo,
                'senha': senha_criptografada
            })
        
        print("Usuários processados com sucesso:")
        for usuario in usuarios:
            print(usuario)  # Exibe cada usuário no console
        
        return usuarios
    except Exception as e:
        print(f"Erro ao processar a planilha: {e}")
        return []

# Caminho para o arquivo .xlsx
caminho_arquivo = "usuarios.xlsx"  # Substitua pelo caminho do seu arquivo

# Processar a planilha
usuarios = processar_planilha(caminho_arquivo)
