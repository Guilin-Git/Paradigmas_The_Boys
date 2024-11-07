import database  # Certifique-se de que o banco de dados e as tabelas estejam criados
import gui       # Inicia a interface gráfica

# Executa a aplicação gráfica
if __name__ == "__main__":
    database.create_table()   # Cria a tabela de heróis, se não existir
    database.create_trigger() # Configura o trigger para o status de heróis
    gui.root.mainloop()       # Executa a interface gráfica
