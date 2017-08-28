import re
import os
import sys
import codecs
import shutil
import string
import argparse
import subprocess

# Mátodo que altera a variável
def changeVar(line, params):
    # Variáveis a serem alteradas
    keys = params.keys();
    for key in keys:
        if key in line:
            #line = re.sub(key, params[key], line)
            line = line.replace(key, params[key])
    return line

# Método que altera os valores nos arquivos
def changeValues(filename, params):
    # Ler o arquivo
    with codecs.open(filename, "r", "utf-8") as f:
        lines = (line.rstrip() for line in f)
        # Alterar o arquivo
        newlines = [ changeVar(line, params) if not re.match("(.*?)[\{\{\}\}](.*?)+", line) == None else line for line in lines]
    # Abrir o arquivo
    file = open(filename)
    #Salvar o arquivo
    with codecs.open(filename, "w", "utf-8") as f:
        f.write('\n'.join(newlines) + '\n')
# Projeto a ser clonado
parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="Diretório onde o projeto será iniciado!")
parser.add_argument("project", help="Node para NodeJS, Cordova para Cordova!")
args = parser.parse_args()
project = args.project.lower()[:3]
# Repositório a ser clonado
repo = None
if project == 'cor':
    repo = "https://github.com/r2ttecnologia/CordovaTemplate.git"
    pass
elif project == 'nod':
    repo = "https://github.com/r2ttecnologia/NodeApiSample.git"
    pass
else:
    print("Parâmetro inválido!")
    sys.exit(-1)

# Lê o nome da pasta onde será criado o template
if args.dir:
    dirpath = args.dir
else:
    dirpath = input("Digite o local do diretório onde será criado o projeto: ")
# Retira aspas
dirpath = dirpath.replace("\"", "")
# Nome do projeto
projectname = input("Nome do projeto: ")
projectname = projectname.replace("-", "")
projectname = projectname.replace(" ", "")
# Descrição do projeto
projectdesc = input("Descrição do projeto: ")
# Repó do projeto
projectrepo = input("Repositório: ")
# Parâmetros a serem modificados nos arquivos
params = {}
params["{{title}}"] = projectname.lower()
params["{{description}}"] = projectdesc
params["{{repo_url}}"] = projectrepo
# Caminho do projeto
projectpath = os.path.join(dirpath, projectname)
# Corrige o caminho
dirpath = os.path.normpath(dirpath)
# Verifica se o diretório informado existe
if os.path.exists(dirpath):
    if(os.path.exists(projectpath)):
        print("Diretório do projeto já existe!")
    else:
        os.mkdir(projectpath)
        print("Clonando " + repo + " em " + projectpath)
        subprocess.check_call("git clone " + repo + " \"" + projectpath + "\"", shell=True)
        # Vai para a pasta do projeto
        os.chdir(projectpath)
        # Apaga os objetos de .git
        for dpath, dname, fname in os.walk('.git'):
            for filename in fname:
                p = os.path.join(dpath, filename)
                os.chmod(p, 0o777) # for example
                os.remove(p)
        # Remover a pasta .git
        shutil.rmtree('.git')
        # Alterar os valores dos arquivos
        for dpath, dname, fname in os.walk('.'):
            for filename in fname:
                f = os.path.join(dpath, filename)
                if filename == '.delme':
                    os.remove(f)
                else:
                    changeValues(f, params)
        # Instalar os módulos
        os.chdir(os.path.join(projectpath, 'source'))
        subprocess.check_call("npm install", shell=True)
else:
    print("O diretório informado não existe! Saindo ...")

