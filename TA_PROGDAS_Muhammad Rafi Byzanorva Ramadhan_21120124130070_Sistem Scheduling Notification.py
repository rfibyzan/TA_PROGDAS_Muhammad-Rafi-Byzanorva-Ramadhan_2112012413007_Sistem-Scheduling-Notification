import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from tkcalendar import Calendar
from plyer import notification
from datetime import datetime


class AppAwal:
    def __init__(self, apk):
        apk.title("Scheduling Notification")
        apk.geometry("300x100")
        apk.resizable(False,False)
        apk.configure(bg="white")

        self.tombol_buka_kalender= ttk.Button(apk,text="Pilih Hari",command=self.BukaKalender)
        self.tombol_buka_kalender.pack(fill="both",expand=True,anchor="center")
        self.menu_agenda = None

        self.Agenda = {}

    def BukaKalender(self):
        Kalender(self)

    def BukaMenuAgenda(self, hari_terpilih, tanggal_terpilih):
        if not self.menu_agenda:
            self.menu_agenda = MenuAgenda(self, hari_terpilih, tanggal_terpilih) 
        else:
            self.menu_agenda.perbarui_tanggal(hari_terpilih, tanggal_terpilih)

class Kalender:
    def __init__(self, main_app):
        self.main_app = main_app
        self.kalender = Toplevel()
        self.kalender.title("Kalender")
        self.kalender.geometry("500x300")
        self.kalender.maxsize(width=750,height=450)
        self.kalender.minsize(width=250,height=300)
        self.kalender.grab_set()
        self.kalender.focus_set()

        TahunIni = datetime.now().year
        BulanIni = datetime.now().month
        HariIni = datetime.now().day

        self.cal = Calendar(self.kalender,selectmode="day",year=TahunIni,month=BulanIni,day=HariIni)
        self.cal.pack(padx=10,fill="both", expand=True)
        
        ButtonSelect = ttk.Button(self.kalender, text="Pilih Hari", command=self.PilihHari)
        ButtonSelect.pack(pady=10)

    def PilihHari(self):
        getter_tanggal = datetime.strptime(self.cal.get_date(),"%m/%d/%y")
        hari_terpilih = getter_tanggal.strftime("%A")
        tanggal_terpilih = getter_tanggal.strftime("%d %B %Y")
        self.kalender.destroy()
        try:
            apk.destroy()
        except:
            pass
        self.main_app.BukaMenuAgenda(hari_terpilih, tanggal_terpilih)
        
class MenuAgenda:
    def __init__(self, menu_agenda, hari_terpilih, tanggal_terpilih):
        
        self.menu_agenda = menu_agenda
        self.hari_terpilih = hari_terpilih
        self.tanggal_terpilih = tanggal_terpilih

        self.MainMenu = tk.Tk()
        self.MainMenu.title("Scheduling Notification")
        self.MainMenu.geometry("960x540")

        self.Label_HariTanggal = ttk.Label(self.MainMenu, text=f"{self.hari_terpilih}, {self.tanggal_terpilih}",font=("Courier New", 30),background="#5191f0",anchor="w")
        self.Label_HariTanggal.pack(padx=10, pady=10, fill="x", side="top", anchor="n")

        self.LabelFrame = ttk.LabelFrame(self.MainMenu, text="Agenda")
        self.LabelFrame.pack(padx=10, pady=10, expand=True, fill="both")

        Tombol_Tambah_Agenda = ttk.Button(self.MainMenu, text="Tambahkan Agenda", command=self.TambahAgenda)
        Tombol_Tambah_Agenda.pack(anchor="w", before=self.LabelFrame, padx=10)

        style = ttk.Style()
        style.configure('elder.TButton', font=20)

        Tombol_Ganti_Tanggal = ttk.Button(self.MainMenu,text="Ganti Tanggal",style="elder.TButton",command=self.GantiTanggal)
        Tombol_Ganti_Tanggal.pack(padx=10, before=self.Label_HariTanggal, anchor="n")

        self.notif()

    def GantiTanggal(self):
        self.menu_agenda.BukaKalender()

    def perbarui_tanggal(self, hari_terpilih, tanggal_terpilih):
        self.hari_terpilih = hari_terpilih
        self.tanggal_terpilih = tanggal_terpilih
        self.Label_HariTanggal.config(text=f"{self.hari_terpilih}, {self.tanggal_terpilih}")
        self.tampilkan_agenda()

    def TambahAgenda(self):
        MenuTambahAgenda(self)

    def tampilkan_agenda(self):
        for widget in self.LabelFrame.winfo_children():
            widget.destroy()
            
        tanggal = self.tanggal_terpilih
        GetAgenda = self.menu_agenda.Agenda.get(tanggal, [])
        
        if GetAgenda:
            for index, item in enumerate(GetAgenda):
                NamaAgenda = item["NamaAgenda"]
                Waktu_str = item["Waktu"].strftime("%H:%M")
                List_agenda = ttk.Button(
                    self.LabelFrame, 
                    text=f"{NamaAgenda}\n{Waktu_str}", 
                    style="Elder.TButton", 
                    command=lambda i=index: self.EditAgenda(i)
                )
                List_agenda.pack(fill="x")

    def EditAgenda(self, index):
        tanggal = self.tanggal_terpilih
        Agenda = self.menu_agenda.Agenda[tanggal]
        EditAgenda(self, Agenda[index])

    def notif(self):
        sekarang = datetime.now()
        for tanggal, daftar_agenda in self.menu_agenda.Agenda.items():
            for agenda in daftar_agenda:
                waktu_agenda = datetime.combine(
                    datetime.strptime(tanggal, "%d %B %Y").date(),
                    agenda["Waktu"].time()
                )
                selisih_waktu = (waktu_agenda - sekarang).total_seconds()
                
                if 599 <= selisih_waktu <= 600 and not agenda.get("notifikasi_terkirim_10_menit", False):
                    notification.notify(
                        title="Sistem",
                        message=f"Agenda: {agenda["NamaAgenda"]}\nakan dimulai 10 menit lagi.",
                        timeout=10
                    )
                    agenda["notifikasi_terkirim_10_menit"] = True 

                if -1 <= selisih_waktu <= 0 and not agenda.get("notifikasi_terkirim_waktu", False):
                    notification.notify(
                        title="Sistem",
                        message=f"Agenda {agenda['NamaAgenda']}\n sudah dimulai!",
                        timeout=10
                    )
                    agenda["notifikasi_terkirim_waktu"] = True  
        self.MainMenu.after(750, self.notif)

class MenuTambahAgenda:    
    def __init__(self, menu_tambah_agenda):
        self.menu_tambah_agenda = menu_tambah_agenda
        
        self.MenuTambahAgenda = Toplevel()
        self.MenuTambahAgenda.title("Tambahkan Agenda")
        self.MenuTambahAgenda.geometry("500x400")
        self.MenuTambahAgenda.maxsize(width=750, height=450)
        self.MenuTambahAgenda.minsize(width=250, height=300)
        self.MenuTambahAgenda.grab_set()
        self.MenuTambahAgenda.focus_set()
        self.MenuTambahAgenda.resizable(False, False)

        Label_Agenda = ttk.Label(self.MenuTambahAgenda, text="Nama Agenda")
        Label_Agenda.pack(padx=10,pady=2, side="top", anchor="w")
        self.Entry_Agenda = ttk.Entry(self.MenuTambahAgenda, textvariable=str)
        self.Entry_Agenda.pack_configure(padx=10,fill="x", anchor="n")
        Label_Catatan = ttk.Label(self.MenuTambahAgenda, text="Catatan")
        Label_Catatan.pack(padx=10,pady=2,side="top", anchor="w")
        self.Entry_Catatan = ttk.Entry(self.MenuTambahAgenda ,textvariable=str)
        self.Entry_Catatan.pack_configure(padx=10, expand=True, fill="both")

        Label_Jam = ttk.Label(self.MenuTambahAgenda, text="Jam")
        Label_Jam.pack(padx=10,pady=2)
        self.Entry_Jam = ttk.Spinbox(self.MenuTambahAgenda, from_=0, to=23)
        self.Entry_Jam.set(0)
        self.Entry_Jam.pack()
        Label_Menit = ttk.Label(self.MenuTambahAgenda, text="Menit")
        Label_Menit.pack(padx=10,pady=2)
        self.Entry_Menit = ttk.Spinbox(self.MenuTambahAgenda, from_=0, to=59)
        self.Entry_Menit.set(0)
        self.Entry_Menit.pack()

        Submit_Entry = ttk.Button(self.MenuTambahAgenda, text="Tambahkan",command=self.tambah_agenda)
        Submit_Entry.pack(pady=3, side="bottom")

    def tambah_agenda(self):
        NamaAgenda = self.Entry_Agenda.get()
        Catatan = self.Entry_Catatan.get()
        Jam = self.Entry_Jam.get()
        Menit = self.Entry_Menit.get()
        Waktu_str = f"{Jam}:{Menit}"
        Waktu = datetime.strptime(Waktu_str,"%H:%M")
        tanggal = self.menu_tambah_agenda.tanggal_terpilih
            
        if NamaAgenda == "":
            messagebox.showerror("Sistem", "Tidak ada nama agenda")
        else:
            if tanggal not in self.menu_tambah_agenda.menu_agenda.Agenda:
                self.menu_tambah_agenda.menu_agenda.Agenda[tanggal] = []
            self.menu_tambah_agenda.menu_agenda.Agenda[tanggal].append({"Waktu": Waktu, "NamaAgenda": NamaAgenda, "Catatan": Catatan, "notifikasi_terkirim_10_menit": False, "notifikasi_terkirim_waktu": False})
            self.menu_tambah_agenda.menu_agenda.Agenda[tanggal].sort(key=lambda x: x["Waktu"])
            messagebox.showinfo("Sistem","Berhasil menambahkan agenda")
            self.menu_tambah_agenda.tampilkan_agenda()
            self.MenuTambahAgenda.destroy()

class EditAgenda:
    def __init__(self, edit_agenda, agenda_item):
        self.edit_agenda = edit_agenda
        self.agenda_item = agenda_item

        self.EditAgenda = Toplevel()
        self.EditAgenda.title("Ubah Agenda")
        self.EditAgenda.geometry("500x400")
        self.EditAgenda.maxsize(width=750, height=450)
        self.EditAgenda.minsize(width=250, height=300)
        self.EditAgenda.grab_set()
        self.EditAgenda.focus_set()
        self.EditAgenda.resizable(False, False)

        Label_Agenda = ttk.Label(self.EditAgenda, text="Nama Agenda")
        Label_Agenda.pack(padx=10, pady=2, side="top", anchor="w")
        self.Entry_Agenda = ttk.Entry(self.EditAgenda)
        self.Entry_Agenda.insert(0, agenda_item["NamaAgenda"])
        self.Entry_Agenda.pack(padx=10, fill="x", anchor="n")
        
        Label_Catatan = ttk.Label(self.EditAgenda, text="Catatan")
        Label_Catatan.pack(padx=10, pady=2, side="top", anchor="w")
        self.Entry_Catatan = ttk.Entry(self.EditAgenda)
        self.Entry_Catatan.insert(0, agenda_item["Catatan"])
        self.Entry_Catatan.pack(padx=10, expand=True, fill="both")

        Label_Jam = ttk.Label(self.EditAgenda, text="Jam")
        Label_Jam.pack(padx=10, pady=2)
        self.Entry_Jam = ttk.Spinbox(self.EditAgenda, from_=0, to=23)
        self.Entry_Jam.set(agenda_item["Waktu"].hour)
        self.Entry_Jam.pack()

        Label_Menit = ttk.Label(self.EditAgenda, text="Menit")
        Label_Menit.pack(padx=10, pady=2)
        self.Entry_Menit = ttk.Spinbox(self.EditAgenda, from_=0, to=59)
        self.Entry_Menit.set(agenda_item["Waktu"].minute)
        self.Entry_Menit.pack()

        Simpan_Perubahan = ttk.Button(self.EditAgenda, text="Simpan Perubahan", command=self.simpan_perubahan)
        Simpan_Perubahan.pack(pady=3,padx=10, side="left")

        Hapus_Agenda = ttk.Button(self.EditAgenda, text="Hapus Agenda",command=self.hapus_agenda)
        Hapus_Agenda.pack(pady=3,padx=10, side="right")

    def simpan_perubahan(self):
        self.agenda_item["NamaAgenda"] = self.Entry_Agenda.get()
        self.agenda_item["Catatan"] = self.Entry_Catatan.get()
        Jam = int(self.Entry_Jam.get())
        Menit = int(self.Entry_Menit.get())
        self.agenda_item["Waktu"] = datetime.strptime(f"{Jam}:{Menit}", "%H:%M")

        messagebox.showinfo("Sistem", "Perubahan berhasil disimpan")
        self.edit_agenda.tampilkan_agenda()
        self.EditAgenda.destroy()

    def hapus_agenda(self):
        pertanyaan = messagebox.askquestion("Sistem", "Agenda akan dihapus, apakah Anda yakin?")
        if pertanyaan == "yes":
            tanggal = self.edit_agenda.tanggal_terpilih
            if tanggal in self.edit_agenda.menu_agenda.Agenda:
                self.edit_agenda.menu_agenda.Agenda[tanggal].remove(self.agenda_item)
                if not self.edit_agenda.menu_agenda.Agenda[tanggal]:
                    del self.edit_agenda.menu_agenda.Agenda[tanggal]

            self.edit_agenda.tampilkan_agenda()

            messagebox.showinfo("Sistem", "Agenda berhasil dihapus")
            self.EditAgenda.destroy()

if __name__ == "__main__":
    apk = tk.Tk()
    app = AppAwal(apk)
    apk.mainloop()