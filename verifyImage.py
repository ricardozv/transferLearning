import os
from PIL import Image

def verificar_e_excluir_imagens(diretorio):
    for subdir, dirs, files in os.walk(diretorio):
        for file in files:
            filepath = os.path.join(subdir, file)
            try:
                with Image.open(filepath) as img:
                    img.verify()  # Verifica se a imagem está corrompida
            except (IOError, SyntaxError) as e:
                print(f'Imagem corrompida/removida: {filepath}')
                os.remove(filepath)

    print("Análise de imagens concluída. Todas as imagens corrompidas foram removidas.")

# Define o diretório raiz para verificar as imagens
diretorio_raiz = 'images'

verificar_e_excluir_imagens(diretorio_raiz)
