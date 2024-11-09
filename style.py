import tkinter as tk
from tkinter import ttk

def apply_the_boys_theme(root):
    style = ttk.Style()

    # Configuração de estilo do tema
    style.configure('TFrame', background='#333333')
    style.configure('TButton', background='#FF0000', foreground='#FFFFFF', font=('Arial', 12, 'bold'))
    style.map('TButton', background=[('active', '#800000')])
    style.configure('TLabel', background='#333333', foreground='#FFFFFF', font=('Arial', 12))
    style.configure('TEntry', fieldbackground='#555555', foreground='#FFFFFF', font=('Arial', 12))

    # Configurar fundo da janela
    root.configure(background='#333333')

    return style
