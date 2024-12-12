import os
import shutil
import xml.etree.ElementTree as ET

def process_xml_files(source_folder, target_folder_equal, target_folder_different, tag_name, target_value, namespaces):
    # Certifique-se de que as pastas de destino existam
    os.makedirs(target_folder_equal, exist_ok=True)
    os.makedirs(target_folder_different, exist_ok=True)

    # Iterar por cada arquivo XML na pasta de origem
    for filename in os.listdir(source_folder):
        if filename.endswith('.xml'):
            file_path = os.path.join(source_folder, filename)
            try:
                # Parse o arquivo XML
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Depuração: Exibir as tags e namespaces encontrados
                print(f"Processando arquivo: {filename}")

                # Buscar todas as ocorrências da tag <ItemListaServico>
                item_tags = root.findall(f".//ns2:{tag_name}", namespaces)
                if item_tags:
                    for tag in item_tags:
                        print(f"Tag encontrada: {tag.tag} com valor {tag.text}")
                        if tag.text == target_value:
                            # Mover o arquivo para a pasta correspondente
                            shutil.move(file_path, os.path.join(target_folder_equal, filename))
                            break
                        elif tag is not None and tag.text != target_value:
                            # Caso nenhuma tag corresponda ao valor
                            shutil.move(file_path, os.path.join(target_folder_different, filename))
                else:
                    print(f"Tag {tag_name} não encontrada no arquivo {filename}")
                    shutil.move(file_path, os.path.join(target_folder_different, filename))
            except ET.ParseError:
                print(f"Erro ao parsear o arquivo XML: {filename}. Certifique-se de que o arquivo seja válido.")
            except Exception as e:
                print(f"Erro ao processar arquivo {filename}: {e}")

# Parâmetros do script
source_folder = r''
target_folder_equal = r''
target_folder_different = r''
tag_name = 'ItemListaServico'
target_value = '14.05'
namespaces = {
    'ns1': 'http://nfe.sjp.pr.gov.br/servico_consultar_nfse_resposta_v03.xsd',
    'ns2': 'http://nfe.sjp.pr.gov.br/tipos_v03.xsd',  # Defina aqui os namespaces conforme necessário
    'ns3': 'http://www.w3.org/2000/09/xmldsig#',
}

# Executar a função
process_xml_files(source_folder, target_folder_equal, target_folder_different, tag_name, target_value, namespaces)
