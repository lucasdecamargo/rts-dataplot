########################################################################################
# Esse script eh feito para as atividades de escalonamento em tempo real
# Voce deve executar o teu codigo do epos como abaixo:
# $ make APPLICATION=rt_rm run > rt_rm_output
# Isso ira gerar um arquivo com a saida da aplicacao de teste fornecida pelo professor.
# O mesmo pode ser feito com EDF
# Olhe a main deste codigo la em baixo. Eh bem intuitiva.
# --------------------------------------------------------------------------------------
# Autor: Lucas de Camargo Souza
########################################################################################

import matplotlib.pyplot as plt

class OutputData:
    def __init__(self):
        self.data = []

    def getData(self):
        x = []
        y = []
        for d in self.data:         
            if(d[1] == 'a'):
                x.append(d[0])
                y.append(3)
            elif(d[1] == 'b'):
                x.append(d[0])
                y.append(2)
            elif(d[1] == 'c'):
                x.append(d[0])
                y.append(1)
        return x,y

    def exportFile(self, fname, mode=0):
        if(mode == 0):
            x,y = self.getData()
            with open(fname, 'w') as f:
                f.write(str(x))
                f.write('\n')
                f.write(str(y))
        elif(mode == 1):
            with open(fname, 'w') as f:
                f.write(str(self.data))


# Use esta classe para um arquivo de saida do tipo:
# 0 C
# 1 C
# 2 A
# ...
class OutputFile(OutputData):
    def __init__(self,fname):
        super().__init__()
        self.fname = fname
        self.crop()

    def crop(self):
        output = []
        with open(self.fname,'r') as f:
            while(True):
                line = f.readline()
                
                if(line == ""):
                    break

                lnumber,sep,temp = line.partition("  ")
                if(len(temp)>1):
                    thread,sep,temp = temp.partition("  ")
                else:
                    thread = temp

                if(lnumber.isdigit() and thread[0].isalpha()):
                    self.data.append((int(lnumber),thread[0]))



# Use esta classe para um arquivo de saida puro e.g.
# make APPLICATION=rt_edf run > arquivo_saida_puro
class OutputRawFile(OutputData):
    def __init__(self, fname):
        super().__init__()
        self.fname = fname
        self.crop()

    def crop(self):
        output = []
        with open(self.fname,'r') as f:
            while(True):
                line = f.readline()
                
                if(line == ""):
                    print("Inconsistent File!")
                    raise EOFError

                if(line.find("Threads will now be created and I'll wait for them to finish...") != -1):
                    break

            f.readline()

            while(True):
                line = f.readline()

                if(line == ""):
                    print("Inconsistent File!")
                    raise EOFError
                
                if(line.find("... done!") != -1):
                    break

                lnumber,sep,temp = line.partition('\t')
                thread,sep,temp = temp.partition('\t')
                if(lnumber.isdigit() and thread.isalpha()):
                    self.data.append((int(lnumber),thread))


class MatPlotter:
    def __init__(self):
        self.data = []
        plt.rcParams.update({'font.size': 20})
        plt.rcParams['figure.constrained_layout.use'] = True

    def add_data(self, data, label : str = ""):
        self.data.append((data,label))

    def plot(self, x_i=0, x_s=0):
        if(len(self.data) ==  1):
            if(x_s != 0):
                plt.xlim(x_i,x_s)
            plt.plot(self.data[0][0][0],self.data[0][0][1], 'r.')
            plt.ylabel(self.data[0][1])
            plt.grid(b=True, which='major', color='#909090', linestyle='-')
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

        elif(len(self.data) ==  2):     
            f, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
            ax1.plot(self.data[0][0][0],self.data[0][0][1], 'r.')
            ax1.set_ylabel(self.data[0][1])
            ax1.grid(b=True, which='major', color='#909090', linestyle='-')
            ax1.minorticks_on()
            ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

            ax2.plot(self.data[1][0][0],self.data[1][0][1], 'b.')
            ax2.set_ylabel(self.data[1][1])
            ax2.grid(b=True, which='major', color='#909090', linestyle='-')
            ax2.minorticks_on()
            ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.3)

            if(x_s != 0):
                ax1.set_xlim(x_i,x_s) 
                ax2.set_xlim(x_i,x_s)

        plt.yticks((1,2,3),('c','b','a'))        
        MatPlotter.maximize()

    def show(self):
        plt.show()

    def maximize():
        plot_backend = plt.get_backend()
        mng = plt.get_current_fig_manager()
        if plot_backend == 'TkAgg':
            mng.resize(*mng.window.maxsize())
        elif plot_backend == 'wxAgg':
            mng.frame.Maximize(True)
        elif plot_backend == 'Qt4Agg':
            mng.window.showMaximized()
        elif plot_backend == 'Qt5Agg':
            mng.window.showMaximized()

if __name__=="__main__":    
    f_rm = OutputRawFile("rt_rm_output")
    f_edf = OutputRawFile("rt_edf_output")

    plot = MatPlotter()

    # Voce pode dicionar um ou dois arquivos no mesmo grafico.
    # Nao implementei pra mais que 2!
    plot.add_data(f_rm.getData(),"RM")
    plot.add_data(f_edf.getData(),"EDF")
    
    plot.plot(0,500)
    plot.show()

    plot.plot(5800,6300)
    plot.show()

    plot.plot(7800,8300)
    plot.show()
