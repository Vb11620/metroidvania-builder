import xml.etree.ElementTree as Et

from miscellaneous_dep import *


def get_element_by_name_forced(
    element_root: Et.Element, element_name: str, file: Et.ElementTree, file_path: str
):
    element = element_root.find(element_name)
    if element is None:
        # création de l'élement si'l n'existe pas
        Et.SubElement(element_root, element_name)
        file.write(file_path)
        element = element_root.find(element_name)
        if element is not None:
            log(f'"<{element_name}>" créé avec succès')
        else:
            exit(
                f'{Fore.RED}>> Error: "<{element_name}>" can\'t be created, check the integrity of the file{Fore.RESET}'
            )

    return element
