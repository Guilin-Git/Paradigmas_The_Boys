import tkinter as tk
from tkinter import messagebox
import database

def show_add_hero():
    clear_entries()
    add_frame.pack(fill="both", expand=True)
    remove_frame.pack_forget()
    update_frame.pack_forget()
    search_frame.pack_forget()

def show_remove_hero():
    clear_entries()
    add_frame.pack_forget()
    remove_frame.pack(fill="both", expand=True)
    update_frame.pack_forget()
    search_frame.pack_forget()

def show_update_hero():
    clear_entries()
    add_frame.pack_forget()
    remove_frame.pack_forget()
    update_frame.pack(fill="both", expand=True)
    search_frame.pack_forget()

def show_search_hero():
    clear_entries()
    add_frame.pack_forget()
    remove_frame.pack_forget()
    update_frame.pack_forget()
    search_frame.pack(fill="both", expand=True)

# Funções de CRUD
def add_hero():
    data = (
        real_name_entry.get(), hero_name_entry.get(), gender_entry.get(),
        float(height_entry.get()), float(weight_entry.get()),
        birth_date_entry.get(), birth_place_entry.get(), powers_entry.get(),
        int(strength_level_entry.get()), int(popularity_entry.get()),
        status_entry.get(), battle_history_entry.get()
    )
    database.add_hero(data)
    messagebox.showinfo("Sucesso", "Herói adicionado com sucesso!")
    clear_entries()

def remove_hero():
    hero_id = int(id_entry.get())
    database.remove_hero(hero_id)
    messagebox.showinfo("Sucesso", "Herói removido com sucesso!")
    clear_entries()

def update_hero():
    hero_id = int(id_entry.get())
    data = (
        real_name_entry.get(), hero_name_entry.get(), gender_entry.get(),
        float(height_entry.get()), float(weight_entry.get()),
        birth_date_entry.get(), birth_place_entry.get(), powers_entry.get(),
        int(strength_level_entry.get()), int(popularity_entry.get()),
        status_entry.get(), battle_history_entry.get()
    )
    database.update_hero(hero_id, data)
    messagebox.showinfo("Sucesso", "Herói atualizado com sucesso!")
    clear_entries()

def search_hero():
    name = search_name_entry.get()
    status = search_status_entry.get()
    popularity = search_popularity_entry.get()
    popularity = int(popularity) if popularity else None
    
    results = database.search_heroes(name=name, status=status, popularity=popularity)
    display_results(results)

def display_results(results):
    for widget in results_frame.winfo_children():
        widget.destroy()
    for hero in results:
        result_label = tk.Label(results_frame, text=str(hero))
        result_label.pack()

def clear_entries():
    for entry in [real_name_entry, hero_name_entry, gender_entry, height_entry, 
                  weight_entry, birth_date_entry, birth_place_entry, powers_entry, 
                  strength_level_entry, popularity_entry, status_entry, battle_history_entry]:
        entry.delete(0, tk.END)

# Configuração da janela principal
root = tk.Tk()
root.title("Banco de Dados de Heróis")

# Botões principais para acessar funções
main_button_frame = tk.Frame(root)
main_button_frame.pack()

add_button = tk.Button(main_button_frame, text="Adicionar Herói", command=show_add_hero)
add_button.pack(side="left")

remove_button = tk.Button(main_button_frame, text="Remover Herói", command=show_remove_hero)
remove_button.pack(side="left")

update_button = tk.Button(main_button_frame, text="Atualizar Herói", command=show_update_hero)
update_button.pack(side="left")

search_button = tk.Button(main_button_frame, text="Buscar Herói", command=show_search_hero)
search_button.pack(side="left")

# Frames de entrada para cada operação
add_frame = tk.Frame(root)
remove_frame = tk.Frame(root)
update_frame = tk.Frame(root)
search_frame = tk.Frame(root)

# Adicionar campos de entrada para "Adicionar Herói"
real_name_label = tk.Label(add_frame, text="Nome Real:")
real_name_label.pack()
real_name_entry = tk.Entry(add_frame)
real_name_entry.pack()

hero_name_label = tk.Label(add_frame, text="Nome do Herói:")
hero_name_label.pack()
hero_name_entry = tk.Entry(add_frame)
hero_name_entry.pack()

gender_label = tk.Label(add_frame, text="Sexo:")
gender_label.pack()
gender_entry = tk.Entry(add_frame)
gender_entry.pack()

height_label = tk.Label(add_frame, text="Altura:")
height_label.pack()
height_entry = tk.Entry(add_frame)
height_entry.pack()

weight_label = tk.Label(add_frame, text="Peso:")
weight_label.pack()
weight_entry = tk.Entry(add_frame)
weight_entry.pack()

birth_date_label = tk.Label(add_frame, text="Data de Nascimento:")
birth_date_label.pack()
birth_date_entry = tk.Entry(add_frame)
birth_date_entry.pack()

birth_place_label = tk.Label(add_frame, text="Local de Nascimento:")
birth_place_label.pack()
birth_place_entry = tk.Entry(add_frame)
birth_place_entry.pack()

powers_label = tk.Label(add_frame, text="Poderes:")
powers_label.pack()
powers_entry = tk.Entry(add_frame)
powers_entry.pack()

strength_level_label = tk.Label(add_frame, text="Nível de Força:")
strength_level_label.pack()
strength_level_entry = tk.Entry(add_frame)
strength_level_entry.pack()

popularity_label = tk.Label(add_frame, text="Popularidade:")
popularity_label.pack()
popularity_entry = tk.Entry(add_frame)
popularity_entry.pack()

status_label = tk.Label(add_frame, text="Status:")
status_label.pack()
status_entry = tk.Entry(add_frame)
status_entry.pack()

battle_history_label = tk.Label(add_frame, text="Histórico de Batalhas:")
battle_history_label.pack()
battle_history_entry = tk.Entry(add_frame)
battle_history_entry.pack()

add_hero_button = tk.Button(add_frame, text="Adicionar", command=add_hero)
add_hero_button.pack()

# Campos de entrada para "Remover Herói"
id_label = tk.Label(remove_frame, text="ID (para remover):")
id_label.pack()
id_entry = tk.Entry(remove_frame)
id_entry.pack()

remove_hero_button = tk.Button(remove_frame, text="Remover", command=remove_hero)
remove_hero_button.pack()

# Campos de entrada para "Atualizar Herói"
id_label_update = tk.Label(update_frame, text="ID (para atualizar):")
id_label_update.pack()
id_entry_update = tk.Entry(update_frame)
id_entry_update.pack()

# Repetir os campos de entrada do 'add_frame' para atualização
# (pode reutilizar os campos de entrada de 'add_frame' ou criar campos específicos)

update_hero_button = tk.Button(update_frame, text="Atualizar", command=update_hero)
update_hero_button.pack()

# Campos de entrada para "Buscar Herói"
search_name_label = tk.Label(search_frame, text="Buscar por Nome:")
search_name_label.pack()
search_name_entry = tk.Entry(search_frame)
search_name_entry.pack()

search_status_label = tk.Label(search_frame, text="Buscar por Status:")
search_status_label.pack()
search_status_entry = tk.Entry(search_frame)
search_status_entry.pack()

search_popularity_label = tk.Label(search_frame, text="Buscar por Popularidade Mínima:")
search_popularity_label.pack()
search_popularity_entry = tk.Entry(search_frame)
search_popularity_entry.pack()

search_button = tk.Button(search_frame, text="Buscar", command=search_hero)
search_button.pack()

# Frame para exibir resultados de busca
results_frame = tk.Frame(search_frame)
results_frame.pack()

root.mainloop()
