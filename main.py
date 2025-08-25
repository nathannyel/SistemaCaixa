import tkinter as tk
from tkinter import messagebox
from banco import criar_tabela, adicionar_movimentacao, listar_movimentacoes
from datetime import datetime
from tkinter import ttk

# Criar tabela ao iniciar
criar_tabela()

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
    def atualizar_lista():
    # Limpar tabela
        for item in tree.get_children():
            tree.delete(item)

    # Inserir novos dados
        for mov in listar_movimentacoes():
            _, tipo, valor, descricao, data = mov
            tree.insert("", "end", values=(tipo, f"{valor:.2f}", descricao, data))

# ---------------- JANELA PRINCIPAL ----------------
root = tk.Tk()
root.title("Sistema de Caixa")
root.geometry("720x480")
root.configure(bg="#f7f9fc")

# ---------- FRAME SUPERIOR (formulário) ----------
top = tk.Frame(root, bg="#f7f9fc", padx=12, pady=12)
top.pack(fill="x")

# Tipo
tk.Label(top, text="Tipo:", bg="#f7f9fc", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
tipo_var = tk.StringVar(value="Entrada")
tipo_menu = tk.OptionMenu(top, tipo_var, "Entrada", "Saída")
tipo_menu.config(font=("Segoe UI", 11))
tipo_menu.grid(row=0, column=1, sticky="we", padx=(6, 12))

# Valor
tk.Label(top, text="Valor:", bg="#f7f9fc", font=("Segoe UI", 11)).grid(row=0, column=2, sticky="w")
valor_entry = tk.Entry(top, font=("Segoe UI", 11))
valor_entry.grid(row=0, column=3, sticky="we", padx=(6, 12))

# Descrição
tk.Label(top, text="Descrição:", bg="#f7f9fc", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=(8, 0))
descricao_entry = tk.Entry(top, font=("Segoe UI", 11))
descricao_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=(6, 12), pady=(8, 0))

# Botão Salvar
salvar_btn = tk.Button(
    top,
    text="Salvar",
    command=salvar,
    bg="#2563eb", fg="white",
    activebackground="#1d4ed8", activeforeground="white",
    relief="flat",
    padx=14, pady=8,
    font=("Segoe UI", 11, "bold")
)
salvar_btn.grid(row=0, column=4, rowspan=2, sticky="nswe")

# Faz as colunas do formulário expandirem
for col in range(0, 4):
    top.grid_columnconfigure(col, weight=1)

# ---------- FRAME INFERIOR (lista como tabela) ----------
list_frame = tk.Frame(root, bg="#ffffff", padx=12, pady=12)
list_frame.pack(fill="both", expand=True)

tk.Label(list_frame, text="Movimentações", bg="#ffffff", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

# Criar a Treeview
colunas = ("tipo", "valor", "descricao", "data")
tree = ttk.Treeview(list_frame, columns=colunas, show="headings", height=10)

# Definir cabeçalhos
tree.heading("tipo", text="Tipo")
tree.heading("valor", text="Valor (R$)")
tree.heading("descricao", text="Descrição")
tree.heading("data", text="Data")

# Ajustar larguras
tree.column("tipo", width=80, anchor="center")
tree.column("valor", width=100, anchor="center")
tree.column("descricao", width=200, anchor="w")
tree.column("data", width=150, anchor="center")

tree.pack(fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
