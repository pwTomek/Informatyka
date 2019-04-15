import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from math import atan,pi,sqrt
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import itertools


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title='Wyznaczenie punktu przecięcia dwóch odcinków'
        self.kol1='r'
        self.kol2='blue'
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100,1000,600)
        self.show()
        
    def initWidgets(self):
        #tworzenie przycisków
        oblicz=QPushButton('oblicz',self)
        czysc=QPushButton('zmien kolor prostej AB',self)
        czysc2=QPushButton('zmień kolor prostej CD',self)
        dane=QPushButton('wyczysc dane',self)
        eksportuj=QPushButton('eksportuj dane', self)
        #tworzenie etykiet i edit line'ów
        xa=QLabel('xa',self)
        ya=QLabel('ya',self)
        xb=QLabel('xb',self)
        yb=QLabel('yb',self)
        xc=QLabel('xc',self)
        yc=QLabel('yc',self)
        xd=QLabel('xd',self)
        yd=QLabel('yd',self)
        xp=QLabel('xp',self)
        yp=QLabel('yp',self)
        wsp=QLabel('podaj współrzędne punktów',self)
        WP=QLabel('Punkt P:',self)
        self.xaa=QLineEdit()
        self.yaa=QLineEdit()
        self.xbb=QLineEdit()
        self.ybb=QLineEdit()
        self.xcc=QLineEdit()
        self.ycc=QLineEdit()
        self.xdd=QLineEdit()
        self.ydd=QLineEdit()
        self.xpp=QLineEdit()
        self.ypp=QLineEdit()
        self.pktp=QLineEdit()
        az1=QLabel('azymut AB [grad]:')
        az2=QLabel('azymut CD [grad]:')
        self.azm1=QLineEdit()
        self.azm2=QLineEdit()
        self.DAB=QLineEdit()
        self.DCD=QLineEdit()
        
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        
        #umiejscowienie widżetów
        grid=QGridLayout()
        grid.addWidget(xa,1,0)
        grid.addWidget(self.xaa,1,1)
        grid.addWidget(ya,2,0)
        grid.addWidget(self.yaa,2,1)
        grid.addWidget(xb,1,2)
        grid.addWidget(self.xbb,1,3)
        grid.addWidget(yb,2,2)
        grid.addWidget(self.ybb,2,3)
        grid.addWidget(xc,1,4)
        grid.addWidget(self.xcc,1,5)
        grid.addWidget(yc,2,4)
        grid.addWidget(self.ycc,2,5)
        grid.addWidget(xd,1,6)
        grid.addWidget(self.xdd,1,7)
        grid.addWidget(yd,2,6)
        grid.addWidget(self.ydd,2,7)
        grid.addWidget(wsp,0,0)
        grid.addWidget(oblicz,3,0,2,2)
        grid.addWidget(eksportuj,4,11,2,2)
        grid.addWidget(czysc,2,8,2,2)
        grid.addWidget(czysc2,3,8,2,2)
        grid.addWidget(dane,4,8,2,2)
        grid.addWidget(xp,5,0)
        grid.addWidget(yp,5,4)
        grid.addWidget(WP,4,0)
        grid.addWidget(self.xpp,5,1,1,2)
        grid.addWidget(self.ypp,5,5,1,2)
        grid.addWidget(self.pktp,4,1,1,6)
        grid.addWidget(self.canvas,75,0,-10,-10)
        grid.addWidget(az1,6,0)
        grid.addWidget(az2,7,0)
        grid.addWidget(self.azm1,6,1,1,1)
        grid.addWidget(self.azm2,7,1,1,1)
        dab=QLabel('długosć odc. AB:',self)
        dcd=QLabel('długosć odc. CD:',self)
        grid.addWidget(dab,6,4)
        grid.addWidget(dcd,6,9)
        grid.addWidget(self.DAB,6,5,2,2)
        grid.addWidget(self.DCD,6,10,2,2)
        self.setLayout(grid)
        
        #obsługa sygnał-slot
        oblicz.clicked.connect(self.proste)
        oblicz.clicked.connect(self.azymut)
        czysc.clicked.connect(self.zmienKolor1)
        czysc2.clicked.connect(self.zmienKolor2)
        dane.clicked.connect(self.wyczysc)
        eksportuj.clicked.connect(self.export)
        oblicz.clicked.connect(self.dlugosc)
        
    def wyczysc(self):
        self.xaa.clear()
        self.yaa.clear()
        self.xbb.clear()
        self.ybb.clear()
        self.xcc.clear()
        self.ycc.clear()
        self.xdd.clear()
        self.ydd.clear()
        self.xpp.clear()
        self.ypp.clear()
        self.pktp.clear()
        self.azm1.clear()
        self.azm2.clear()
        self.DAB.clear()
        self.DCD.clear()
        self.figure.clf()
        self.canvas.draw()
        
    def zmienKolor1(self):
        kolor=QColorDialog.getColor()
        if kolor.isValid():
            print(kolor.name())
            self.kol1 = kolor.name()
            self.proste()
    def zmienKolor2(self):
        kolor2=QColorDialog.getColor()
        if kolor2.isValid():
            print(kolor2.name())
            self.kol2=kolor2.name()
            self.proste()
            
            
        
    def proste(self):
        #sprawdzenie czy dane są wartosciami liczbowymi
        xaa=self.sprawdz(self.xaa)
        yaa=self.sprawdz(self.yaa)
        xbb=self.sprawdz(self.xbb)
        ybb=self.sprawdz(self.ybb)
        xcc=self.sprawdz(self.xcc)
        ycc=self.sprawdz(self.ycc)
        xdd=self.sprawdz(self.xdd)
        ydd=self.sprawdz(self.ydd)
        
        

        
        A1='A'
        B1='B'
        C1='C'
        D1='D'
        
        while 1:
            try:
                t1=((xcc-xaa)*(ydd-ycc)-(ycc-yaa)*(xdd-xcc))/((xbb-xaa)*(ydd-ycc)-(ybb-yaa)*(xdd-xcc))
                t2=((xcc-xaa)*(ybb-yaa)-(ycc-yaa)*(xbb-xaa))/((xbb-xaa)*(ydd-ycc)-(ybb-yaa)*(xdd-xcc))
                if (t1>=0 and t1<=1) and (t2>=0 and t2<=1):
                    xP=xaa+t1*(xbb-xaa)
                    yP=yaa+t1*(ybb-yaa)
                    xP=round(xP,3)
                    yP=round(yP,3)
                    self.xpp.setText(str(xP))
                    self.ypp.setText(str(yP))
                    self.pktp.setText('leży na przecięciu prostych')
                    
                elif (t1<0 or t1>1) and (t2<0 or t2>1):
                    xP=xaa+t1*(xbb-xaa)
                    yP=yaa+t1*(ybb-yaa)
                    xP=round(xP,3)
                    yP=round(yP,3)
                    self.xpp.setText(str(xP))
                    self.ypp.setText(str(yP))
                    self.pktp.setText('leży na przedłużeniu odcinków')

                elif (t1<0 or t1>1) and (t2>=0 and t2<=1):
                    xP=xaa+t1*(xbb-xaa)
                    yP=yaa+t1*(ybb-yaa)
                    xP=round(xP,3)
                    yP=round(yP,3)
                    self.xpp.setText(str(xP))
                    self.ypp.setText(str(yP))
                    self.pktp.setText('leży na odcinku CD')  
                 
                elif (t1>=0 and t1<=1) and (t2<0 or t2>1):
                    xP=xaa+t1*(xbb-xaa)
                    yP=yaa+t1*(ybb-yaa)
                    xP=round(xP,3)
                    yP=round(yP,3)
                    self.xpp.setText(str(xP))
                    self.ypp.setText(str(yP))
                    self.pktp.setText('leży na odcinku AB')
                    
                break
            except ZeroDivisionError:
                self.pktp.setText('proste są równoległe')
                yab=[yaa, ybb]
                xab=[xaa, xbb]
                ycd=[ycc, ydd]
                xcd=[xcc, xdd]
                ax=self.figure.add_subplot(111)
                ax.plot(xab,yab, color=self.kol1)
                ax.plot(xcd,ycd, color=self.kol2)
                ax.text(xaa,yaa,A1)
                ax.text(xbb,ybb,B1)
                ax.text(xcc,ycc,C1)
                ax.text(xdd,ydd,D1)
                ax.text(xaa, yaa, 'A  %d,%d' % (int(xaa),int(yaa)))
                ax.text(xbb, ybb, 'B  %d,%d' % (int(xbb),int(ybb)))
                ax.text(xcc, ycc, 'C  %d,%d' % (int(xcc),int(ycc)))
                ax.text(xdd, ydd, 'D  %d,%d' % (int(xdd),int(ydd)))
                ax.text(xpp,ypp, 'P %d,%d' % (int(xpp),int(ypp)))
                self.canvas.draw()
                break
        

        xpp=self.sprawdz(self.xpp)
        ypp=self.sprawdz(self.ypp)
        
        yab=[yaa, ybb]
        xab=[xaa, xbb]
        ycd=[ycc, ydd]
        xcd=[xcc, xdd]
        xap=[xaa, xpp]
        yap=[yaa, ypp]
        xcp=[xcc, xpp]
        ycp=[ycc, ypp]   
         
        ax=self.figure.add_subplot(111)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Położenie prostych')
        ax.plot(xap,yap,'green', linestyle='dashed')
        ax.plot(xcp,ycp, 'green', linestyle='dashed')
        ax.plot(xab,yab, color=self.kol1)
        ax.plot(xcd,ycd, color=self.kol2)
        ax.plot(xaa,yaa,'ro')
        ax.plot(xbb,ybb,'ro')
        ax.plot(xcc,ycc,'bo')
        ax.plot(xdd,ydd,'bo')
        ax.plot(xpp,ypp,'yo')
        ax.text(xaa,yaa,A1)
        ax.text(xbb,ybb,B1)
        ax.text(xcc,ycc,C1)
        ax.text(xdd,ydd,D1)
        ax.text(xaa, yaa, 'A  %d,%d' % (int(xaa),int(yaa)))
        ax.text(xbb, ybb, 'B  %d,%d' % (int(xbb),int(ybb)))
        ax.text(xcc, ycc, 'C  %d,%d' % (int(xcc),int(ycc)))
        ax.text(xdd, ydd, 'D  %d,%d' % (int(xdd),int(ydd)))
        self.canvas.draw()
    

    def sprawdz(self,element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            element.setText('to nie jest liczba')
            return None
        
    def azymut(self):
        
        xaa=self.sprawdz(self.xaa)
        yaa=self.sprawdz(self.yaa)
        xbb=self.sprawdz(self.xbb)
        ybb=self.sprawdz(self.ybb)
        xcc=self.sprawdz(self.xcc)
        ycc=self.sprawdz(self.ycc)
        xdd=self.sprawdz(self.xdd)
        ydd=self.sprawdz(self.ydd)
        
        dxab=xbb-xaa
        dyab=ybb-yaa
        dxcd=xdd-xcc
        dycd=ydd-ycc
        
        if dxab>0 and dyab>0:
            Azab=atan(abs(dyab)/abs(dxab))
        elif dxab<0 and dyab>0:
            Azab=pi-atan(abs(dyab)/abs(dxab))
        elif dxab<0 and dyab<0:
            Azab=pi+atan(abs(dyab)/abs(dxab))
        elif dxab>0 and dyab<0:
            Azab=2*pi-atan(abs(dyab)/abs(dxab))
        elif dxab==0 and dyab>0:
            Azab=2*pi
        elif dxab==0 and dyab<0:
            Azab=pi
        elif dxab>0 and dyab==0:
            Azab=pi/2
        elif dxab<0 and dyab==0:
            Azab=3*pi/2
            
            
        if dxcd>0 and dycd>0:
            Azcd=atan(abs(dycd)/abs(dxcd))
        elif dxcd<0 and dycd>0:
            Azcd=pi-atan(abs(dycd)/abs(dxcd))
        elif dxcd<0 and dycd<0:
            Azcd=pi+atan(abs(dycd)/abs(dxcd))
        elif dxcd>0 and dycd<0:
            Azcd=2*pi-atan(abs(dycd)/abs(dxcd))
        elif dxcd==0 and dycd>0:
            Azcd=2*pi
        elif dxcd==0 and dycd<0:
            Azcd=pi
        elif dxcd>0 and dycd==0:
            Azcd=pi/2
        elif dxcd<0 and dycd==0:
            Azcd=3*pi/2
            
        Azab=round(Azab*200/pi,4)    
        Azcd=round(Azcd*200/pi,4)
        
        self.azm1.setText(str(Azab))
        self.azm2.setText(str(Azcd))
        
    def dlugosc(self):
        
        xaa=self.sprawdz(self.xaa)
        yaa=self.sprawdz(self.yaa)
        xbb=self.sprawdz(self.xbb)
        ybb=self.sprawdz(self.ybb)
        xcc=self.sprawdz(self.xcc)
        ycc=self.sprawdz(self.ycc)
        xdd=self.sprawdz(self.xdd)
        ydd=self.sprawdz(self.ydd)
        
        dxab=xbb-xaa
        dyab=ybb-yaa
        dxcd=xdd-xcc
        dycd=ydd-ycc
        
        dlAB=sqrt(dxab**2+dyab**2)
        dlCD=sqrt(dxcd**2+dycd**2)
        dlAB=round(dlAB,4)
        dlCD=round(dlCD,4)
        
        self.DAB.setText(str(dlAB))
        self.DCD.setText(str(dlCD))
        
    def export(self):
        xpp=float(self.xpp.text())
        ypp=float(self.ypp.text())
        xaa=float(self.xaa.text())
        yaa=float(self.yaa.text())
        xbb=float(self.xbb.text())
        ybb=float(self.ybb.text())
        xcc=float(self.xcc.text())
        ycc=float(self.ycc.text())
        xdd=float(self.xdd.text())
        ydd=float(self.ydd.text())
        DAB=float(self.DAB.text())
        DCD=float(self.DCD.text())
        az1=float(self.azm1.text())
        az2=float(self.azm2.text())
        A2='A'
        B2='B'
        C2='C'
        D2='D'
        P2='P'
        E=open('EksportDanych.txt','w')
        E.write('\n|{:^20}|{:^20}|{:20}|'.format('punkt','X','Y'))
        E.write('\n|{:^20}|{:^20.3f}|{:20.3f}|'.format(P2,xpp,ypp))
        E.write('\n|{:^20}|{:^20.3f}|{:20.3f}|'.format(A2,xaa,yaa))
        E.write('\n|{:^20}|{:^20.3f}|{:20.3f}|'.format(B2,xbb,ybb))
        E.write('\n|{:^20}|{:^20.3f}|{:20.3f}|'.format(C2,xcc,ycc))
        E.write('\n|{:^20}|{:^20.3f}|{:20.3f}|'.format(D2,xdd,ydd))
        E.write('\n')
        E.write(60*'-')
        E.write('\n|{:^20}|{:^20}|{:20}|{:^20}|'.format('długosć AB','Azymut AB','długosć CD', 'Azymut CD'))
        E.write('\n|{:^20.3f}|{:^20.4f}|{:20.3f}|{:^20.4f}|'.format(DAB,az1,DCD,az2))
        E.write('\n')
        E.write(60*'-')
        E.close()
        E.show()

        
def main():
    app=QApplication(sys.argv)
    window=AppWindow()
    app.exec()
    
    
if __name__=='__main__':
    main()
