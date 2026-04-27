import tkinter as tk
from tkinter import font as tkfont
from auth_manager import AuthManager as am
from validator import Validator
# ─────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────
BG          = "#0a0a0f"
CARD_BG     = "#111118"
BORDER      = "#1e1e2e"
ACCENT      = "#c8ff57"
ACCENT_DIM  = "#1a2406"
TEXT        = "#f0f0f5"
MUTED       = "#6b6b80"
ERROR_COL   = "#ff6b6b"
INPUT_BG    = "#16161f"
INPUT_FOCUS = "#1e1e2e"

W, H        = 500, 770         # window size


# ─────────────────────────────────────────
#  HELPER — rounded rectangle on Canvas
# ─────────────────────────────────────────
def round_rect(canvas, x1, y1, x2, y2, r=14, **kw):
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)


# ─────────────────────────────────────────
#  CUSTOM ENTRY WIDGET
# ─────────────────────────────────────────
class StyledEntry(tk.Frame):
    def __init__(self, parent, placeholder="", show="", width=360, **kw):
        super().__init__(parent, bg=CARD_BG, **kw)
        self._placeholder = placeholder
        self._show        = show
        self._active_show = show
        self._has_focus   = False
        self._width       = width
        self._eye_btn     = None
        self._eye_window  = None
        self._entry_pad_x = 14
        self._entry_pad_y = 23
        self._eye_space   = 36 if show else 0

        self.canvas = tk.Canvas(self, bg=CARD_BG, highlightthickness=0,
                                height=46, width=width)
        self.canvas.pack(fill="x")
        self.canvas.bind("<Configure>", self._on_resize)

        self._rect = round_rect(self.canvas, 1, 1, width - 2, 45, r=10,
                                fill=INPUT_BG, outline=BORDER, width=1)

        self._var = tk.StringVar()
        self.entry = tk.Entry(self.canvas, textvariable=self._var,
                              bg=INPUT_BG, fg=MUTED,
                              insertbackground=ACCENT,
                              relief="flat", bd=0,
                              font=("Helvetica", 12),
                              show="")
        self.entry_win = self.canvas.create_window(
            self._entry_pad_x, self._entry_pad_y,
            anchor="w", window=self.entry,
            width=self._entry_width(width), height=30,
        )

        # placeholder
        self.entry.insert(0, placeholder)
        self.entry.bind("<FocusIn>",  self._on_focus)
        self.entry.bind("<FocusOut>", self._on_blur)
        
        if show:
            self._eye_btn = EyeButton(self.canvas, self)
            self._eye_window = self.canvas.create_window(
                width - 18, 23, anchor="center", window=self._eye_btn
            )

    # ── public API ──────────────────────
    def get(self):
        v = self._var.get()
        return "" if v == self._placeholder else v

    def clear(self):
        self._var.set(self._placeholder)
        self.entry.config(fg=MUTED, show="")
        self._active_show = self._show
        self._set_border(BORDER)

    def set_error(self, is_err):
        self._set_border(ERROR_COL if is_err else (ACCENT if self._has_focus else BORDER))

    def toggle_show(self):
        if not self._show:
            return
        if self._active_show == self._show:
            self._active_show = ""
        else:
            self._active_show = self._show
        if self._var.get() != self._placeholder:
            self.entry.config(show=self._active_show)

    # ── internals ───────────────────────
    def _entry_width(self, total_width):
        available = total_width - self._entry_pad_x - self._eye_space - 10
        return max(available, 80)

    def _rounded_rect_points(self, width, height=46, radius=10):
        x1, y1 = 1, 1
        x2, y2 = max(width - 1, 1), height - 1
        r = radius
        return [
            x1 + r, y1,   x2 - r, y1,
            x2,     y1,   x2,     y1 + r,
            x2,     y2 - r, x2,   y2,
            x2 - r, y2,   x1 + r, y2,
            x1,     y2,   x1,     y2 - r,
            x1,     y1 + r, x1,   y1,
            x1 + r, y1,
        ]

    def _on_resize(self, event):
        width = max(event.width, 1)
        self._width = width
        self.canvas.coords(self._rect, *self._rounded_rect_points(width))
        self.canvas.itemconfig(self.entry_win, width=self._entry_width(width))
        self.canvas.coords(self.entry_win, self._entry_pad_x, self._entry_pad_y)
        if self._eye_window is not None:
            self.canvas.coords(self._eye_window, width - 18, 23)

    def _on_focus(self, _=None):
        self._has_focus = True
        if self._var.get() == self._placeholder:
            self._var.set("")
            self.entry.config(fg=TEXT,
                              show=self._active_show if self._show else "")
        self._set_border(ACCENT)

    def _on_blur(self, _=None):
        self._has_focus = False
        if self._var.get() == "":
            self._var.set(self._placeholder)
            self.entry.config(fg=MUTED, show="")
        self._set_border(BORDER)

    def _set_border(self, color):
        self.canvas.itemconfig(self._rect, outline=color)


# ─────────────────────────────────────────
#  EYE TOGGLE BUTTON
# ─────────────────────────────────────────
class EyeButton(tk.Canvas):
    def __init__(self, parent, entry_widget, **kw):
        super().__init__(parent, width=28, height=28,
                         bg=INPUT_BG, highlightthickness=0, cursor="hand2", **kw)
        self._entry  = entry_widget
        self._open   = True
        self._draw()
        self.bind("<Button-1>", self._toggle)

    def _toggle(self, _=None):
        self._open = not self._open
        self._entry.toggle_show()
        self._draw()

    def _draw(self):
        self.delete("all")
        c = MUTED
        if self._open:
            # eye-open
            self.create_oval(4, 9, 24, 19, outline=c, width=1.5, fill="")
            self.create_oval(10, 11, 18, 17, outline=c, width=1.5, fill="")
        else:
            # eye-closed (slash)
            self.create_oval(4, 9, 24, 19, outline=c, width=1.5, fill="")
            self.create_line(5, 22, 23, 6, fill=c, width=1.5)


# ─────────────────────────────────────────
#  ANIMATED ACCENT BUTTON
# ─────────────────────────────────────────
class AccentButton(tk.Canvas):
    def __init__(self, parent, text, command, **kw):
        super().__init__(parent, height=46, bg=CARD_BG,
                         highlightthickness=0, cursor="hand2", **kw)
        self._text    = text
        self._command = command
        self._hover   = False
        self.bind("<Configure>",  self._draw)
        self.bind("<Enter>",      self._on_enter)
        self.bind("<Leave>",      self._on_leave)
        self.bind("<Button-1>",   self._on_click)

    def _draw(self, _=None):
        self.delete("all")
        w = self.winfo_width() or 360
        fill = "#d4ff70" if self._hover else ACCENT
        round_rect(self, 0, 0, w, 46, r=10, fill=fill, outline="")
        self.create_text(w//2, 23, text=self._text,
                         fill=BG, font=("Helvetica", 13, "bold"))

    def _on_enter(self, _): self._hover = True;  self._draw()
    def _on_leave(self, _): self._hover = False; self._draw()
    def _on_click(self, _): self._command()


# ─────────────────────────────────────────
#  TOAST NOTIFICATION
# ─────────────────────────────────────────
class Toast:
    def __init__(self, root):
        self._root  = root
        self._frame = None
        self._job   = None

    def show(self, msg, kind="success"):
        if self._frame:
            self._frame.destroy()
        if self._job:
            self._root.after_cancel(self._job)

        color = ACCENT if kind == "success" else ERROR_COL

        self._frame = tk.Frame(self._root, bg="#16161f",
                               highlightbackground=color,
                               highlightthickness=1)
        tk.Label(self._frame, text="●", fg=color,
                 bg="#16161f", font=("Helvetica", 8)).pack(side="left", padx=(10, 4), pady=10)
        tk.Label(self._frame, text=msg, fg=color,
                 bg="#16161f", font=("Helvetica", 11)).pack(side="left", padx=(0, 14), pady=10)

        # place at bottom-center
        self._root.update_idletasks()
        fw = self._frame.winfo_reqwidth() + 40
        x  = (W - fw) // 2
        self._frame.place(x=x, y=H - 70)
        self._job = self._root.after(3000, self._hide)

    def _hide(self):
        if self._frame:
            self._frame.destroy()
            self._frame = None

# ─────────────────────────────────────────
#  DASHBOARD WINDOW
# ─────────────────────────────────────────
class Dashboard(tk.Toplevel):
    def __init__(self, parent, fullname, on_logout):
        super().__init__(parent)
        self.title("PyAuth — Dashboard")
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._on_logout = on_logout

        # centre on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - W) // 2
        y = (self.winfo_screenheight() - H) // 2
        self.geometry(f"{W}x{H}+{x}+{y}")

        self._build(fullname)

    def _build(self, fullname):
        # grid background
        bg_cv = tk.Canvas(self, bg=BG, highlightthickness=0)
        bg_cv.place(x=0, y=0, width=W, height=H)
        for i in range(0, W, 40):
            bg_cv.create_line(i, 0, i, H, fill="#13131a", width=1)
        for j in range(0, H, 40):
            bg_cv.create_line(0, j, W, j, fill="#13131a", width=1)

        # card
        card = tk.Frame(self, bg=CARD_BG,
                        highlightbackground=BORDER, highlightthickness=1)
        card.place(x=40, y=120, width=W-80, height=280)

        # accent top bar
        bar = tk.Canvas(card, bg=ACCENT, highlightthickness=0, height=6)
        bar.pack(fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=30, pady=30)

        # avatar circle with initial
        initial = fullname[0].upper()
        av = tk.Canvas(inner, width=64, height=64,
                       bg=CARD_BG, highlightthickness=0)
        av.pack(pady=(0, 16))
        av.create_oval(0, 0, 64, 64, fill=ACCENT, outline="")
        av.create_text(32, 32, text=initial,
                       fill=BG, font=("Helvetica", 26, "bold"))

        # greeting
        tk.Label(inner, text="Welcome back,", fg=MUTED, bg=CARD_BG,
                 font=("Helvetica", 11)).pack()
        tk.Label(inner, text=f"Hi, {fullname} 👋", fg=TEXT, bg=CARD_BG,
                 font=("Helvetica", 20, "bold")).pack(pady=(4, 24))

        # logout button
        AccentButton(inner, "Logout", self._logout).pack(fill="x")

    def _logout(self):
        self.destroy()
        self._on_logout()

# ─────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────
def username_error(u):
    try:
        Validator.validateUsername(u)
        return None
    except ValueError as e:
        return str(e)

def name_error(n):
    try:
        Validator.validateName(n)
        return None
    except ValueError as e:
        return str(e)

def password_error(p):
    try:
        Validator.validatePassword(p)
        return None
    except ValueError as e:
        return str(e)


# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyAuth")
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)
        self.configure(bg=BG)

        # centre on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - W) // 2
        y = (self.winfo_screenheight() - H) // 2
        self.geometry(f"{W}x{H}+{x}+{y}")

        self._toast      = Toast(self)
        self._active_tab = "login"

        self._build_ui()

    # ── UI SKELETON ─────────────────────
    def _build_ui(self):
        # background canvas for subtle grid lines
        bg_canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        bg_canvas.place(x=0, y=0, width=W, height=H)
        for i in range(0, W, 40):
            bg_canvas.create_line(i, 0, i, H, fill="#13131a", width=1)
        for j in range(0, H, 40):
            bg_canvas.create_line(0, j, W, j, fill="#13131a", width=1)

        # card frame
        card = tk.Frame(self, bg=CARD_BG, highlightbackground=BORDER,
                        highlightthickness=1)
        card.place(x=40, y=60, width=W-80, height=H-100)

        # ── brand ──
        brand_row = tk.Frame(card, bg=CARD_BG)
        brand_row.pack(pady=(28, 0))

        icon_cv = tk.Canvas(brand_row, width=32, height=32,
                            bg=CARD_BG, highlightthickness=0)
        icon_cv.pack(side="left", padx=(0, 8))
        round_rect(icon_cv, 0, 0, 32, 32, r=8, fill=ACCENT, outline="")
        icon_cv.create_text(16, 16, text="🔒", font=("Helvetica", 13))

        tk.Label(brand_row, text="Py", fg=TEXT, bg=CARD_BG,
                 font=("Helvetica", 18, "bold")).pack(side="left")
        tk.Label(brand_row, text="Auth", fg=ACCENT, bg=CARD_BG,
                 font=("Helvetica", 18, "bold")).pack(side="left")

        # ── tab switcher ──
        tab_frame = tk.Frame(card, bg=INPUT_BG, padx=4, pady=4)
        tab_frame.pack(fill="x", padx=24, pady=(20, 0))

        self._tab_login    = self._tab_btn(tab_frame, "Login",    "login")
        self._tab_register = self._tab_btn(tab_frame, "Register", "register")
        self._tab_login.pack(side="left", fill="x", expand=True)
        self._tab_register.pack(side="left", fill="x", expand=True)

        # ── page container ──
        self._container = tk.Frame(card, bg=CARD_BG)
        self._container.pack(fill="both", expand=True, padx=24, pady=10)

        self._login_page    = self._build_login(self._container)
        self._register_page = self._build_register(self._container)

        self._show_tab("login")

    def _tab_btn(self, parent, label, tab_id):
        btn = tk.Label(parent, text=label, bg=INPUT_BG, fg=MUTED,
                       font=("Helvetica", 11, "bold"),
                       padx=10, pady=7, cursor="hand2")
        btn.bind("<Button-1>", lambda _: self._show_tab(tab_id))
        return btn

    def _show_tab(self, tab):
        self._active_tab = tab
        # style tabs
        if tab == "login":
            self._tab_login.config(bg=ACCENT, fg=BG)
            self._tab_register.config(bg=INPUT_BG, fg=MUTED)
            self._register_page.pack_forget()
            self._login_page.pack(fill="both", expand=True)
        else:
            self._tab_register.config(bg=ACCENT, fg=BG)
            self._tab_login.config(bg=INPUT_BG, fg=MUTED)
            self._login_page.pack_forget()
            self._register_page.pack(fill="both", expand=True)
        self._clear_errors()

    # ── LOGIN PAGE ───────────────────────
    def _build_login(self, parent):
        frame = tk.Frame(parent, bg=CARD_BG)

        tk.Label(frame, text="Welcome back.", fg=TEXT, bg=CARD_BG,
                 font=("Helvetica", 20, "bold"),
                 anchor="w").pack(fill="x", pady=(16, 2))
        tk.Label(frame, text="Sign in to your account to continue.",
                 fg=MUTED, bg=CARD_BG, font=("Helvetica", 10),
                 anchor="w").pack(fill="x", pady=(0, 18))

        # username
        self._lbl_l_user, self._err_l_user = self._field_label(frame, "USERNAME")
        self._e_l_user = StyledEntry(frame, placeholder="your_username")
        self._e_l_user.pack(fill="x", pady=(0, 4))
        self._err_l_user.pack(fill="x")
        self._bind_clear_on_type(self._e_l_user, self._err_l_user)

        # password
        self._lbl_l_pass, self._err_l_pass = self._field_label(frame, "PASSWORD")
        pw_row = tk.Frame(frame, bg=CARD_BG)
        pw_row.pack(fill="x", pady=(0, 4))
        self._e_l_pass = StyledEntry(pw_row, placeholder="••••••••", show="•")
        self._e_l_pass.pack(side="left", fill="x", expand=True)
        self._err_l_pass.pack(fill="x")
        self._bind_clear_on_type(self._e_l_pass, self._err_l_pass)

        # submit
        tk.Frame(frame, bg=CARD_BG, height=10).pack()
        AccentButton(frame, "Sign In →", self._handle_login).pack(fill="x")

        # divider
        self._divider(frame)

        # switch link
        sw = tk.Frame(frame, bg=CARD_BG)
        sw.pack()
        tk.Label(sw, text="Don't have an account? ", fg=MUTED,
                 bg=CARD_BG, font=("Helvetica", 10)).pack(side="left")
        lnk = tk.Label(sw, text="Create one", fg=ACCENT,
                       bg=CARD_BG, font=("Helvetica", 10, "underline"),
                       cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda _: self._show_tab("register"))

        return frame

    # ── REGISTER PAGE ────────────────────
    def _build_register(self, parent):
        frame = tk.Frame(parent, bg=CARD_BG)

        tk.Label(frame, text="Create account.", fg=TEXT, bg=CARD_BG,
                 font=("Helvetica", 20, "bold"),
                 anchor="w").pack(fill="x", pady=(16, 2))
        tk.Label(frame, text="Fill in the details to get started.",
                 fg=MUTED, bg=CARD_BG, font=("Helvetica", 10),
                 anchor="w").pack(fill="x", pady=(0, 14))

        # first + last name row
        name_row = tk.Frame(frame, bg=CARD_BG)
        name_row.pack(fill="x", pady=(0, 4))

        # first name
        left = tk.Frame(name_row, bg=CARD_BG)
        left.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self._lbl_r_fn, self._err_r_fn = self._field_label(left, "FIRST NAME")
        self._e_r_fn = StyledEntry(left, placeholder="Jane", width=170)
        self._e_r_fn.pack(fill="x")
        self._err_r_fn.pack(fill="x")
        self._bind_clear_on_type(self._e_r_fn, self._err_r_fn)

        # last name
        right = tk.Frame(name_row, bg=CARD_BG)
        right.pack(side="left", fill="x", expand=True)
        self._lbl_r_ln, self._err_r_ln = self._field_label(right, "LAST NAME")
        self._e_r_ln = StyledEntry(right, placeholder="Doe", width=170)
        self._e_r_ln.pack(fill="x")
        self._err_r_ln.pack(fill="x")
        self._bind_clear_on_type(self._e_r_ln, self._err_r_ln)

        # username
        self._lbl_r_user, self._err_r_user = self._field_label(frame, "USERNAME")
        self._e_r_user = StyledEntry(frame, placeholder="jane_doe")
        self._e_r_user.pack(fill="x", pady=(0, 4))
        self._err_r_user.pack(fill="x")
        self._bind_clear_on_type(self._e_r_user, self._err_r_user)

        # password
        self._lbl_r_pass, self._err_r_pass = self._field_label(frame, "PASSWORD")
        pw_row = tk.Frame(frame, bg=CARD_BG)
        pw_row.pack(fill="x", pady=(0, 4))
        self._e_r_pass = StyledEntry(pw_row, placeholder="••••••••", show="•")
        self._e_r_pass.pack(side="left", fill="x", expand=True)
        self._err_r_pass.pack(fill="x")
        self._bind_clear_on_type(self._e_r_pass, self._err_r_pass)

        # submit
        tk.Frame(frame, bg=CARD_BG, height=6).pack()
        AccentButton(frame, "Create Account →", self._handle_register).pack(fill="x")

        # divider
        self._divider(frame)

        # switch link
        sw = tk.Frame(frame, bg=CARD_BG)
        sw.pack()
        tk.Label(sw, text="Already have an account? ", fg=MUTED,
                 bg=CARD_BG, font=("Helvetica", 10)).pack(side="left")
        lnk = tk.Label(sw, text="Sign in", fg=ACCENT,
                       bg=CARD_BG, font=("Helvetica", 10, "underline"),
                       cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda _: self._show_tab("login"))

        return frame

    # ── DASHBOARD ───────────────────────
    def _open_dashboard(self, fullname):
        self.withdraw()
        dash = Dashboard(self, fullname, on_logout=self.deiconify)
        dash.protocol("WM_DELETE_WINDOW", lambda: (dash.destroy(), self.deiconify()))    

    # ── SHARED HELPERS ───────────────────
    def _field_label(self, parent, text):
        lbl = tk.Label(parent, text=text, fg=MUTED, bg=CARD_BG,
                       font=("Helvetica", 8, "bold"), anchor="w")
        lbl.pack(fill="x", pady=(8, 3))
        err = tk.Label(parent, text="", fg=ERROR_COL, bg=CARD_BG,
                       font=("Helvetica", 8), anchor="w")
        return lbl, err

    def _divider(self, parent):
        div = tk.Frame(parent, bg=CARD_BG)
        div.pack(fill="x", pady=14)
        tk.Frame(div, bg=BORDER, height=1).pack(side="left", fill="x",
                                                 expand=True, pady=8)
        tk.Label(div, text="  or  ", fg=MUTED, bg=CARD_BG,
                 font=("Helvetica", 9)).pack(side="left")
        tk.Frame(div, bg=BORDER, height=1).pack(side="left", fill="x",
                                                 expand=True, pady=8)

    def _set_err(self, entry, err_lbl, msg):
        entry.set_error(True)
        err_lbl.config(text=msg)

    def _bind_clear_on_type(self, entry_widget, err_lbl):
        entry_widget.entry.bind(
            "<KeyRelease>",
            lambda _: self._clear_field_error(entry_widget, err_lbl)
        )

    def _clear_field_error(self, entry_widget, err_lbl):
        entry_widget.set_error(False)
        err_lbl.config(text="")

    def _clear_errors(self):
        pairs = [
            (self._e_l_user,  self._err_l_user),
            (self._e_l_pass,  self._err_l_pass),
            (self._e_r_fn,    self._err_r_fn),
            (self._e_r_ln,    self._err_r_ln),
            (self._e_r_user,  self._err_r_user),
            (self._e_r_pass,  self._err_r_pass),
        ]
        for e, lbl in pairs:
            e.set_error(False)
            lbl.config(text="")

    def _clear_login_fields(self):
        self._e_l_user.clear()
        self._e_l_pass.clear()

    def _clear_register_fields(self):
        self._e_r_fn.clear()
        self._e_r_ln.clear()
        self._e_r_user.clear()
        self._e_r_pass.clear()

    # ── HANDLERS ─────────────────────────
    def _handle_login(self):
        self._clear_errors()
        username = self._e_l_user.get()
        password = self._e_l_pass.get()
        ok = True

        username_msg = username_error(username)
        if username_msg:
            self._set_err(self._e_l_user, self._err_l_user, username_msg)
            ok = False
        if not password:
            self._set_err(self._e_l_pass, self._err_l_pass, "Password is required.")
            ok = False
        if not ok:
            return

        status, user = am.login(username, password)
        print(f"Login -> username={username}")

        if status == "User found":
            fullname = user.fullname() if user else username
            self._clear_login_fields()
            self._toast.show("Logged in successfully!", "success")
            self.after(800, lambda: self._open_dashboard(fullname))
        else:
            self._toast.show("Invalid username or password.", "error")


    def _handle_register(self):
        self._clear_errors()
        firstname = self._e_r_fn.get()
        lastname  = self._e_r_ln.get()
        username  = self._e_r_user.get()
        password  = self._e_r_pass.get()
        ok = True

        firstname_msg = name_error(firstname)
        if firstname_msg:
            self._set_err(self._e_r_fn, self._err_r_fn, firstname_msg)
            ok = False
        lastname_msg = name_error(lastname)
        if lastname_msg:
            self._set_err(self._e_r_ln, self._err_r_ln, lastname_msg)
            ok = False
        username_msg = username_error(username)
        if username_msg:
            self._set_err(self._e_r_user, self._err_r_user, username_msg)
            ok = False
        password_msg = password_error(password)
        if password_msg:
            self._set_err(self._e_r_pass, self._err_r_pass, password_msg)
            ok = False
        if not ok:
            return

        status, message = am.register(firstname, lastname, username, password)
        print(f"Register -> {firstname} {lastname}, @{username}")
        if status == "success":
            self._clear_register_fields()
            self._toast.show(message + " Please sign in.", "success")
            self.after(1200, lambda: self._show_tab("login"))
        else:
            self._toast.show(message, "error")

# ─────────────────────────────────────────
if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
