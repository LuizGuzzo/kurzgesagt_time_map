import datetime
import sys
import tkinter as tk
from tkinter import messagebox

# Configurações gerais
LINE_LENGTH_CM = 30        # Escala real desejada: 30 cm
NUM_ANOS = 100             # De 0 a 99 anos
VERTICAL_SPACING = 40      # Espaçamento vertical base entre linhas (pixels)
EXTRA_SPACING = 20         # Espaçamento extra na linha com evento
MARGIN = 20                # Margem lateral (pixels)

# Data de nascimento fixa
BIRTH_DATE = datetime.datetime.strptime("03/05/1997", "%d/%m/%Y")

def calcula_idade(event_date):
    """Retorna a idade (em anos com fração) considerando a data de nascimento."""
    if event_date < BIRTH_DATE:
        raise ValueError("A data do evento deve ser posterior à data de nascimento!")
    diff_days = (event_date - BIRTH_DATE).days
    return diff_days / 365.25

def parse_events_from_file(file_path):
    """
    Lê um arquivo .txt onde cada linha está no formato:
         dd/mm/aaaa - nome do evento
    Retorna uma lista de tuplas (event_date, event_name).
    """
    events = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                date_str, name = line.split(" - ", 1)
                event_date = datetime.datetime.strptime(date_str.strip(), "%d/%m/%Y")
                events.append((event_date, name.strip()))
            except Exception as e:
                print(f"Erro ao processar a linha: {line}\n{e}")
    return events

class TimelineAppBase:
    """
    Classe base para o desenho da timeline.

    - A escala "real" de 30 cm é definida a partir do DPI da tela e pode ser ajustada pelo zoom.
    - O canvas acompanha a largura da janela; as linhas horizontais se estendem de MARGIN até a margem direita.
    - A numeração aparece em ambos os lados (esquerda e direita).
    - O zigzag é desenhado usando os endpoints naturais (linhas pares terminam à direita; ímpares, à esquerda).
    - São desenhados marcadores verticais em verde indicando os limites dos 30 cm:
         • A cada 30 cm: traços maiores (dash=(15,8), width=3, cor "#008000").
         • A cada 15 cm (não inteiros): traços menores (dash=(8,4), width=1, cor "#00A000").
         • A cada 7,5 cm (os demais): pontilhados (dash=(1,2), width=1, cor "#00C000").
    - Uma legenda é desenhada no canto superior esquerdo explicando os marcadores.
    """
    def __init__(self, root):
        self.root = root
        dpi = root.winfo_fpixels('1i')  # pixels por polegada
        self.pixels_per_cm = dpi / 2.54
        self.original_line_length_px = int(LINE_LENGTH_CM * self.pixels_per_cm)
        self.zoom_factor = 1.0
        self.line_length_px = int(self.original_line_length_px * self.zoom_factor)
        
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.info_label = tk.Label(root, text=f"Linha: {LINE_LENGTH_CM} cm = {self.line_length_px} pixels (Zoom: {self.zoom_factor:.2f})")
        self.info_label.pack(side="bottom", fill="x")
        self.canvas.bind("<Configure>", self.on_configure)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
    
    def get_extra_lines(self):
        """Retorna um conjunto com os índices das linhas que devem ter espaçamento extra.
        Por padrão, nenhum. Sobrescreva nas classes derivadas se necessário."""
        return set()
    
    def draw_base_timeline(self, line_color="lightgray", zigzag_color="gray"):
        """Desenha as linhas horizontais (ocupando toda a largura do canvas),
        os números (em ambos os lados) e o zigzag entre elas, considerando espaçamentos extras."""
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        full_line_end = canvas_width - MARGIN
        extra_lines = self.get_extra_lines()
        y_positions = []
        offset = MARGIN
        for i in range(NUM_ANOS):
            y_positions.append(offset)
            if i in extra_lines:
                offset += VERTICAL_SPACING + EXTRA_SPACING
            else:
                offset += VERTICAL_SPACING
        total_height = offset + MARGIN
        self.y_positions = y_positions
        self.canvas.config(scrollregion=(0, 0, canvas_width, total_height))
        
        # Desenha as linhas horizontais e os rótulos de idade em ambos os lados
        for i in range(NUM_ANOS):
            y = y_positions[i]
            self.canvas.create_line(MARGIN, y, full_line_end, y, fill=line_color)
            self.canvas.create_text(MARGIN - 5, y, text=str(i), anchor="e", font=("Arial", 10))
            self.canvas.create_text(full_line_end + 5, y, text=str(i), anchor="w", font=("Arial", 10))
        
        # Desenha o zigzag
        connection_points = []
        for i in range(NUM_ANOS):
            y = y_positions[i]
            endpoint = full_line_end if (i % 2 == 0) else MARGIN
            connection_points.append((endpoint, y))
        for i in range(NUM_ANOS - 1):
            (x_i, y_i) = connection_points[i]
            y_next = y_positions[i+1]
            natural_next = connection_points[i+1][0]
            self.canvas.create_line(x_i, y_i, x_i, y_next, fill=zigzag_color, width=2)
            self.canvas.create_line(x_i, y_next, natural_next, y_next, fill=zigzag_color, width=2)
        
        # Desenha os marcadores verticais a cada múltiplo da escala (30 cm com zoom)
        factor = 0.25
        while True:
            marker_x = MARGIN + factor * self.line_length_px
            if marker_x >= canvas_width:
                break
            if abs(factor % 1.0) < 1e-6:  # 30 cm
                dash = (15,8)
                width = 3
                color = "#008000"  # verde intenso
            elif abs(factor % 0.5) < 1e-6:  # 15 cm
                dash = (8,4)
                width = 1
                color = "#00A000"  # verde intermediário
            else:  # 7.5 cm
                dash = (1,2)
                width = 1
                color = "#00C000"  # verde mais saturado
            self.canvas.create_line(marker_x, 0, marker_x, total_height, fill=color, dash=dash, width=width)
            factor += 0.25

        # Desenha a legenda
        self.draw_legend(canvas_width, total_height)
    
    def draw_legend(self, canvas_width, total_height):
        """Desenha uma legenda no canto superior esquerdo explicando os marcadores."""
        legend_x = MARGIN + 10
        legend_y = MARGIN + 10
        legend_width = 220
        legend_height = 80
        # Fundo branco com borda preta
        self.canvas.create_rectangle(legend_x, legend_y, legend_x+legend_width, legend_y+legend_height, fill="white", outline="black")
        # Legenda para 30 cm
        self.canvas.create_line(legend_x+10, legend_y+15, legend_x+10+40, legend_y+15,
                                fill="#008000", dash=(15,8), width=3)
        self.canvas.create_text(legend_x+60, legend_y+15, text="30 cm", anchor="w", font=("Arial", 10))
        # Legenda para 15 cm
        self.canvas.create_line(legend_x+10, legend_y+35, legend_x+10+40, legend_y+35,
                                fill="#00A000", dash=(8,4), width=1)
        self.canvas.create_text(legend_x+60, legend_y+35, text="15 cm", anchor="w", font=("Arial", 10))
        # Legenda para 7.5 cm
        self.canvas.create_line(legend_x+10, legend_y+55, legend_x+10+40, legend_y+55,
                                fill="#00C000", dash=(1,2), width=1)
        self.canvas.create_text(legend_x+60, legend_y+55, text="7.5 cm", anchor="w", font=("Arial", 10))
    
    def zoom(self, event):
        """Ajusta o zoom conforme o scroll do mouse e redesenha a timeline."""
        if hasattr(event, 'delta'):
            if event.delta > 0:
                self.zoom_factor *= 1.1
            elif event.delta < 0:
                self.zoom_factor /= 1.1
        else:
            if event.num == 4:
                self.zoom_factor *= 1.1
            elif event.num == 5:
                self.zoom_factor /= 1.1
        self.line_length_px = int(self.original_line_length_px * self.zoom_factor)
        self.info_label.config(text=f"Linha: {LINE_LENGTH_CM} cm = {self.line_length_px} pixels (Zoom: {self.zoom_factor:.2f})")
        self.redraw()
    
    def on_configure(self, event):
        self.redraw()
    
    def redraw(self):
        """Método a ser sobrescrito nas classes derivadas."""
        pass

class TimelineAppInteractive(TimelineAppBase):
    """
    Modo interativo (único evento): o usuário informa uma data e o evento é plotado.
    Acima do marcador (círculo vermelho) são exibidas as distâncias (esquerda e direita)
    calculadas com base na escala fixa de 30 cm.
    A linha que contém o evento recebe espaçamento extra para evitar sobreposição com a linha inferior.
    """
    def __init__(self, root, idade_evento, frac_evento):
        self.idade_evento = idade_evento
        self.frac_evento = frac_evento
        self.event_line = int(idade_evento)
        super().__init__(root)
        self.redraw()
    
    def get_extra_lines(self):
        return {self.event_line}
    
    def redraw(self):
        self.draw_base_timeline()
        line_length_px = self.line_length_px
        event_y = self.y_positions[self.event_line]
        if self.event_line % 2 == 0:
            event_marker_x = MARGIN + self.frac_evento * line_length_px
        else:
            event_marker_x = MARGIN + (line_length_px - self.frac_evento * line_length_px)
        r = 5
        self.canvas.create_oval(event_marker_x - r, event_y - r,
                                 event_marker_x + r, event_y + r, fill="red")
        if self.event_line % 2 == 0:
            left_cm = self.frac_evento * LINE_LENGTH_CM
            right_cm = LINE_LENGTH_CM - left_cm
        else:
            left_cm = (1 - self.frac_evento) * LINE_LENGTH_CM
            right_cm = LINE_LENGTH_CM - left_cm
        self.canvas.create_text(event_marker_x, event_y - 20,
                                text=f"Esq: {left_cm:.2f} cm | Dir: {right_cm:.2f} cm",
                                fill="blue", font=("Arial", 10, "bold"))

class TimelineAppFile(TimelineAppBase):
    """
    Modo arquivo: lê um arquivo .txt com linhas no formato:
         dd/mm/aaaa - nome do evento
    Para cada evento (se vários ocorrerem na mesma linha, essa linha recebe espaçamento extra),
    calcula a posição (baseada na data) e exibe:
       • Acima do marcador: as distâncias (esquerda e direita) com base na escala de 30 cm.
       • Abaixo do marcador: o nome do evento.
    """
    def __init__(self, root, events):
        self.events = []
        for (ev_date, ev_name) in events:
            try:
                idade = calcula_idade(ev_date)
                if 0 <= idade < NUM_ANOS:
                    self.events.append({
                        "date": ev_date,
                        "name": ev_name,
                        "idade": idade,
                        "linha": int(idade),
                        "frac": idade - int(idade)
                    })
            except Exception as e:
                print(f"Ignorando evento {ev_date} - {ev_name}: {e}")
        super().__init__(root)
        self.redraw()
    
    def get_extra_lines(self):
        return {ev["linha"] for ev in self.events}
    
    def redraw(self):
        self.draw_base_timeline()
        line_length_px = self.line_length_px
        for ev in self.events:
            linha = ev["linha"]
            frac = ev["frac"]
            event_y = self.y_positions[linha]
            if linha % 2 == 0:
                event_marker_x = MARGIN + frac * line_length_px
            else:
                event_marker_x = MARGIN + (line_length_px - frac * line_length_px)
            r = 5
            self.canvas.create_oval(event_marker_x - r, event_y - r,
                                    event_marker_x + r, event_y + r, fill="red")
            if linha % 2 == 0:
                left_cm = frac * LINE_LENGTH_CM
                right_cm = LINE_LENGTH_CM - left_cm
            else:
                left_cm = (1 - frac) * LINE_LENGTH_CM
                right_cm = LINE_LENGTH_CM - left_cm
            self.canvas.create_text(event_marker_x, event_y - 20,
                                    text=f"Esq: {left_cm:.2f} cm | Dir: {right_cm:.2f} cm",
                                    fill="blue", font=("Arial", 10, "bold"))
            self.canvas.create_text(event_marker_x, event_y + 20,
                                    text=ev["name"], fill="black", font=("Arial", 10, "bold"))

def main():
    try:
        root = tk.Tk()
        root.geometry("1200x800")
        if len(sys.argv) > 1 and sys.argv[1].lower().endswith(".txt"):
            file_path = sys.argv[1]
            events = parse_events_from_file(file_path)
            if not events:
                print("Nenhum evento válido encontrado no arquivo.")
                return
            root.title("Timeline de Eventos (Arquivo)")
            app = TimelineAppFile(root, events)
        else:
            event_str = input("Digite a data do evento (dd/mm/aaaa): ")
            event_date = datetime.datetime.strptime(event_str, "%d/%m/%Y")
            idade_evento = calcula_idade(event_date)
            frac_evento = idade_evento - int(idade_evento)
            root.title("Timeline (Evento Único)")
            app = TimelineAppInteractive(root, idade_evento, frac_evento)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        print("Erro:", e)

if __name__ == "__main__":
    main()
