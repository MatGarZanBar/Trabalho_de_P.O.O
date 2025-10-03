import tkinter as tk
from tkinter import ttk, messagebox, Radiobutton, IntVar
import time
from SanguiFinal_V2 import Paciente, Medico, Tipo_Sang, Transfussao
import os
import datetime
import random


class SistemaSangue:
    
    def __init__(self):
        self.F_PADRAO = ("Comic Sans MS", 20)
        self.F_NEGRITO = ("Comic Sans MS", 20, "bold")
        self.F_GRANDE = (("Comic Sans MS", 32, "bold"))
        self.F_VERMELHO = (("Comic Sans MS", 32, "bold"))
        self.editando_transfusao = False

        self.janela = tk.Tk()
        self.janela.geometry("900x900")
        self.janela.title('Sanguinários Anônimos')

        # Menus
        self.menubar = tk.Menu(self.janela)
        self.menu_arquivo = tk.Menu(self.menubar, tearoff=False)
        self.menu_arquivo.add_command(label="Início", command=self.inicio)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label="Sair", command=self.janela.quit)
        self.menubar.add_cascade(label="Arquivo", menu=self.menu_arquivo)

        self.menu_cadastro = tk.Menu(self.menubar, tearoff=False)
        self.menu_cadastro.add_command(label="Paciente", command=self.tela_paciente)
        self.menu_cadastro.add_command(label="Médico", command=self.tela_medico)
        self.menu_cadastro.add_command(label="Sangue", command=self.tela_sangue)
        self.menu_cadastro.add_separator()
        self.menu_cadastro.add_command(label="Transfussão", command=self.tela_trans)
        self.menu_cadastro.add_separator()
        self.menubar.add_cascade(label="Cadastro", menu=self.menu_cadastro)
        self.janela.config(menu=self.menubar)

        # Frames
        self.frame_inicio = ttk.Frame(self.janela)
        self.frame_paciente = ttk.Frame(self.janela)
        self.frame_medico = ttk.Frame(self.janela)
        self.frame_sangue = ttk.Frame(self.janela)
        self.frame_trans = ttk.Frame(self.janela)
        for frame in (self.frame_inicio, self.frame_paciente, self.frame_medico, self.frame_sangue, self.frame_trans):
            frame.grid(row=0, column=0, sticky='nsew')

        
        self.lb_ola = ttk.Label(self.frame_inicio, text="Bem-vindo ao sistema", font=self.F_GRANDE)
        self.lb_ola.pack(pady=30)
        self.lb_alunos = ttk.Label(self.frame_inicio, text="Você verá as opções acima", font=self.F_PADRAO)
        self.lb_alunos.pack(pady=20)

        
        self.titulo = tk.Label(self.frame_paciente, text='Registro de Paciente', font=self.F_GRANDE, fg="black")
        self.titulo.grid(row=0, column=2, pady=50)
        self.NomePac_Dis = ttk.Label(self.frame_paciente, text='Nome:', font=self.F_PADRAO)
        self.NomePac_Dis.grid(row=1, column=1)
        self.Dt_Nasc_Dis = ttk.Label(self.frame_paciente, text='Data de Nascimento:', font=self.F_PADRAO)
        self.Dt_Nasc_Dis.grid(row=2, column=1, pady=0)
        self.cpf_Dis = ttk.Label(self.frame_paciente, text='CPF:', font=self.F_PADRAO)
        self.cpf_Dis.grid(row=3, column=1, pady=0)

        self.NomePac = ttk.Entry(self.frame_paciente, width=70)
        self.Dt_Nasc = ttk.Entry(self.frame_paciente, width=70)
        self.cpf = ttk.Entry(self.frame_paciente, width=70)
        self.NomePac.grid(row=1, column=2, ipady=5)
        self.Dt_Nasc.grid(row=2, column=2, ipady=5)
        self.cpf.grid(row=3, column=2, ipady=5)

        self.botao_apagar = tk.Button(self.frame_paciente, text='Deletar', font=self.F_NEGRITO, height=1, width=10, command=lambda: self.apagar(self.NomePac, self.Dt_Nasc, self.cpf))
        self.botao_apagar.grid(row=4, column=1, sticky='nsew')
        self.botao_salvar = tk.Button(self.frame_paciente, text='Salvar', font=self.F_NEGRITO, height=1, width=10, bg="#29bd00", command=self.salvar)
        self.botao_salvar.grid(row=5, column=1, sticky='nsew')
        self.botao_excluir = tk.Button(self.frame_paciente, text='Excluir', font=self.F_NEGRITO, height=1, width=10, bg='#ff4242', command=self.excluir)
        self.botao_excluir.grid(row=6, column=1, sticky='nsew')

        self.lista = tk.Listbox(self.frame_paciente, height=50, width=25, bg="white", activestyle='dotbox', font=self.F_PADRAO)
        self.lista.grid(row=4, column=2, rowspan=20, columnspan=1)
        self.lista.bind('<<ListboxSelect>>', self.on_list_select)
        self.pacientes_listaId = []
        for tipo in Paciente.select():
            self.lista.insert(tk.END, tipo.nome_pac)
            self.pacientes_listaId.append(tipo)

        
        self.titulo_m = tk.Label(self.frame_medico, text='Registro de Médicos', font=self.F_GRANDE, fg="black")
        self.titulo_m.grid(row=0, column=2, pady=50)
        self.NomeMed_Dis = ttk.Label(self.frame_medico, text='Nome:', font=self.F_PADRAO)
        self.NomeMed_Dis.grid(row=1, column=1)
        self.Tx_Suc_Dis = ttk.Label(self.frame_medico, text='Taxa de Sucesso:', font=self.F_PADRAO)
        self.Tx_Suc_Dis.grid(row=2, column=1, pady=0)
        self.cpfMed_Dis = ttk.Label(self.frame_medico, text='CPF:', font=self.F_PADRAO)
        self.cpfMed_Dis.grid(row=3, column=1, pady=0)

        self.NomeMed = ttk.Entry(self.frame_medico, width=70)
        self.Tx_Suc = ttk.Entry(self.frame_medico, width=70)
        self.cpfMed = ttk.Entry(self.frame_medico, width=70)
        self.NomeMed.grid(row=1, column=2, ipady=5)
        self.Tx_Suc.grid(row=2, column=2, ipady=5)
        self.cpfMed.grid(row=3, column=2, ipady=5)

        self.botao_apagarM = tk.Button(self.frame_medico, text='Deletar', font=self.F_NEGRITO, height=1, width=10, command=lambda: self.apagar(self.NomeMed, self.Tx_Suc, self.cpfMed))
        self.botao_apagarM.grid(row=4, column=1, sticky='nsew')
        self.botao_salvar_m = tk.Button(self.frame_medico, text='Salvar', font=self.F_NEGRITO, height=1, width=10, bg="#29bd00", command=self.salvar_M)
        self.botao_salvar_m.grid(row=5, column=1, sticky='nsew')
        self.botao_excluir_m = tk.Button(self.frame_medico, text='Excluir', font=self.F_NEGRITO, height=1, width=10, bg='#ff4242', command=self.excluir_M)
        self.botao_excluir_m.grid(row=6, column=1, sticky='nsew')

        self.lista_medico = tk.Listbox(self.frame_medico, height=50, width=25, bg="white", activestyle='dotbox', font=self.F_PADRAO)
        self.lista_medico.grid(row=4, column=2, rowspan=20, columnspan=1)
        self.lista_medico.bind('<<ListboxSelect>>', self.on_list_select_M)
        self.medicos_listaId = []
        for tipo in Medico.select():
            self.lista_medico.insert(tk.END, tipo.nome_med)
            self.medicos_listaId.append(tipo)

        
        self.titulo_s = tk.Label(self.frame_sangue, text='Registro de Sangues', font=self.F_GRANDE, fg="red")
        self.titulo_s.grid(row=0, column=2, pady=50)
        self.TipoSan_Dis = ttk.Label(self.frame_sangue, text='Nome:', font=self.F_PADRAO)
        self.TipoSan_Dis.grid(row=1, column=1)
        self.SangQuantDis = ttk.Label(self.frame_sangue, text='Disponibilidade', font=self.F_PADRAO)
        self.SangQuantDis.grid(row=2, column=1, pady=0)

        self.TipoSang = ttk.Entry(self.frame_sangue, width=70)
        self.TipoSang.grid(row=1, column=2, ipady=5)
        self.var = IntVar()
        self.ComSangue = Radiobutton(self.frame_sangue, text="Disponível", variable=self.var, value=1, command=lambda: self.Dis(True))
        self.ComSangue.grid(row=2, column=2, ipady=5)
        self.SemSangue = Radiobutton(self.frame_sangue, text="Indisponível", variable=self.var, value=0, command=lambda: self.Indis(False))
        self.SemSangue.grid(row=2, column=3, ipady=5)

        self.botao_apagarS = tk.Button(self.frame_sangue, text='Deletar', font=self.F_NEGRITO, height=1, width=10, command=lambda: self.apagar(self.TipoSang))
        self.botao_apagarS.grid(row=4, column=1, sticky='nsew')
        self.botao_salvar_S = tk.Button(self.frame_sangue, text='Salvar', font=self.F_NEGRITO, height=1, width=10, bg="#29bd00", command=self.salvar_S)
        self.botao_salvar_S.grid(row=5, column=1, sticky='nsew')
        self.botao_excluir_S = tk.Button(self.frame_sangue, text='Excluir', font=self.F_NEGRITO, height=1, width=10, bg='#ff4242', command=self.excluir_S)
        self.botao_excluir_S.grid(row=6, column=1, sticky='nsew')

        self.lista_sangue = tk.Listbox(self.frame_sangue, height=50, width=25, bg="white", activestyle='dotbox', font=self.F_PADRAO)
        self.lista_sangue.grid(row=4, column=2, rowspan=20, columnspan=1)
        self.lista_sangue.bind('<<ListboxSelect>>', self.on_list_select_S)
        self.sangues_listaId = []
        for tipo in Tipo_Sang.select():
            self.lista_sangue.insert(tk.END, tipo.tipo_sang)
            self.sangues_listaId.append(tipo)

        
        self.titulo_t = tk.Label(self.frame_trans, text='Registro de Transfussões', font=self.F_GRANDE, fg="red")
        self.titulo_t.grid(row=0, column=2, pady=50)
        self.Pac_Trans = ttk.Label(self.frame_trans, text='Paciente:', font=self.F_PADRAO)
        self.Pac_Trans.grid(row=1, column=1)
        self.Med_Trans = ttk.Label(self.frame_trans, text='Médico:', font=self.F_PADRAO)
        self.Med_Trans.grid(row=2, column=1)
        self.Sang_Trans = ttk.Label(self.frame_trans, text='Sangue:', font=self.F_PADRAO)
        self.Sang_Trans.grid(row=3, column=1)

        self.combobox_tipo_p = ttk.Combobox(self.frame_trans, values=[f"{tipo.id}. {tipo.nome_pac}" for tipo in Paciente.select()])
        self.combobox_tipo_p.grid(row=1, column=2, padx=10, pady=10, sticky="we")
        self.combobox_tipo_m = ttk.Combobox(self.frame_trans, values=[f"{tipo.id}. {tipo.nome_med}" for tipo in Medico.select()])
        self.combobox_tipo_m.grid(row=2, column=2, padx=10, pady=10, sticky="we")
        self.combobox_tipo_s = ttk.Combobox(self.frame_trans, values=[f"{tipo.id}. {tipo.tipo_sang} ({tipo.sang_dispo})" for tipo in Tipo_Sang.select()])
        self.combobox_tipo_s.grid(row=3, column=2, padx=10, pady=10, sticky="we")

        self.botao_salvar_T = tk.Button(self.frame_trans, text='Salvar', font=self.F_NEGRITO, height=1, width=10, bg="#29bd00", command=self.salvar_T)
        self.botao_salvar_T.grid(row=5, column=1, sticky='nsew')
        self.botao_excluir_T = tk.Button(self.frame_trans, text='Excluir', font=self.F_NEGRITO, height=1, width=10, bg='#ff4242', command=self.excluir_T)
        self.botao_excluir_T.grid(row=6, column=1, sticky='nsew')

        self.lista_transfussao = tk.Listbox(self.frame_trans, height=50, width=25, bg="white", activestyle='dotbox', font=self.F_PADRAO)
        self.lista_transfussao.grid(row=4, column=2, rowspan=22, columnspan=5)
        self.lista_transfussao.bind('<<ListboxSelect>>', self.on_list_select_T)
        self.transfussoes_listaId = []
        for tipo in Transfussao.select():
            self.lista_transfussao.insert(tk.END, f"{tipo.paciente_t.nome_pac} ( {tipo.tipo_sang_t.tipo_sang}({tipo.tipo_sang_t.sang_dispo})) ―-― {tipo.medico_t.nome_med}")
            self.transfussoes_listaId.append(tipo)

        self.frame_inicio.tkraise()
        self.janela.mainloop()

    
    def tela_paciente(self):
        self.frame_paciente.tkraise()

    def tela_medico(self):
        self.frame_medico.tkraise()

    def tela_sangue(self):
        self.frame_sangue.tkraise()

    def tela_trans(self):
        self.atualizar_comboboxes()
        self.frame_trans.tkraise()

    def inicio(self):
        self.frame_inicio.tkraise()

    def Dis(self, dispo):
        dispo = True
        return dispo

    def Indis(self, dispo):
        dispo = False
        return dispo

    def atualizar_comboboxes(self):
        tipos_paci = [f"{tipo.id}. {tipo.nome_pac}" for tipo in Paciente.select()]
        self.combobox_tipo_p.configure(values=tipos_paci)
        tipos_med = [f"{tipo.id}. {tipo.nome_med}" for tipo in Medico.select()]
        self.combobox_tipo_m.configure(values=tipos_med)
        tipos_sang = [f"{tipo.id}. {tipo.tipo_sang} ({tipo.sang_dispo})" for tipo in Tipo_Sang.select()]
        self.combobox_tipo_s.configure(values=tipos_sang)

   
    def excluir(self):
        try:
            tamanho2 = self.lista.curselection()
            if tamanho2:
                index = tamanho2[0]
                paciente = self.pacientes_listaId[index]
                pac_eli = Paciente.get(Paciente.id == paciente.id)
                pac_eli.delete_instance()
                self.lista.delete(index)
                del self.pacientes_listaId[index]
                self.NomePac.delete(0, tk.END)
                self.Dt_Nasc.delete(0, tk.END)
                self.cpf.delete(0, tk.END)
                self.botao_salvar.configure(text="Salvar", font=self.F_PADRAO, bg='#29bd00')
            else:
                messagebox.showwarning(title="Calma lá", message="Tá tentando excluir o void do espaço por alg acaso?")
        except Exception as erro:
            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"O MALDITO ERRO: {erro}")
    
    def excluir_M(self):

        try:

            tamanho2 = self.lista_medico.curselection()
            if tamanho2:
                index = tamanho2[0]
                medico = self.medicos_listaId[index]
    

                med_eli = Medico.get (Medico.id == medico.id)
                med_eli.delete_instance()

                self.lista_medico.delete(index)
                del self.medicos_listaId[index]

                self.NomeMed.delete(0, tk.END)
                self.Tx_Suc.delete(0, tk.END)
                self.cpfMed.delete(0, tk.END)

    

                self.botao_salvar.configure(text = "Salvar", font = self.F_PADRAO, bg='#29bd00')

            else:
                messagebox.showwarning(title="Calma lá", message="Tá tentando excluir o void do espaço por alg acaso?")
        except Exception as erro:

            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"O MALDITO ERRO: {erro}")
    
    def excluir_S(self):

        try:

            tamanho4 = self.lista_sangue.curselection()
            if tamanho4:
                index = tamanho4[0]
                sangue = self.sangues_listaId[index]
    

                sang_eli = Tipo_Sang.get (Tipo_Sang.id == sangue.id)
                sang_eli.delete_instance()

                self.lista_sangue.delete(index)
                del self.sangues_listaId[index]

                self.Tipo_Sang.delete(0, tk.END)
            
            

    

                self.botao_salvar_S.configure(text = "Salvar", font = self.F_PADRAO, bg='#29bd00')

            else:
                messagebox.showwarning(title="Calma lá", message="Tá tentando excluir o void do espaço por alg acaso?")



    

    
        except Exception as erro:

            pass
        
    
    def excluir_T(self):

        try:
            selection = self.lista_transfussao.curselection()
            if selection:
                index = selection[0]
            
                transfusoes = list(Transfussao.select())
                transfusao = transfusoes[index]
           
                transfusao.delete_instance()
           
                self.lista_transfussao.delete(index)
            
                self.combobox_tipo_p.set('')
                self.combobox_tipo_m.set('')
                self.combobox_tipo_s.set('')
            else:
                messagebox.showwarning(title="Erro", message="Selecione uma transfusão para excluir.")
        except Exception as erro:
            messagebox.showwarning(title="Erro", message="Erro ao excluir transfusão")
            print(f"Erro ao excluir transfusão: {erro}")



    

   
    def salvar(self):
        try:
            nome_p = self.NomePac.get()
            dt_nsc_p = self.Dt_Nasc.get()
            cpf_p = self.cpf.get()
            if not nome_p or not dt_nsc_p or not cpf_p:
                messagebox.showwarning(title="Erro", message="Tá incompleta essa parada ae")
                return
            pac1 = Paciente.create(nome_pac=nome_p, dt_nasc_pac=dt_nsc_p, cpf_pac=cpf_p)
            self.lista.insert(tk.END, nome_p)
            self.pacientes_listaId.append(pac1)
        except:
            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
    
    def salvar_M(self):

        try:

            nome_M = self.NomeMed.get()
            Tx = self.Tx_Suc.get()
            cpf_Med = self.cpfMed.get()

            if not nome_M or not Tx or not cpf_Med:
                messagebox.showwarning(title="Erro", message="Tá incompleta essa parada ae")
                return

            med1 = Medico.create(nome_med=nome_M, cpf_med=cpf_Med, taxa_suce=Tx)

            print(f"Nome: {nome_M}\nTaxa de Sucesso {Tx}\nCPF: {cpf_Med}")

            tamanho = self.lista_medico.size()
            self.lista_medico.insert(tk.END, nome_M)
            self.medicos_listaId.append(med1)

        except Exception as erro:
            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"Erro ao salvar médico: {erro}")

    def salvar_S(self):

        try:

            TipoSan = self.TipoSang.get()
            Disp = self.var.get()
      

            if not TipoSan:
                messagebox.showwarning(title="Erro", message="Tá incompleta essa parada ae")
                return

            Sang1 = Tipo_Sang.create(tipo_sang=TipoSan, sang_dispo=Disp)

            print(f"Tipo de Sangue: {TipoSan}\nSangue está: ")

            if(Disp == 1):
                print(f"Disponível\n")
        
            elif(Disp == 0):
                print(f"Indisponível\n")
        
            else:
                print(f"Não sei oque vc fez\n")
        

            tamanho = self.lista_sangue.size()
            self.lista_sangue.insert(tk.END, TipoSan)
            self.sangues_listaId.append(Sang1)

        except Exception as erro:
            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"Erro ao salvar sangue: {erro}")
    
    def salvar_T(self):

        try:
            paciente_valor = self.combobox_tipo_p.get()
            medico_valor = self.combobox_tipo_m.get()
            sangue_valor = self.combobox_tipo_s.get()

            if not paciente_valor or not medico_valor or not sangue_valor:
                messagebox.showwarning(title="Erro", message="Selecione paciente, médico e sangue!")
                return

       
            paciente_id = int(paciente_valor.split('.')[0])
            medico_id = int(medico_valor.split('.')[0])
            sangue_id = int(sangue_valor.split('.')[0])

            paciente_box = (paciente_valor.split('.')[1])
            medico_box = (medico_valor.split('.')[1])
            sangue_box = (sangue_valor.split('.')[1])

            transfusao1 = Transfussao.create(
                paciente_t_id=paciente_id,
                medico_t_id=medico_id,
                tipo_sang_t_id=sangue_id,
                data_hora=datetime.datetime.now()
            )
            self.lista_transfussao.insert(tk.END, f"{paciente_box} ({sangue_box}) ―-― {medico_box}")
            self.sangues_listaId.append(transfusao1)


        

     

        except Exception as erro:
            messagebox.showwarning(title="Erro", message="Erro ao salvar transfusão")
            print(f"Erro ao salvar transfusão: {erro}")
    

   
    def on_list_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            paciente = self.pacientes_listaId[index]
            self.NomePac.delete(0, tk.END)
            self.NomePac.insert(0, paciente.nome_pac)
            self.Dt_Nasc.delete(0, tk.END)
            self.Dt_Nasc.insert(0, paciente.dt_nasc_pac)
            self.cpf.delete(0, tk.END)
            self.cpf.insert(0, paciente.cpf_pac)
            self.botao_salvar.configure(text="Editar", font=self.F_PADRAO, bg='lightblue', command=self.editar)
        else:
            self.botao_salvar.configure(text="Salvar", font=self.F_PADRAO, bg='#29bd00', command=self.salvar)
    
    def on_list_select_M(self, event):
        selection = event.widget.curselection()
    
        if selection:
            index = selection[0]
            medico = self.medicos_listaId[index]

        

            self.NomeMed.delete(0, tk.END)
            self.NomeMed.insert(0, medico.nome_med)
        
            self.Tx_Suc.delete(0, tk.END)
            self.Tx_Suc.insert(0, medico.taxa_suce)

            self.cpfMed.delete(0, tk.END)
            self.cpfMed.insert(0, medico.cpf_med)


            self.botao_salvar_m.configure(text = "Editar", font = self.F_PADRAO, bg= 'lightblue', command= self.editar_M)

    
        else:
         
            self.botao_salvar_m.configure(text = "Salvar", font = self.F_PADRAO, bg='#29bd00', command=self.salvar_M)



    def on_list_select_S(self, event):
        selection = event.widget.curselection()
    
        if selection:
            index = selection[0]
            sangue = self.sangues_listaId[index]

        

            self.TipoSang.delete(0, tk.END)
            self.TipoSang.insert(0, sangue.tipo_sang)
        
            self.ComSangue.config(value=True)
       

        


            self.botao_salvar_S.configure(text = "Editar", font = self.F_PADRAO, bg= 'lightblue', command= self.editar_S)

    
        else:
         
            self.botao_salvar_S.configure(text = "Salvar", font = self.F_PADRAO, bg='#29bd00', command=self.salvar_S)

    def on_list_select_T(self, event):
        
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.transfusao = list(Transfussao.select())[index]

       
            for i, tipo in enumerate(Paciente.select()):
                if tipo.id == self.transfusao.paciente_t.id:
                    self.combobox_tipo_p.current(i)
                    break

       
            for i, tipo in enumerate(Medico.select()):
                if tipo.id == self.transfusao.medico_t.id:
                    self.combobox_tipo_m.current(i)
                    break

     
            for i, tipo in enumerate(Tipo_Sang.select()):
                if tipo.id == self.transfusao.tipo_sang_t.id:
                    self.combobox_tipo_s.current(i)
                    break

    
        else:
            self.botao_salvar_T.configure(
                text="Salvar",
                font=self.F_PADRAO,
                bg='#29bd00',
                command=self.salvar_T
            )




    def editar(self):
        try:
            nome_p = self.NomePac.get()
            dt_nsc_p = self.Dt_Nasc.get()
            cpf_p = self.cpf.get()

            print(f"\n--------------------------------\nNome: {nome_p}\nData de Nascimento: {dt_nsc_p}\nCPF: {cpf_p}\n------------------------------------\n")

            tamanho2 = self.lista.curselection()
            if tamanho2:
                index = tamanho2[0]
                paciente = self.pacientes_listaId[index]

                paciente.nome_pac = nome_p    
                paciente.dt_nasc_pac = dt_nsc_p     
                paciente.cpf_pac = cpf_p
                paciente.save()

                self.lista.delete(index)
                self.lista.insert(index, nome_p)
                self.pacientes_listaId[index] = paciente

                self.botao_salvar.configure(text="Salvar", font=self.F_PADRAO, bg='#29bd00', command=self.salvar)
            else:
                messagebox.showwarning(title="Atenção", message="Selecione um paciente para editar.")
        except Exception as erro:
            messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"O MALDITO ERRO: {erro}")
    
    def editar_M(self):




        try:
        

        
            nome_m = self.NomeMed.get()
            Taxa_suces= self.Tx_Suc.get()
            cpf_m = self.cpfMed.get()

        



            print(f"\n--------------------------------\nNome: {nome_m}\nTaxa de Sucesso: {Taxa_suces}\nCPF: {cpf_m}\n------------------------------------\n")

            tamanho3 = self.lista_medico.curselection()
            if tamanho3:
                index = tamanho3[0]
                medico = self.medicos_listaId[index]

        
                medico.nome_med = nome_m    
                medico.taxa_suce = Taxa_suces     
                medico.cpf_med = cpf_m
                medico.save()
       

        
                self.lista_medico.delete(index)
                self.lista_medico.insert((index), nome_m)

        

       


                self.medicos_listaId[index] = medico

                self.botao_salvar_m.configure(text = "Salvar", font = self.F_PADRAO, bg='#29bd00', command=self.salvar_M)
        


        
        
        except Exception as erro:

            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"O MALDITO ERRO: {erro}")

    
    def editar_S(self):




        try:
        

        
            self.TipodeSan = self.TipoSang.get()


        
      

        



            print(f"\n--------------------------------\nTipo de Sangue: {self.TipodeSan}\nTem Disponível: {self.dispo}\n------------------------------------\n")

            tamanho3 = self.lista_sangue.curselection()
            if tamanho3:
                index = tamanho3[0]
                sangue = self.sangues_listaId[index]

        
                sangue.tipo_sang = self.TipodeSan   
                sangue.sang_dispo = self.var.get()    
                sangue.save()
       

        
                self.lista_sangue.delete(index)
                self.lista_sangue.insert((index), self.TipodeSan)

        

       


                self.sangues_listaId[index] = sangue

                self.botao_salvar_S.configure(text = "Salvar", font = self.F_PADRAO, bg='#29bd00', command=self.salvar_S)
        


        
        
        except Exception as erro:

            tk.messagebox.showwarning(title="Erro", message="Insira valores válidos")
            print(f"O MALDITO ERRO: {erro}")
    
    def apagar(x, y = None, z = None):

        try:
            x.delete(0, tk.END)
            y.delete(0, tk.END)
            z.delete(0, tk.END)
        except:
            x.delete(0, tk.END)
    
    def atualizar_comboboxes(self):

   

        tipos_paci = [f"{tipo.id}. {tipo.nome_pac}" for tipo in Paciente.select()]
        self.combobox_tipo_p.configure(values=tipos_paci)

        tipos_med = [f"{tipo.id}. {tipo.nome_med}" for tipo in Medico.select()]
        self.combobox_tipo_m.configure(values=tipos_med)

        tipos_sang = [f"{tipo.id}. {tipo.tipo_sang} ({tipo.sang_dispo})" for tipo in Tipo_Sang.select()]
        self.combobox_tipo_s.configure(values=tipos_sang)




if __name__ == "__main__":
    SistemaSangue()