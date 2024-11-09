import tkinter as tk
from tkinter import messagebox
import database

# Funções de exibição das telas
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

# Funções CRUD
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

# Função para carregar dados do herói para atualizar
def load_hero_for_update():
    hero_id = int(id_entry_update.get())
    hero_data = database.search_heroes(name=None, status=None, popularity=None)
    hero_data = next((hero for hero in hero_data if hero[0] == hero_id), None)
    
    if hero_data:
        real_name_entry_update.delete(0, tk.END)
        real_name_entry_update.insert(0, hero_data[1])
        
        hero_name_entry_update.delete(0, tk.END)
        hero_name_entry_update.insert(0, hero_data[2])

        gender_entry_update.delete(0, tk.END)
        gender_entry_update.insert(0, hero_data[3])

        height_entry_update.delete(0, tk.END)
        height_entry_update.insert(0, str(hero_data[4]))

        weight_entry_update.delete(0, tk.END)
        weight_entry_update.insert(0, str(hero_data[5]))

        birth_date_entry_update.delete(0, tk.END)
        birth_date_entry_update.insert(0, hero_data[6])

        birth_place_entry_update.delete(0, tk.END)
        birth_place_entry_update.insert(0, hero_data[7])

        powers_entry_update.delete(0, tk.END)
        powers_entry_update.insert(0, hero_data[8])

        strength_level_entry_update.delete(0, tk.END)
        strength_level_entry_update.insert(0, str(hero_data[9]))

        popularity_entry_update.delete(0, tk.END)
        popularity_entry_update.insert(0, str(hero_data[10]))

        status_entry_update.delete(0, tk.END)
        status_entry_update.insert(0, hero_data[11])

        battle_history_entry_update.delete(0, tk.END)
        battle_history_entry_update.insert(0, hero_data[12])
        
        messagebox.showinfo("Sucesso", "Dados do herói carregados para atualização.")
    else:
        messagebox.showwarning("Aviso", "Herói não encontrado com o ID especificado.")

def update_hero():
    try:
        hero_id = int(id_entry_update.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")
        return
    
    data = (
        real_name_entry_update.get(), hero_name_entry_update.get(), gender_entry_update.get(),
        float(height_entry_update.get()), float(weight_entry_update.get()),
        birth_date_entry_update.get(), birth_place_entry_update.get(), powers_entry_update.get(),
        int(strength_level_entry_update.get()), int(popularity_entry_update.get()),
        status_entry_update.get(), battle_history_entry_update.get()
    )
    
    database.update_hero(hero_id, data)
    messagebox.showinfo("Sucesso", "Herói atualizado com sucesso!")
    clear_update_entries()

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
        result_label = tk.Label(results_frame, text=str(hero), font=("Arial", 12), fg="#fff", bg="#2f2f2f")
        result_label.pack()

# Funções de limpeza
def clear_entries():
    for entry in [real_name_entry, hero_name_entry, gender_entry, height_entry, 
                  weight_entry, birth_date_entry, birth_place_entry, powers_entry, 
                  strength_level_entry, popularity_entry, status_entry, battle_history_entry]:
        entry.delete(0, tk.END)

def clear_update_entries():
    for entry in [id_entry_update, real_name_entry_update, hero_name_entry_update, gender_entry_update, 
                  height_entry_update, weight_entry_update, birth_date_entry_update, birth_place_entry_update, 
                  powers_entry_update, strength_level_entry_update, popularity_entry_update, 
                  status_entry_update, battle_history_entry_update]:
        entry.delete(0, tk.END)

# Configuração da janela principal
root = tk.Tk()
root.title("Banco de Dados de Heróis")
root.geometry("600x700")
root.config(bg="#1c1c1c")

# Botões principais para acessar funções
main_button_frame = tk.Frame(root, bg="#333")
main_button_frame.pack(fill="x", pady=10)

add_button = tk.Button(main_button_frame, text="Adicionar Herói", command=show_add_hero, font=("Arial", 14), bg="#555", fg="white")
add_button.pack(side="left", padx=10)

remove_button = tk.Button(main_button_frame, text="Remover Herói", command=show_remove_hero, font=("Arial", 14), bg="#555", fg="white")
remove_button.pack(side="left", padx=10)

update_button = tk.Button(main_button_frame, text="Atualizar Herói", command=show_update_hero, font=("Arial", 14), bg="#555", fg="white")
update_button.pack(side="left", padx=10)

search_button = tk.Button(main_button_frame, text="Pesquisar Heróis", command=show_search_hero, font=("Arial", 14), bg="#555", fg="white")
search_button.pack(side="left", padx=10)

# Frames das telas
add_frame = tk.Frame(root, bg="#1c1c1c")
remove_frame = tk.Frame(root, bg="#1c1c1c")
update_frame = tk.Frame(root, bg="#1c1c1c")
search_frame = tk.Frame(root, bg="#1c1c1c")

# Adicionar campos de entrada para "Adicionar Herói"
real_name_label = tk.Label(add_frame, text="Nome Real:", font=("Arial", 12), fg="white", bg="#1c1c1c")
real_name_label.pack()
real_name_entry = tk.Entry(add_frame, font=("Arial", 12))
real_name_entry.pack()

hero_name_label = tk.Label(add_frame, text="Nome do Herói:", font=("Arial", 12), fg="white", bg="#1c1c1c")
hero_name_label.pack()
hero_name_entry = tk.Entry(add_frame, font=("Arial", 12))
hero_name_entry.pack()

gender_label = tk.Label(add_frame, text="Sexo:", font=("Arial", 12), fg="white", bg="#1c1c1c")
gender_label.pack()
gender_entry = tk.Entry(add_frame, font=("Arial", 12))
gender_entry.pack()

height_label = tk.Label(add_frame, text="Altura:", font=("Arial", 12), fg="white", bg="#1c1c1c")
height_label.pack()
height_entry = tk.Entry(add_frame, font=("Arial", 12))
height_entry.pack()

weight_label = tk.Label(add_frame, text="Peso:", font=("Arial", 12), fg="white", bg="#1c1c1c")
weight_label.pack()
weight_entry = tk.Entry(add_frame, font=("Arial", 12))
weight_entry.pack()

birth_date_label = tk.Label(add_frame, text="Data de Nascimento:", font=("Arial", 12), fg="white", bg="#1c1c1c")
birth_date_label.pack()
birth_date_entry = tk.Entry(add_frame, font=("Arial", 12))
birth_date_entry.pack()

birth_place_label = tk.Label(add_frame, text="Local de Nascimento:", font=("Arial", 12), fg="white", bg="#1c1c1c")
birth_place_label.pack()
birth_place_entry = tk.Entry(add_frame, font=("Arial", 12))
birth_place_entry.pack()

powers_label = tk.Label(add_frame, text="Poderes:", font=("Arial", 12), fg="white", bg="#1c1c1c")
powers_label.pack()
powers_entry = tk.Entry(add_frame, font=("Arial", 12))
powers_entry.pack()

strength_level_label = tk.Label(add_frame, text="Nível de Força:", font=("Arial", 12), fg="white", bg="#1c1c1c")
strength_level_label.pack()
strength_level_entry = tk.Entry(add_frame, font=("Arial", 12))
strength_level_entry.pack()

popularity_label = tk.Label(add_frame, text="Popularidade:", font=("Arial", 12), fg="white", bg="#1c1c1c")
popularity_label.pack()
popularity_entry = tk.Entry(add_frame, font=("Arial", 12))
popularity_entry.pack()

status_label = tk.Label(add_frame, text="Status:", font=("Arial", 12), fg="white", bg="#1c1c1c")
status_label.pack()
status_entry = tk.Entry(add_frame, font=("Arial", 12))
status_entry.pack()

battle_history_label = tk.Label(add_frame, text="Histórico de Batalhas:", font=("Arial", 12), fg="white", bg="#1c1c1c")
battle_history_label.pack()
battle_history_entry = tk.Entry(add_frame, font=("Arial", 12))
battle_history_entry.pack()

# Botão de Adicionar
add_button_frame = tk.Frame(add_frame, bg="#1c1c1c")
add_button_frame.pack(pady=10)
add_button = tk.Button(add_button_frame, text="Adicionar Herói", command=add_hero, font=("Arial", 12), bg="#007bff", fg="white")
add_button.pack()

# Remover Herói
id_label_remove = tk.Label(remove_frame, text="ID do Herói para Remover:", font=("Arial", 12), fg="white", bg="#1c1c1c")
id_label_remove.pack()
id_entry = tk.Entry(remove_frame, font=("Arial", 12))
id_entry.pack()

remove_button_frame = tk.Frame(remove_frame, bg="#1c1c1c")
remove_button_frame.pack(pady=10)
remove_button = tk.Button(remove_button_frame, text="Remover Herói", command=remove_hero, font=("Arial", 12), bg="#FF0000", fg="white")
remove_button.pack()

# Atualizar Herói
id_label_update = tk.Label(update_frame, text="ID do Herói para Atualizar:", font=("Arial", 12), fg="white", bg="#1c1c1c")
id_label_update.pack()
id_entry_update = tk.Entry(update_frame, font=("Arial", 12))
id_entry_update.pack()

# Campos para editar os dados do herói
real_name_label_update = tk.Label(update_frame, text="Nome Real:", font=("Arial", 12), fg="white", bg="#1c1c1c")
real_name_label_update.pack()
real_name_entry_update = tk.Entry(update_frame, font=("Arial", 12))
real_name_entry_update.pack()

hero_name_label_update = tk.Label(update_frame, text="Nome do Herói:", font=("Arial", 12), fg="white", bg="#1c1c1c")
hero_name_label_update.pack()
hero_name_entry_update = tk.Entry(update_frame, font=("Arial", 12))
hero_name_entry_update.pack()

gender_label_update = tk.Label(update_frame, text="Sexo:", font=("Arial", 12), fg="white", bg="#1c1c1c")
gender_label_update.pack()
gender_entry_update = tk.Entry(update_frame, font=("Arial", 12))
gender_entry_update.pack()

height_label_update = tk.Label(update_frame, text="Altura:", font=("Arial", 12), fg="white", bg="#1c1c1c")
height_label_update.pack()
height_entry_update = tk.Entry(update_frame, font=("Arial", 12))
height_entry_update.pack()

weight_label_update = tk.Label(update_frame, text="Peso:", font=("Arial", 12), fg="white", bg="#1c1c1c")
weight_label_update.pack()
weight_entry_update = tk.Entry(update_frame, font=("Arial", 12))
weight_entry_update.pack()

birth_date_label_update = tk.Label(update_frame, text="Data de Nascimento:", font=("Arial", 12), fg="white", bg="#1c1c1c")
birth_date_label_update.pack()
birth_date_entry_update = tk.Entry(update_frame, font=("Arial", 12))
birth_date_entry_update.pack()

birth_place_label_update = tk.Label(update_frame, text="Local de Nascimento:", font=("Arial", 12), fg="white", bg="#1c1c1c")
birth_place_label_update.pack()
birth_place_entry_update = tk.Entry(update_frame, font=("Arial", 12))
birth_place_entry_update.pack()

powers_label_update = tk.Label(update_frame, text="Poderes:", font=("Arial", 12), fg="white", bg="#1c1c1c")
powers_label_update.pack()
powers_entry_update = tk.Entry(update_frame, font=("Arial", 12))
powers_entry_update.pack()

strength_level_label_update = tk.Label(update_frame, text="Nível de Força:", font=("Arial", 12), fg="white", bg="#1c1c1c")
strength_level_label_update.pack()
strength_level_entry_update = tk.Entry(update_frame, font=("Arial", 12))
strength_level_entry_update.pack()

popularity_label_update = tk.Label(update_frame, text="Popularidade:", font=("Arial", 12), fg="white", bg="#1c1c1c")
popularity_label_update.pack()
popularity_entry_update = tk.Entry(update_frame, font=("Arial", 12))
popularity_entry_update.pack()

status_label_update = tk.Label(update_frame, text="Status:", font=("Arial", 12), fg="white", bg="#1c1c1c")
status_label_update.pack()
status_entry_update = tk.Entry(update_frame, font=("Arial", 12))
status_entry_update.pack()

battle_history_label_update = tk.Label(update_frame, text="Histórico de Batalhas:", font=("Arial", 12), fg="white", bg="#1c1c1c")
battle_history_label_update.pack()
battle_history_entry_update = tk.Entry(update_frame, font=("Arial", 12))
battle_history_entry_update.pack()

# Botão para carregar herói para atualização
load_button_frame = tk.Frame(update_frame, bg="#1c1c1c")
load_button_frame.pack(pady=10)
load_button = tk.Button(load_button_frame, text="Carregar Herói", command=load_hero_for_update, font=("Arial", 12), bg="#FF6600", fg="white")
load_button.pack()

# Botão para atualizar herói
update_button_frame = tk.Frame(update_frame, bg="#1c1c1c")
update_button_frame.pack(pady=10)
update_button = tk.Button(update_button_frame, text="Atualizar Herói", command=update_hero, font=("Arial", 12), bg="#FF0000", fg="white")
update_button.pack()

# Pesquisar Herói
search_name_label = tk.Label(search_frame, text="Nome do Herói:", font=("Arial", 12), fg="white", bg="#1c1c1c")
search_name_label.pack()
search_name_entry = tk.Entry(search_frame, font=("Arial", 12))
search_name_entry.pack()

search_status_label = tk.Label(search_frame, text="Status do Herói:", font=("Arial", 12), fg="white", bg="#1c1c1c")
search_status_label.pack()
search_status_entry = tk.Entry(search_frame, font=("Arial", 12))
search_status_entry.pack()

search_popularity_label = tk.Label(search_frame, text="Popularidade (número):", font=("Arial", 12), fg="white", bg="#1c1c1c")
search_popularity_label.pack()
search_popularity_entry = tk.Entry(search_frame, font=("Arial", 12))
search_popularity_entry.pack()

search_button_frame = tk.Frame(search_frame, bg="#1c1c1c")
search_button_frame.pack(pady=10)
search_button = tk.Button(search_button_frame, text="Pesquisar Herói", command=search_hero, font=("Arial", 12), bg="#007bff", fg="white")
search_button.pack()

# Frame para exibir resultados de pesquisa
results_frame = tk.Frame(search_frame, bg="#1c1c1c")
results_frame.pack(pady=20)


root.mainloop()
