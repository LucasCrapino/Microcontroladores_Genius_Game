import random
import threading
import os
import requests
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import psycopg2
from datetime import datetime

# --- Configurações do Jogo ---
COLORS = {
    "azul": {"normal": "#1e3a8a", "ativo": "#60a5fa"},
    "vermelho": {"normal": "#7f1d1d", "ativo": "#f87171"},
    "amarelo": {"normal": "#854d0e", "ativo": "#fde047"},
    "verde": {"normal": "#14532d", "ativo": "#86efac"},
}
BUTTON_ORDER = ["azul", "vermelho", "amarelo", "verde"]
TIMINGS = {"blink_on_ms": 500, "blink_off_ms": 200, "click_on_ms": 200}
DIFFICULTY_DECAY = 0.97
MIN_BLINK_ON = 220
INTER_ROUND_DELAY_MS = 2000
WINDOW_W = 520
WINDOW_H = 620

# --- Configuração do Banco (Postgres RDS) ---
DB_CONFIG = {
    "host": "database-1.cl40iigyy6en.sa-east-1.rds.amazonaws.com",
    "port": 5432,
    "user": "postgres",
    "password": "micro123!",
    "database": "postgres",
    "table": "PlacarGenius"
}

UBIDOTS_TOKEN = os.environ.get("UBIDOTS_TOKEN", "BBUS-OLHUjQCSD1iLeg12NH76Z8EIfcFkd4")
UBIDOTS_DEVICE = "simon_device"
UBIDOTS_VARIABLE = "maior_pontuacao"
UBIDOTS_API_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE}"
HEADERS_UBIDOTS = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}

def send_to_ubidots(value):
    """
    Envia um valor para o device/variable no Ubidots.
    Payload: { "<variable_label>": <value> }
    """
    if not UBIDOTS_TOKEN or UBIDOTS_TOKEN == "SEU_UBIDOTS_TOKEN_AQUI":
        print("Ubidots token não configurado. Ignorando envio.")
        return False
    payload = {UBIDOTS_VARIABLE: value}
    try:
        resp = requests.post(UBIDOTS_API_URL, headers=HEADERS_UBIDOTS, json=payload, timeout=8)
        resp.raise_for_status()
        return True
    except Exception as e:
        print("Falha ao enviar para Ubidots:", e)
        return False

class SimonApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simon – Jogo da Memória")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.minsize(WINDOW_W, WINDOW_H)
        self.root.maxsize(WINDOW_W, WINDOW_H)
        self.root.resizable(False, False)
        self.rodada_atual = 1
        self.sequence = []
        self.user_input = []
        self.is_showing = False
        self.blink_on_ms = TIMINGS["blink_on_ms"]
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self.root.destroy()

    def _build_ui(self):
        container = tk.Frame(self.root, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        header = tk.Frame(container)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.label_status = tk.Label(header, text="Clique em Iniciar", font=("Segoe UI", 14, "bold"),
                                     width=34, anchor="w", wraplength=WINDOW_W-40)
        self.label_status.pack(side=tk.LEFT)
        self.label_round = tk.Label(header, text="Rodada: 0", font=("Segoe UI", 12), width=12, anchor="e")
        self.label_round.pack(side=tk.RIGHT)

        indicators = tk.Frame(container)
        indicators.grid(row=1, column=0, columnspan=2, pady=(0, 6))
        bg = indicators.cget("bg")
        self.ind_canvas = tk.Canvas(indicators, width=90, height=28, highlightthickness=0, bg=bg)
        self.ind_canvas.pack()
        self.ind_red_id = self.ind_canvas.create_oval(8, 6, 28, 26, fill="#7f1d1d", outline="#000000")
        self.ind_green_id = self.ind_canvas.create_oval(62, 6, 82, 26, fill="#14532d", outline="#000000")

        grid = tk.Frame(container)
        grid.grid(row=2, column=0, columnspan=2, pady=(4, 4))
        self.buttons = {}
        def make_btn(name, r, c):
            btn = tk.Button(grid, width=14, height=6, relief=tk.RAISED, bd=3,
                            bg=COLORS[name]["normal"], activebackground=COLORS[name]["ativo"],
                            command=lambda n=name: self.on_color_click(n))
            btn.grid(row=r, column=c, padx=8, pady=8)
            self.buttons[name] = btn
        make_btn("azul", 0, 0)
        make_btn("vermelho", 0, 1)
        make_btn("amarelo", 1, 0)
        make_btn("verde", 1, 1)

        actions = tk.Frame(container)
        actions.grid(row=3, column=0, columnspan=2, pady=(12, 0))
        self.btn_start = tk.Button(actions, text="Iniciar", font=("Segoe UI", 12, "bold"),
                                   command=self.start_game, width=12)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_repeat = tk.Button(actions, text="Repetir sequência", state=tk.DISABLED,
                                    command=self.repeat_sequence, width=16)
        self.btn_repeat.pack(side=tk.LEFT)
        self.btn_show_score = tk.Button(actions, text="Ver placar", font=("Segoe UI", 12), command=self.show_score)
        self.btn_show_score.pack(side=tk.LEFT, padx=(8,0))

    def _indicator_set(self, which: str, on: bool):
        if which == "red":
            self.ind_canvas.itemconfig(self.ind_red_id, fill=("#ef4444" if on else "#7f1d1d"))
        elif which == "green":
            self.ind_canvas.itemconfig(self.ind_green_id, fill=("#22c55e" if on else "#14532d"))
        self.ind_canvas.update_idletasks()

    def _indicator_blink(self, which: str, times: int = 2, on_ms: int = 180, off_ms: int = 120, when_done=None):
        def blink_once(rem):
            if rem == 0:
                if when_done: when_done()
                return
            self._indicator_set(which, True)
            self.root.after(on_ms, lambda: (
                self._indicator_set(which, False),
                self.root.after(off_ms, lambda: blink_once(rem - 1))
            ))
        blink_once(times)

    def start_game(self):
        self.rodada_atual = 1
        self.blink_on_ms = TIMINGS["blink_on_ms"]
        self.label_status.config(text="Observando…")
        self.label_round.config(text=f"Rodada: {self.rodada_atual}")
        self.disable_actions_during_show()
        self._indicator_blink("green", times=2, when_done=lambda: self.root.after(INTER_ROUND_DELAY_MS, self.seq_new_round))

    def seq_new_round(self):
        self.sequence = [random.choice(BUTTON_ORDER) for _ in range(self.rodada_atual)]
        self.user_input = []
        self.disable_actions_during_show()
        self.show_sequence(0)

    def repeat_sequence(self):
        if not self.sequence or self.is_showing: return
        self.label_status.config(text="Observando…")
        self.user_input = []
        self.disable_actions_during_show()
        self.show_sequence(0)

    def disable_actions_during_show(self):
        self.is_showing = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_repeat.config(state=tk.DISABLED)
        self.btn_show_score.config(state=tk.NORMAL)
        for b in self.buttons.values(): b.config(state=tk.DISABLED)

    def enable_actions_after_show(self):
        self.is_showing = False
        self.btn_start.config(state=tk.DISABLED)
        self.btn_repeat.config(state=tk.NORMAL)
        self.btn_show_score.config(state=tk.NORMAL)
        for b in self.buttons.values(): b.config(state=tk.NORMAL)
        self.label_status.config(text="Sua vez! Clique na sequência correta.")

    def show_sequence(self, idx: int):
        if idx >= len(self.sequence):
            self.enable_actions_after_show()
            return
        name = self.sequence[idx]
        btn = self.buttons[name]
        self._set_button_glow(btn, name, True)
        self.root.after(self.blink_on_ms, lambda: self._show_sequence_off(idx))

    def _show_sequence_off(self, idx: int):
        name = self.sequence[idx]
        btn = self.buttons[name]
        self._set_button_glow(btn, name, False)
        self.root.after(TIMINGS["blink_off_ms"], lambda: self.show_sequence(idx + 1))

    def _set_button_glow(self, btn: tk.Button, name: str, on: bool):
        btn.config(bg=COLORS[name]["ativo" if on else "normal"])
        btn.update_idletasks()

    def on_color_click(self, name: str):
        if self.is_showing: return
        btn = self.buttons[name]
        self._set_button_glow(btn, name, True)
        self.root.after(TIMINGS["click_on_ms"], lambda: self._set_button_glow(btn, name, False))
        self.user_input.append(name)
        idx = len(self.user_input) - 1
        if self.user_input[idx] != self.sequence[idx]:
            self.handle_wrong()
            return
        if len(self.user_input) == len(self.sequence):
            self.handle_round_success()

    def handle_wrong(self):
        self.label_status.config(text="Errou! 😵")
        def end_game():
            self.flash_all()
            self.prompt_save_score()
        self._indicator_blink("red", times=2, when_done=end_game)

    def flash_all(self):
        for name, btn in self.buttons.items():
            self._set_button_glow(btn, name, True)
        self.root.after(400, lambda: [self._set_button_glow(btn, name, False) for name, btn in self.buttons.items()])

    def handle_round_success(self):
        self.label_status.config(text="Acertou! Próxima rodada… ✅")
        self.rodada_atual += 1
        self.label_round.config(text=f"Rodada: {self.rodada_atual}")
        self.blink_on_ms = max(int(self.blink_on_ms * DIFFICULTY_DECAY), MIN_BLINK_ON)
        self.disable_actions_during_show()
        self._indicator_blink("green", times=2, when_done=lambda: self.root.after(INTER_ROUND_DELAY_MS, self.seq_new_round))

    def prompt_save_score(self):
        score = self.rodada_atual - 1
        name = simpledialog.askstring("Salvar pontuação", f"Sua pontuação: {score}\nDigite seu nome (3 letras):", parent=self.root)
        if name:
            name = name[:3].upper()
            self.save_score(name, score)
        self.btn_start.config(state=tk.NORMAL)
        self.btn_repeat.config(state=tk.DISABLED)
        for b in self.buttons.values(): b.config(state=tk.DISABLED)
        self.label_status.config(text="Clique em Iniciar para jogar novamente.")

    def save_score(self, name, score):
        try:
            conn = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )
            cursor = conn.cursor()
            sql = f"INSERT INTO {DB_CONFIG['table']} (nome, pontuacao) VALUES (%s, %s)"
            cursor.execute(sql, (name, score))
            conn.commit()

            # buscar maior pontuação atual
            cursor.execute(f"SELECT MAX(pontuacao) FROM {DB_CONFIG['table']}")
            max_row = cursor.fetchone()
            maior = max_row[0] if max_row and max_row[0] is not None else score

            # enviar para Ubidots em thread para não bloquear UI
            threading.Thread(target=send_to_ubidots, args=(maior,), daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o placar:\n{e}")
        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

    def show_score(self):
        try:
            conn = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )
            cursor = conn.cursor()
            sql = f"SELECT nome, pontuacao, dataCriacao FROM {DB_CONFIG['table']} ORDER BY pontuacao DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível buscar o placar:\n{e}")
            return
        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

        score_window = tk.Toplevel(self.root)
        score_window.title("Placar")
        score_window.geometry("300x300")
        tree = ttk.Treeview(score_window, columns=("Nome", "Pontuação", "Data"), show="headings")
        tree.heading("Nome", text="Nome")
        tree.heading("Pontuação", text="Pontuação")
        tree.heading("Data", text="Data")
        tree.pack(fill=tk.BOTH, expand=True)
        for row in rows:
            tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimonApp(root)
    root.mainloop()
