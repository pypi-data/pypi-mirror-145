import random, string

def gs():
    print('Esse programa irá gerar uma senha aleatória, com letras maiúsculas, minúsculas, números e símbolos.')
    print('---------------------------------------------------------------------------------------------------')
    tamanho = int(input('Digite a quantidade de caracteres para a senha aleatória: '))

    chars = string.ascii_letters + string.digits + 'ç!@#$%&*-?'

    rnd = random.SystemRandom()

    result = f'Você escolheu uma senha com {tamanho} caracteres, e a senha gerada é: '

    print(result + ''.join((rnd.choice(chars) for i in range(tamanho))))



