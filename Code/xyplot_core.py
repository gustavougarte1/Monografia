import numpy as np
import matplotlib.pyplot as plt


def prepare_xy_data_from_file(filename,columns=2):
    with open(filename) as f:
        lines = f.readlines()    
        #print(lines)
        x = [line.split()[0] for line in lines]
        try:
            y = [line.split()[1] for line in lines]
        except:
            y = [line.replace("\n","") for line in lines]
            y = [line.split(" ")[1] for line in lines]

            
        if columns==3:
            y2=[line.split()[2] for line in lines]
    for i in range(len(x)):
        x[i]=float(x[i])
    
    for i in range(len(y)):
        try:
            y[i]=float(y[i])
        except:
            print(y[i])
    if columns==3:
        for i in range(len(y2)):    
            y2[i]=float(y2[i])
        return(x,y,y2)
    return(x,y)
  

def sort_depth_value(x,y):
    """x value, y depth"""
    assert len(x)==len(y)
    list1 = [[x[i],y[i]] for i in range(len(x))]
    
    from operator import itemgetter
    list1=sorted(list1, key=itemgetter(0))
    
    x=[item[0] for item in list1]
    y=[item[1] for item in list1]
  
    return(x,y)
       
class my_plot:
    def __init__(self):
        self.x_list=[]
        self.y_list=[]  
        self.c_list=[]
        self.label_list=[]
        self.linewidth=[]
        pass
    
    def load_data(self,filepath,sort=False):
        x,y=prepare_xy_data_from_file(filepath)
        if sort==True:
            x,y=sort_depth_value(x,y)
        return(x,y)
    
    def append_data(self,x,y,c,label,linewidth=2.0):        
        self.x_list.append(x)
        self.y_list.append(y)
        self.c_list.append(c)
        self.label_list.append(label)  
        self.linewidth.append(linewidth)
    
    def construct_plot(self,title,xlabel,ylabel,save=False,xymin=False,xymax=False,figsize=(7,5),scatter=False,vlines=[],xticks_bool=False):
        fig = plt.figure(figsize=figsize)
        ax1 = fig.add_subplot(111)
        ax1.set_title(title)    
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        for i in range(len(self.x_list)):
            if scatter==True:
                ax1.scatter(self.x_list[i],self.y_list[i], c=self.c_list[i], label=self.label_list[i], s=self.linewidth[i])
            else:
                ax1.plot(self.x_list[i],self.y_list[i], c=self.c_list[i], label=self.label_list[i], linewidth=self.linewidth[i])
        if xticks_bool==True:
            plt.xticks(np.arange(0,900,63), ["6/2004","9/2004","12/2004","3/2005","6/2005","9/2005","12/2005","3/2006","6/2006","9/2006","12/2006","3/2007","6/2007","9/2007"], rotation=60)
        
        for line in vlines:
            plt.axvline(x=line,color="k")
        
        #ax1.plot(y,x, c='r', label='Mean T depth profile, Viscoplasticity - case 1', linewidth=1.0)
        leg = ax1.legend()
        if xymin!=False:
            ax1.set_xlim(xmin=xymin[0])
            ax1.set_ylim(ymin=xymin[1])
        if xymax!=False:
            ax1.set_xlim(xmax=xymax[0])
            ax1.set_ylim(ymax=xymax[1])
        if save!=False:    
            fig.savefig("img\\"+save,format="png",dpi=200,bbox_inches='tight')
        return(ax1,fig)


def logarithmic(x):
    for i in range(len(x)):
        if x[i]<=0:
            x[i]=1e-10
        x[i]=math.log10(x[i])
    return(x)

