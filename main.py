import tkinter as tk
from tkinter import messagebox
from banco import criar_tabela, adicionar_movimentacao, listar_movimentacoes
from datetime import datetime
from tkinter import ttk, messagebox

# ---------------- JANELA PRINCIPAL ----------------
root = tk.Tk()
root.title("Sistema de Caixa")
root.geometry("720x480")
root.configure(bg="#f7f9fc")

# Configuração de estilo
style = ttk.Style()
style.theme_use("clam") # deixa os weights mais modernos

# Estilo da Treeview (tabela)
style.configure(
    "Treeview",
    background="#ffffff",
    foreground="#333333",
    rowheight=26,
    )
style.map("Treeview",
          background=[("selected", "#1a73e8")],
          foreground=[("selected", "white")])
    
# Cabeçalho da tabela
style.configure(
    "Treeview.Heading",
    background="#eef2f7",
    foreground="#111827",
    font=("segoe UI", 10, "bold")
    )
    
# Criar tabela ao iniciar
# --- LISTA DE MOVIMENTAÇÕES ---
list_frame = tk.Frame(root, bg="#f7f9fc", padx=12, pady=0)
list_frame.grid(row=1, column=0, sticky="nsew")

# Faz a área da lista crescer com a janela
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
list_frame.grid_rowconfigure(1, weight=1)
list_frame.grid_columnconfigure(0, weight=1)

# Título
lbl_mov = tk.Label(list_frame, text="Movimentações", bg="#f7f9fc",
                   fg="#111827", font=("Segoe UI", 12, "bold"))
lbl_mov.grid(row=0, column=0, sticky="w", pady=(0,6))

# --- TABELA (Treeview) ---
list_frame = tk.Frame(root, bg="#f4f6f9")
list_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=16, pady=(0,16))

cols = ("Tipo", "Valor", "Descricao", "Data")
tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)

# Cabeçalhos centralizados
tree.heading("Tipo", text="Tipo", anchor="center")
tree.heading("Valor", text="Valor", anchor="center")
tree.heading("Descricao", text="Descrição", anchor="center")
tree.heading("Data", text="Data", anchor="center")

# Colunas: esconde a #0 e define alinhamentos/larguras
tree.column("#0", width=0, stretch=False)
tree.column("Tipo", width=120, anchor="w")        # à esquerda
tree.column("Valor", width=110, anchor="e")       # à direita
tree.column("Descricao", width=300, anchor="w")   # à esquerda
tree.column("Data", width=160, anchor="center")   # centralizada

# Scroll vertical
scroll = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)

tree.grid(row=0, column=0, sticky="nsew")
scroll.grid(row=0, column=1, sticky="ns")

# Ajustar colunas automaticamente quando a janela é redimensionada
list_frame.grid_columnconfigure(0, weight=1)
list_frame.grid_rowconfigure(0, weight=1)

# Garantir que a coluna Data possa se expandir (não ficar oculta)
tree.column("Data", width=180, anchor="center", stretch=True)

# ---------------- FUNÇÕES ----------------
def salvar():
    tipo = tipo_var.get()
    valor = valor_entry.get()
    descricao = descricao_entry.get()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not valor:
        messagebox.showerror("Erro", "Informe o valor")
        return

    try:
        valor_float = float(valor.replace(",", "."))  # aceita vírgula ou ponto
        adicionar_movimentacao(tipo, valor_float, descricao, data)
        messagebox.showinfo("Sucesso", "Movimentação salva com sucesso!")
        valor_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        atualizar_lista()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def atualizar_lista():
    # limpa
    for item in tree.get_children():
        tree.delete(item)

    # carrega do banco
    for mov in listar_movimentacoes():
        # esquema esperado: (id, tipo, valor, descricao, data)
        _id, tipo, valor, descricao, data = mov

        # formata valor com "R$" e separador brasileiro
        try:
            v = float(valor)
            valor_fmt = f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            valor_fmt = f"R$ {valor}"

        # insere **exatamente 4** valores (na ordem das colunas)
        tree.insert("", "end", values=(tipo, valor_fmt, descricao, data))

# ---------- FRAME SUPERIOR (formulário) ----------

top = tk.Frame(root, bg="#f7f9fc", padx=12, pady=12)
top.grid(row=0, column=0, sticky="ew")
top.grid_columnconfigure(3, weight=1)   # faz a coluna do valor/descrição crescer

# Tipo
tk.Label(top, text="Tipo:", bg="#f7f9fc", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
tipo_var = tk.StringVar(value="Entrada")
# (Se preferir manter OptionMenu, pode; mas o Combobox fica mais moderno)
tipo_menu = ttk.Combobox(top, textvariable=tipo_var,
                         values=["Entrada", "Saída"], state="readonly", font=("Segoe UI", 11))
tipo_menu.grid(row=0, column=1, sticky="we", padx=(6, 12))

# Valor
tk.Label(top, text="Valor:", bg="#f7f9fc", font=("Segoe UI", 11)).grid(row=0, column=2, sticky="w")
valor_entry = tk.Entry(top, font=("Segoe UI", 11))
valor_entry.grid(row=0, column=3, sticky="we", padx=(6, 12))

# Descrição
tk.Label(top, text="Descrição:", bg="#f7f9fc", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=(8,0))
descricao_entry = tk.Entry(top, font=("Segoe UI", 11))
descricao_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=(6, 12), pady=(8,0))

# ÚNICO botão Salvar (com hover)
salvar_btn = tk.Button(
    top, text="Salvar", command=salvar,
    bg="#1a73e8", fg="white",
    activebackground="#1669c1", activeforeground="white",
    relief="flat", font=("Segoe UI", 11, "bold"),
    padx=16, pady=6
)
salvar_btn.grid(row=0, column=4, rowspan=2, sticky="nswe", padx=8)

def _hover_on(e):  salvar_btn.configure(bg="#1669c1")
def _hover_off(e): salvar_btn.configure(bg="#1a73e8")
salvar_btn.bind("<Enter>", _hover_on)
salvar_btn.bind("<Leave>", _hover_off)


root.mainloop()
