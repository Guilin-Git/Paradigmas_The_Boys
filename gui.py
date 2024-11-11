import dearpygui.dearpygui as dpg
from database import add_hero, remove_hero, update_hero, search_heroes, get_hero_by_id, add_crime, search_crimes, add_mission
import os
import sqlite3
import random


# Função para rolar o dado
def roll_dice():
    return random.randint(1, 10)


# Configuração de cor e estilo personalizada
def setup_theme():
    with dpg.theme(tag="custom_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 25), category=dpg.mvThemeCat_Core)  # Fundo da janela
            dpg.add_theme_color(dpg.mvThemeCol_Button, (150, 0, 0), category=dpg.mvThemeCat_Core)  # Botões em vermelho
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220), category=dpg.mvThemeCat_Core)  # Texto em branco
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40), category=dpg.mvThemeCat_Core)  # Campos de entrada

def open_add_hero_window():
    if dpg.does_item_exist("add_hero_window"):
        dpg.focus_item("add_hero_window")
    else:
        with dpg.window(label="Add Hero", modal=True, tag="add_hero_window"):
            dpg.add_input_text(label="Real Name", tag="real_name")
            dpg.add_input_text(label="Hero Name", tag="hero_name")
            dpg.add_input_text(label="Gender", tag="gender")
            dpg.add_input_float(label="Height", tag="height", format="%.2f")
            dpg.add_input_float(label="Weight", tag="weight", format="%.2f")
            dpg.add_input_text(label="Birth Date (dd/mm/yyyy)", tag="birth_date")
            dpg.add_input_text(label="Birth Place", tag="birth_place")
            dpg.add_input_text(label="Powers", tag="powers")
            dpg.add_input_int(label="Strength Level (0-100)", tag="strength_level")
            dpg.add_input_int(label="Popularity (0-100)", tag="popularity")
            dpg.add_input_text(label="Battle History", tag="battle_history")
            dpg.add_button(label="Add Hero", callback=add_hero_callback)

def add_hero_callback(sender, app_data, user_data):
    hero_data = [
        dpg.get_value("real_name"),
        dpg.get_value("hero_name"),
        dpg.get_value("gender"),
        dpg.get_value("height"),
        dpg.get_value("weight"),
        dpg.get_value("birth_date"),
        dpg.get_value("birth_place"),
        dpg.get_value("powers"),
        dpg.get_value("strength_level"),
        dpg.get_value("popularity"),
        "Ativo",  # Status inicial como "Ativo"
        dpg.get_value("battle_history")
    ]

    # Adiciona o herói ao banco de dados
    add_hero(hero_data)

    # Fecha a janela de adição e exibe feedback
    dpg.delete_item("add_hero_window")
    dpg.set_value("status_text", f"Herói '{hero_data[1]}' adicionado com sucesso.")

# Função para abrir janela de busca de herói
def open_search_window():
    if dpg.does_item_exist("search_hero_window"):
        dpg.focus_item("search_hero_window")
    else:
        with dpg.window(label="Search Hero", modal=True, tag="search_hero_window"):
            dpg.add_input_text(label="Hero Name", tag="search_name")
            dpg.add_button(label="Search", callback=search_hero_callback)
            with dpg.group(tag="search_results"):
                pass


def search_hero_callback(sender, app_data, user_data):
    name = dpg.get_value("search_name")  # Nome do herói para busca
    results = search_heroes(name=name)

    # Limpa os resultados de pesquisa anteriores, se houver
    if dpg.does_item_exist("search_results"):
        dpg.delete_item("search_results", children_only=True)

    # Exibe os resultados da pesquisa
    with dpg.group(parent="search_results"):
        for hero in results:
            dpg.add_text(f"Herói: {hero[2]}, Popularidade: {hero[10]}, Status: {hero[11]}")

    # Atualiza a mensagem de status
    dpg.set_value("status_text", f"{len(results)} resultado(s) encontrado(s) para '{name}'.")

# Função para abrir janela de atualização de herói
def open_update_hero_window():
    if dpg.does_item_exist("update_hero_window"):
        dpg.focus_item("update_hero_window")
    else:
        with dpg.window(label="Update Hero", modal=True, tag="update_hero_window"):
            dpg.add_input_int(label="Hero ID", tag="update_hero_id", callback=lambda: load_hero_data(dpg.get_value("update_hero_id")))
            dpg.add_input_text(label="Real Name", tag="update_real_name")
            dpg.add_input_text(label="Hero Name", tag="update_hero_name")
            dpg.add_input_text(label="Gender", tag="update_gender")
            dpg.add_input_float(label="Height", tag="update_height", format="%.2f")
            dpg.add_input_float(label="Weight", tag="update_weight", format="%.2f")
            dpg.add_input_text(label="Birth Date (dd/mm/yyyy)", tag="birth_date")
            dpg.add_input_text(label="Birth Place", tag="update_birth_place")
            dpg.add_input_text(label="Powers", tag="update_powers")
            dpg.add_input_int(label="Strength Level (0-100)", tag="update_strength_level")
            dpg.add_input_int(label="Popularity (0-100)", tag="update_popularity")
            dpg.add_input_text(label="Battle History", tag="update_battle_history")
            dpg.add_button(label="Update Hero", callback=update_hero_callback)


def update_hero_callback(sender, app_data, user_data):
    hero_id = dpg.get_value("update_hero_id")  # ID do herói a ser atualizado
    updated_data = [
        dpg.get_value("update_real_name"),
        dpg.get_value("update_hero_name"),
        dpg.get_value("update_gender"),
        dpg.get_value("update_height"),
        dpg.get_value("update_weight"),
        dpg.get_value("update_birth_date"),
        dpg.get_value("update_birth_place"),
        dpg.get_value("update_powers"),
        dpg.get_value("update_strength_level"),
        dpg.get_value("update_popularity"),
        dpg.get_value("update_status"),
        dpg.get_value("update_battle_history")
    ]

    # Atualiza o herói no banco de dados
    update_hero(hero_id, updated_data)

    # Fecha a janela de atualização e exibe feedback
    dpg.delete_item("update_hero_window")
    dpg.set_value("status_text", f"Herói com ID {hero_id} atualizado com sucesso.")


def open_remove_hero_window():
    if dpg.does_item_exist("remove_hero_window"):
        dpg.focus_item("remove_hero_window")
    else:
        with dpg.window(label="Remove Hero", modal=True, tag="remove_hero_window"):
            dpg.add_input_int(label="Hero ID", tag="remove_hero_id")
            dpg.add_button(label="Remove Hero", callback=remove_hero_callback)


# Função de callback para remover o herói
def remove_hero_callback(sender, app_data, user_data):
    hero_id = dpg.get_value("remove_hero_id")

    # Remove o herói do banco de dados pelo ID
    remove_hero(hero_id)

    # Fecha a janela de remoção e exibe feedback
    dpg.delete_item("remove_hero_window")
    dpg.set_value("status_text", f"Herói com ID {hero_id} removido com sucesso.")

# Função para abrir janela para adicionar crime
def open_add_crime_window():
    if dpg.does_item_exist("add_crime_window"):
        dpg.focus_item("add_crime_window")
    else:
        with dpg.window(label="Add Crime", modal=True, tag="add_crime_window"):
            dpg.add_input_int(label="Hero ID", tag="crime_hero_id")
            dpg.add_input_text(label="Hero Name", tag="crime_hero_name")
            dpg.add_input_text(label="Crime Name", tag="crime_name")
            dpg.add_input_text(label="Crime Description", tag="crime_description")
            dpg.add_input_text(label="Crime Date (dd/mm/yyyy)", tag="crime_date")
            dpg.add_input_text(label="Crime Severity", tag="crime_severity")
            dpg.add_button(label="Add Crime", callback=submit_crime_callback)

# Função para abrir janela para adicionar missão
def open_add_mission_window():
    if dpg.does_item_exist("add_mission_window"):
        dpg.focus_item("add_mission_window")
    else:
        with dpg.window(label="Add Mission", modal=True, tag="add_mission_window"):
            dpg.add_input_text(label="Mission Name", tag="mission_name")
            dpg.add_input_text(label="Mission Description", tag="mission_description")
            dpg.add_input_int(label="Difficulty Level (1-10)", tag="difficulty_level")
            dpg.add_input_int(label="Hero ID", tag="hero_id_mission")
            dpg.add_button(label="Add Mission", callback=submit_mission_callback)

# Função para carregar a imagem de fundo
def add_background_image():
    try:
        # Obter o caminho absoluto para a imagem
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_directory, "theboys_background.png")

        # Verificar se o arquivo existe
        if not os.path.exists(image_path):
            print(f"Imagem não encontrada no caminho: {image_path}. Continuando sem a imagem de fundo.")
        else:
            # Carregar a imagem
            width, height, channels, data = dpg.load_image(image_path)

            # Adicionar a imagem como textura
            with dpg.texture_registry():
                dpg.add_static_texture(width, height, data, tag="background_image")

        # Criar a janela principal
        with dpg.window(label="Hero Database - The Boys", width=800, height=600, tag="main_window"):
            if os.path.exists(image_path):  # Apenas adicionar a imagem se ela estiver presente
                dpg.add_image("background_image")
            dpg.add_text("Hero Management System", color=(220, 220, 220))
            dpg.add_button(label="Add Hero", callback=open_add_hero_window)
            dpg.add_button(label="Search Hero", callback=open_search_window)
            dpg.add_button(label="Update Hero", callback=open_update_hero_window)
            dpg.add_button(label="Remove Hero", callback=open_remove_hero_window)
            dpg.add_button(label="Add Crime", callback=open_add_crime_window)
            dpg.add_button(label="Cometer Crime", callback=commit_crime_callback)
            dpg.add_button(label="Add Mission", callback=open_add_mission_window)
            dpg.add_button(label="Complete Mission", callback=complete_mission_callback)

            # Adicione o status_text dentro da janela principal
            dpg.add_text("", tag="status_text")
            dpg.bind_item_theme("main_window", "custom_theme")
    except TypeError:
        print("Erro: Imagem de fundo não pôde ser carregada. Verifique o caminho do arquivo.")

# Função para adicionar um crime
def submit_crime_callback(sender, app_data, user_data):
    crime_name = dpg.get_value("crime_name")
    crime_description = dpg.get_value("crime_description")
    crime_severity = dpg.get_value("crime_severity")
    hero_id = dpg.get_value("hero_id_crime")

    # Adicionar crime sem penalidade de popularidade
    add_crime((crime_name, crime_description, hero_id, "2024-11-10", "HeroName", crime_severity), hero_id)
    dpg.set_value("status_text", f"Crime '{crime_name}' adicionado sem penalidade.")


# Função para cometer um crime e aplicar penalidade
def commit_crime_callback(sender, app_data, user_data):
    hero_id = dpg.get_value("hero_id_crime")
    dice_roll = roll_dice()
    update_hero(hero_id, {"popularity": dice_roll * -1})
    dpg.set_value("status_text", f"Crime cometido! Popularidade do herói reduzida em {dice_roll} pontos.")


# Função para adicionar uma missão
def submit_mission_callback(sender, app_data, user_data):
    mission_name = dpg.get_value("mission_name")
    mission_description = dpg.get_value("mission_description")
    difficulty_level = dpg.get_value("difficulty_level")
    hero_id = dpg.get_value("hero_id_mission")

    # Adicionar missão sem ajuste de popularidade
    add_mission((mission_name, mission_description, difficulty_level, "Sucesso", 5), hero_id)
    dpg.set_value("status_text", f"Missão '{mission_name}' adicionada sem recompensa aplicada.")


# Função para completar uma missão e aplicar recompensa
# Função para completar uma missão e aplicar recompensa
def complete_mission_callback(sender, app_data, user_data):
    hero_id = dpg.get_value("hero_id_mission")
    dice_roll = roll_dice()
    update_hero(hero_id, {"popularity": dice_roll})
    dpg.set_value("status_text", f"Missão completada! Popularidade do herói aumentada em {dice_roll} pontos.")

# Função para carregar os dados do herói para atualização
def load_hero_data(hero_id):
    hero = get_hero_by_id(hero_id)
    if hero:
        dpg.set_value("update_real_name", hero[1])
        dpg.set_value("update_hero_name", hero[2])
        dpg.set_value("update_gender", hero[3])
        dpg.set_value("update_height", hero[4])
        dpg.set_value("update_weight", hero[5])
        dpg.set_value("update_birth_date", hero[6])
        dpg.set_value("update_birth_place", hero[7])
        dpg.set_value("update_powers", hero[8])
        dpg.set_value("update_strength_level", hero[9])
        dpg.set_value("update_popularity", hero[10])
        dpg.set_value("update_status", hero[11])
        dpg.set_value("update_battle_history", hero[12])

# Configuração da interface principal
dpg.create_context()
setup_theme()
add_background_image()

# Janela principal com botões de funcionalidade
"""with dpg.window(label="Hero Management System", width=800, height=600, tag="main_window"):
    dpg.add_text("Hero Management System", color=(220, 220, 220))
    dpg.add_button(label="Add Hero", callback=open_add_hero_window)
    dpg.add_button(label="Search Hero", callback=open_search_window)
    dpg.add_button(label="Update Hero", callback=open_update_hero_window)
    dpg.add_button(label="Remove Hero", callback=open_remove_hero_window)
    dpg.add_button(label="Add Crime", callback=open_add_crime_window)
    dpg.add_button(label="Cometer Crime", callback=commit_crime_callback)
    dpg.add_button(label="Add Mission", callback=open_add_mission_window)
    dpg.add_button(label="Complete Mission", callback=complete_mission_callback)"""

# Exibir status de operações
"""dpg.add_text("", tag="status_text")"""

# Iniciar a interface
dpg.create_viewport(title="Hero Database - The Boys", width=1000, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

