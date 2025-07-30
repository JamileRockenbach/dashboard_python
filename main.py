import unidecode
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox

df_global = None
def abrir_csv():
    global df_global
    caminho = filedialog.askopenfilename(filetypes=[("Arquivo CSV", "*.csv")])
    if not caminho:
        return
    try:
        df = pd.read_csv(caminho)
        df.columns = df.columns.str.strip().str.lower()
        if 'nota' in df.columns:
            df['nota'] = pd.to_numeric(df['nota'], errors='coerce')
            df = df.dropna(subset=['nota'])

        if 'nome' not in df.columns or 'nota' not in df.columns:
            messagebox.showerror("Erro", "O CSV precisa ter as colunas: 'nome' e 'nota'")
            return
        df_global = df
        mostrar_resultados(df)
    except Exception as e:
        messagebox.showerror("Erro ao abrir o arquivo", str(e))

def mostrar_resultados(df):
    media = df['nota'].mean()
    mediana = df['nota'].median()
    maximo = df['nota'].max()
    minimo = df['nota'].min()

    media_label.config(text=f"Média: {media:.2f}")
    mediana_label.config(text=f"Mediana: {mediana:.2f}")
    maximo_label.config(text=f"Máximo: {maximo}")
    minimo_label.config(text=f"Mínimo: {minimo}")

def mostrar_dispersao():
    global ultima_figura
    if df_global is None:
        messagebox.showwarning("Aviso", "Abra um CSV primeiro!")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df_global['nome'], df_global['nota'], color='orange', s=100, edgecolors='k')
    ax.set_title("Dispersão das Notas")
    ax.set_xlabel("Nome")
    ax.set_ylabel("Nota")
    plt.xticks(rotation=45)
    plt.tight_layout()
    ultima_figura = fig
    plt.show()

def mostrar_boxplot():
    global ultima_figura
    if df_global is None:
        messagebox.showwarning("Aviso", "Abra um CSV primeiro!")
        return

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.boxplot(df_global['nota'], patch_artist=True, boxprops=dict(facecolor='lightgreen'))
    ax.set_title("Box Plot das Notas")
    ax.set_ylabel("Nota")
    plt.tight_layout()
    ultima_figura = fig
    plt.show()

def mostrar_barras():
    global ultima_figura
    if df_global is None:
        messagebox.showwarning("Aviso", "Abra um CSV primeiro!")
        return
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_global['nome'], df_global['nota'], color='skyblue', edgecolor='black')
    ax.set_title("Gráfico de Barras das Notas")
    ax.set_xlabel("Nome")
    ax.set_ylabel("Nota")
    plt.xticks(rotation=45)
    plt.tight_layout()
    ultima_figura = fig
    plt.show()

def mostrar_pizza():
    global ultima_figura
    if df_global is None:
        messagebox.showwarning("Aviso", "Abra um CSV primeiro!")
        return
    
    df_grouped = df_global.groupby('nota').size()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df_grouped, labels=df_grouped.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
    ax.set_title("Distribuição das Notas (Pizza)")
    ultima_figura = fig
    plt.show()

def filtrar_nome():
    if df_global is None:
        messagebox.showwarning("Aviso", "Abra um CSV primeiro!")
        return

    nome = entrada_nome.get().strip().lower()
    if not nome:
        messagebox.showinfo("Info", "Digite um nome para filtrar.")
        return
    try:
        nomes_normalizados = df_global['nome'].dropna().astype(str).apply(lambda x: unidecode.unidecode(x.lower()))
        nome_normalizado = unidecode.unidecode(nome)
        filtrado = df_global[nomes_normalizados.str.contains(nome_normalizado)]
        if filtrado.empty:
            resultado.config(text=f"Nenhum resultado para '{entrada_nome.get()}'")
        else:
            resultado.config(text=f"{len(filtrado)} resultado(s) encontrado(s) para '{entrada_nome.get()}'")
            mostrar_resultados(filtrado)
    except Exception as e:
        messagebox.showerror("Erro ao filtrar", str(e))

def limpar_dados():
    global df_global
    df_global = None
    media_label.config(text="")
    mediana_label.config(text="")
    maximo_label.config(text="")
    minimo_label.config(text="")
    entrada_nome.delete(0, tk.END)

def mudar_cor(botao, cor_nova, cor_original):
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_nova))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor_original))


janela = tk.Tk()
janela.iconbitmap("assets/icone.ico")
janela.configure(bg="#98c6f8") 
janela.title("Mini Dashboard de Dados")
janela.geometry("700x500") 
janela.resizable(False, False)

btn_abrir = tk.Button(janela, text="Abrir CSV", command=abrir_csv, font=("Segoe UI", 12))
btn_abrir.pack(pady=8)
frame_resultado = tk.Frame(janela, bg="#b9d5f1")
frame_resultado.pack(pady=5)

media_label = tk.Label(frame_resultado, text="", font=("Segoe UI", 11), bg="#b9d5f1")
media_label.pack()
mediana_label = tk.Label(frame_resultado, text="", font=("Segoe UI", 11), bg="#b9d5f1")
mediana_label.pack()
maximo_label = tk.Label(frame_resultado, text="", font=("Segoe UI", 11), fg="#065206", bg="#b9d5f1") 
maximo_label.pack()
minimo_label = tk.Label(frame_resultado, text="", font=("Segoe UI", 11), fg="#D20707", bg="#b9d5f1") 
minimo_label.pack()

resultado = tk.Label(janela, text="", font=("Segoe UI", 10), fg="red", bg="#b9d5f1")
resultado.pack(pady=3)
frame_filtro = tk.Frame(janela)
frame_filtro.pack(pady=5)
entrada_nome = tk.Entry(frame_filtro, font=("Segoe UI", 11), width=20)
entrada_nome.pack(side=tk.LEFT, padx=5)
btn_filtrar = tk.Button(frame_filtro, text="Filtrar por Nome", command=filtrar_nome)
btn_filtrar.pack(side=tk.LEFT)

btn_dispersao = tk.Button(janela, text="Diagrama de Dispersão", command=mostrar_dispersao)
btn_dispersao.pack(pady=4)
btn_boxplot = tk.Button(janela, text="Box Plot", command=mostrar_boxplot)
btn_boxplot.pack(pady=4)
btn_barras = tk.Button(janela, text="Gráfico de Barras", command=mostrar_barras)
btn_barras.pack(pady=4)
btn_pizza = tk.Button(janela, text="Gráfico de Pizza", command=mostrar_pizza)
btn_pizza.pack(pady=4)
btn_limpar = tk.Button(janela, text="Limpar Dados", command=limpar_dados)
btn_limpar.pack(pady=6)

botoes = [btn_abrir, btn_filtrar, btn_dispersao, btn_boxplot, btn_barras, btn_pizza, btn_limpar]
for botao in botoes:
    mudar_cor(botao, "#4a90e2", "#d0e7ff")


frase = tk.Label(janela, text="Dashboard de Dados 📊", font=("Segoe UI", 22),bg="#98c6f8",fg="gray25"
)
frase.pack(side=tk.BOTTOM, pady=20)
linha_divisoria = tk.Frame(janela, height=2, bg="#28292A") 
linha_divisoria.pack(fill='x', padx=2, pady=(0,7))

janela.mainloop()