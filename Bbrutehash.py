#!/bin/python3
import crypt, os, hashlib

metodos = {"1":"MD5","5":"SHA-256","6":"SHA-512","y":"Yescrypt"}


print("="*50)
print("Bbrutehash".center(50))
print("="*50)

while True:
    
    print("Selecione um dos algoritimos abaixo:")
    for key, metodo in metodos.items():
        print(f"[{key}] - {metodo}")

    input_metodo = str(input(">>>"))
    if input_metodo in metodos.keys():
        print("="*50)
        print(f"O metodo selecionado foi: {metodos[input_metodo]}".center(50))
        print("="*50)
        if input_metodo == "y":
            print("Informe os parâmetros da hash")
            print("Exemplo: $<metodo>$<PARÂMENTROS>$<Salt>$<Hash>")
            input_parametros = str(input(">>>"))
        break
    else:
        print("="*70)
        print("Entrada inválida, por favor selecione um metodo valido.".center(70))
        print("="*70)

if input_metodo == "y":
    print("Informe o salt à ser utilizado.")
    print("Exemplo: $<metodo>$<PARÂMENTROS>$<Salt>$<Hash>")
    while True:
        input_salt = str(input(">>>")).strip()
        if input_salt:
            break      
        else:
            print("Salt OBRIGATÓRIO, para o metodo escolhido.")
else:
    print("Informe o salt à ser utilizado. (CASO NÃO SEJA INFORMADO, NÃO SERÁ UTILIZADO SALT)")
    print("Exemplo: $<metodo>$<Salt>$<Hash>")
    input_salt = str(input(">>>")).strip()
while True:
    input_hash = str(input("Informe a hash\n>>>"))
    if input_hash:
        break
    else:
        print("O campo hash não pode ser vazio.")

if input_salt:
    if input_metodo == "y":
        hash_alvo = f"${input_metodo}${input_parametros}${input_salt}${input_hash}"
    else:
        hash_alvo = f"${input_metodo}${input_salt}${input_hash}"
else:
    hash_alvo = input_hash

local_path = os.getcwd()
print(f"ATENÇÃO: A wordlist deve estar localizada na pasta: {local_path}")
print("Informe o nome da wordlist contendo a extensão.")
print("EXEMPLO: wordlist.txt")
wordlist = str(input(">>> "))

with open(wordlist, "r", encoding="utf-8") as wl:
    for senha in wl:
        senha = senha.strip()
        if input_salt:
            if input_metodo == "y":
                hash_senha = crypt.crypt(senha,f"${input_metodo}${input_parametros}${input_salt}$")
            else:
                hash_senha = crypt.crypt(senha,f"${input_metodo}${input_salt}$")
            
            if hash_alvo == hash_senha:
                print(f"Senha encontrada: {senha}")
                break
            else:
                print(f"Testado: {senha}")

        else:
            if input_metodo == "1":
                hash_senha = hashlib.md5(senha.encode('UTF-8'))
                if hash_alvo == hash_senha.hexdigest():
                    print(f"Senha encontrada: {senha}")
                    break
                else:
                    print(f"Testado: {senha}")
            elif input_metodo == "5":
                hash_senha = hashlib.sha256(senha.encode('UTF-8'))
                if hash_alvo == hash_senha.hexdigest():
                    print(f"Senha encontrada: {senha}")
                    break
                else:
                    print(f"Testado: {senha}")
            elif input_metodo == "6":
                hash_senha = hashlib.sha512(senha.encode('UTF-8'))
                if hash_alvo == hash_senha.hexdigest():
                    print(f"Senha encontrada: {senha}")
                    break
                else:
                    print(f"Testado: {senha}")
