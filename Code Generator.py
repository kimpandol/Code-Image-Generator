import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

class ChordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guitar Chord Generator")
        self.root.geometry("450x650")
        self.root.configure(bg="#1a1a1a")

        self.roots = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        self.chord_library = {
            "C": {
                "Major (M)": [(1, 3), (2, 2), (3, 0), (4, 1), (5, 0)],
                "Minor (m)": [(1, 3), (2, 5), (3, 5), (4, 4), (5, 3)],
                "Dominant 7 (7)": [(1, 3), (2, 2), (3, 3), (4, 1), (5, 0)],
                "Major 7 (maj7)": [(1, 3), (2, 2), (3, 0), (4, 0), (5, 0)],
            },
            "A": {
                "Major (M)": [(1, 0), (2, 2), (3, 2), (4, 2), (5, 0)],
                "Minor (m)": [(1, 0), (2, 2), (3, 2), (4, 1), (5, 0)],
                "Dominant 7 (7)": [(1, 0), (2, 2), (3, 0), (4, 2), (5, 0)],
                "Major 7 (maj7)": [(1, 0), (2, 2), (3, 1), (4, 2), (5, 0)],
            },
            "G": {
                "Major (M)": [(0, 3), (1, 2), (2, 0), (3, 0), (4, 0), (5, 3)],
                "Minor (m)": [(0, 3), (1, 5), (2, 5), (3, 3), (4, 3), (5, 3)],
                "Dominant 7 (7)": [(0, 3), (1, 2), (2, 0), (3, 0), (4, 0), (5, 1)],
            },
            "E": {
                "Major (M)": [(0, 0), (1, 2), (2, 2), (3, 1), (4, 0), (5, 0)],
                "Minor (m)": [(0, 0), (1, 2), (2, 2), (3, 0), (4, 0), (5, 0)],
                "Dominant 7 (7)": [(0, 0), (1, 2), (2, 0), (3, 1), (4, 0), (5, 0)],
            },
            "D": {
                "Major (M)": [(2, 0), (3, 2), (4, 3), (5, 2)],
                "Minor (m)": [(2, 0), (3, 2), (4, 3), (5, 1)],
                "Dominant 7 (7)": [(2, 0), (3, 2), (4, 1), (5, 2)],
            }
        }

        self.setup_ui()
        self.update_diagram()

    def setup_ui(self):
        ctrl_frame = tk.Frame(self.root, bg="#1a1a1a", pady=20)
        ctrl_frame.pack()

        tk.Label(ctrl_frame, text="근음:", fg="white", bg="#1a1a1a").grid(row=0, column=0, padx=5)
        self.root_var = tk.StringVar(value="C")
        self.root_combo = ttk.Combobox(ctrl_frame, textvariable=self.root_var, values=self.roots, state="readonly", width=5)
        self.root_combo.grid(row=0, column=1, padx=5)
        self.root_combo.bind("<<ComboboxSelected>>", lambda e: self.update_diagram())

        tk.Label(ctrl_frame, text="타입:", fg="white", bg="#1a1a1a").grid(row=0, column=2, padx=5)
        self.type_var = tk.StringVar(value="Major (M)")
        self.type_combo = ttk.Combobox(ctrl_frame, textvariable=self.type_var, 
                                       values=["Major (M)", "Minor (m)", "Dominant 7 (7)", "Major 7 (maj7)"], 
                                       state="readonly", width=15)
        self.type_combo.grid(row=0, column=3, padx=5)
        self.type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_diagram())

        save_btn = tk.Button(ctrl_frame, text="저장", command=self.save_image, bg="#d4af37", fg="black", font=("Arial", 10, "bold"))
        save_btn.grid(row=0, column=4, padx=10)

        self.img_label = tk.Label(self.root, bg="#1a1a1a")
        self.img_label.pack(pady=10)

    def get_chord_dots(self, root, c_type):
        if root in self.chord_library and c_type in self.chord_library[root]:
            return self.chord_library[root][c_type]
        
        root_fret = {'F':1, 'F#':2, 'G':3, 'G#':4, 'A':5, 'A#':6, 'B':7}.get(root, 1)
        if "Minor" in c_type:
            return [(0, root_fret), (1, root_fret+2), (2, root_fret+2), (3, root_fret), (4, root_fret), (5, root_fret)]
        return [(0, root_fret), (1, root_fret+2), (2, root_fret+2), (3, root_fret+1), (4, root_fret), (5, root_fret)]

    def draw_chord(self, root_name, type_name):
        width, height = 300, 400
        # 배경을 투명하게 설정 (RGBA 모드, (0,0,0,0))
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 실제 코드가 그려지는 박스 영역
        draw.rounded_rectangle([20, 20, 280, 380], radius=20, fill=(35, 35, 35, 255))
        
        try: font = ImageFont.truetype("arial.ttf", 25)
        except: font = ImageFont.load_default()
        draw.text((150, 60), f"{root_name} {type_name}", fill="white", font=font, anchor="mm")

        margin_x, margin_top = 70, 110
        grid_w, grid_h = 160, 220
        s_spacing, f_spacing = grid_w / 5, grid_h / 4

        dots = self.get_chord_dots(root_name, type_name)
        active_frets = [d[1] for d in dots if d[1] > 0]
        min_fret = min(active_frets) if active_frets else 0
        start_fret = 0 if min_fret <= 3 else min_fret

        if start_fret > 0:
            draw.text((35, margin_top + 10), f"{start_fret}f", fill=(180, 180, 180, 255))

        for i in range(5):
            y = margin_top + (i * f_spacing)
            line_w = 6 if start_fret == 0 and i == 0 else 2
            draw.line([(margin_x, y), (margin_x+grid_w, y)], fill=(200, 200, 200, 255), width=line_w)
        for i in range(6):
            x = margin_x + (i * s_spacing)
            draw.line([(x, margin_top), (x, margin_top+grid_h)], fill=(200, 200, 200, 255), width=2)

        for s_idx, f_val in dots:
            cx = margin_x + (s_idx * s_spacing)
            if f_val == 0:
                draw.ellipse([cx-7, margin_top-22, cx+7, margin_top-8], outline="white", width=2)
            else:
                rel_fret = f_val if start_fret == 0 else (f_val - start_fret + 1)
                cy = margin_top + (rel_fret * f_spacing) - (f_spacing / 2)
                draw.ellipse([cx-14, cy-14, cx+14, cy+14], fill="white", outline="#d4af37", width=2)
        return img

    def update_diagram(self):
        self.current_img = self.draw_chord(self.root_var.get(), self.type_var.get())
        
        # Tkinter 미리보기용 배경 입히기 (Tkinter는 투명 PNG 미리보기를 기본 지원하지 않음)
        preview_img = Image.new("RGB", (300, 400), (26, 26, 26))
        preview_img.paste(self.current_img, (0, 0), self.current_img)
        
        self.tk_img = ImageTk.PhotoImage(preview_img)
        self.img_label.config(image=self.tk_img)

    def save_image(self):
        filename = f"{self.root_var.get()}_{self.type_var.get()}.png".replace(" ", "_")
        # 투명 배경 유지를 위해 PNG 형식으로 저장
        self.current_img.save(filename)
        messagebox.showinfo("성공", f"투명 배경 PNG로 저장 완료: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChordGeneratorApp(root)
    root.mainloop()