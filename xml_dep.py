import xml.etree.ElementTree as Et

from miscellaneous_dep import *


def create_element(
    element_root: Et.Element, element_name: str, file: Et.ElementTree, file_path: str
):
    element = element_root.find(element_name)
    if element is None:
        # création de l'élement si'l n'existe pas
        Et.SubElement(element_root, element_name)
        file.write(file_path)
        element = element_root.find(element_name)
        if element is not None:
            log(f'"<{element_root.tag}>/<{element_name}>" créé avec succès')
        else:
            exit(
                f'{Fore.RED}>> Error: "<{element_name}>" can\'t be created, check the integrity of the file{Fore.RESET}'
            )
    else:
        minor_log(f'"<{element_root.tag}>/<{element_name}>" existe déjà')


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
            log(f'"<{element_root.tag}>/<{element_name}>" créé avec succès')
        else:
            exit(
                f'{Fore.RED}>> Error: "<{element_name}>" can\'t be created, check the integrity of the file{Fore.RESET}'
            )

    return element


def remove_element_by_name(
    element_root: Et.Element, element_name: str, file: Et.ElementTree, file_path: str
):
    element = element_root.find(element_name)
    if element is not None:
        element_root.remove(element)
        file.write(file_path)

    if element_root.find(element_name) is None:
        achievement_log(f'"<{element_root.tag}>/<{element_name}>" supprimé avec succès')
    else:
        exit(
            f'{Fore.RED}>> Error: "<{element_name}>" can\'t be deleted, check the integrity of the file{Fore.RESET}'
        )


def remove_elements_by_attribute(
    element_root: Et.Element,
    attribute_key: str,
    attribute_value: str,
    file: Et.ElementTree,
    file_path: str,
):
    for element in element_root:
        if element.get(attribute_key) == attribute_value:
            element_root.remove(element)

    file.write(file_path)

    deleted = True
    for element in element_root:
        if element.get(attribute_key) == attribute_value:
            deleted = False

    if deleted:
        achievement_log(
            f"'<{element_root.tag}>/<foos {attribute_key}=\"{attribute_value}\">' supprimés avec succès"
        )
    else:
        exit(
            f"{Fore.RED}>> Error: '<{element_root.tag}>/<foo {attribute_key}=\"{attribute_value}\">' can't be deleted, check the integrity of the file{Fore.RESET}"
        )
