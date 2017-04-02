from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import sys  # We need sys so that we can pass argv to QApplication
import design  # This file holds our MainWindow and all design related things
import os  # For listing directory methods
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from netifaces import interfaces, ifaddresses, AF_INET

gstr  = " "  # dipakai untuk komunikasi antar Class1 dan Class2
gname = " "  

class udp_server( QtCore.QThread ):
    total       = QtCore.pyqtSignal(object)
    update      = QtCore.pyqtSignal()
    PORT_NUMBER = 3393                                    #membuat port
    SIZE        = 1024
    port        = int(PORT_NUMBER)
    mySocket    = socket( AF_INET, SOCK_DGRAM )     
    def __init__(self, parent, n):
        hostName = gethostbyname( '0.0.0.0' )
        self.mySocket.bind( (hostName, self.port) )
        print ("Test server listening on port {0}\n".format(self.port))
        super(udp_server, self).__init__(parent)

    def run(self ):  
        global gstr          
        while True :
          (data,addr) = self.mySocket.recvfrom(self.SIZE) # baca data 
          data        =  data.decode()                    # merubah data menjadi suatu string kata
          print       ( data )
          gstr        = data
          self.update.emit()
    

class ExampleApp( QtGui.QMainWindow, design.Ui_MainWindow ):
    def __init__(self):
        super(self.__class__, self).__init__()
        global gname
        self.setupUi(self)  # mendefinisikan file.py
        self.btnSend.clicked.connect( self.btnSend_di_klik )  # fungsi btnSend_di_klik() dijalankan ketika tombol btnSend diklik
        self.btn_look_ip.clicked.connect( self.lihat_ip )     # cara kerja dari PyQt4 untuk menyambungkan antara object windows dengan fungsi 
        self.online.clicked.connect( self.update_ip_dir )     # buatan kita sendiri adalah dengan cara: clicked.connect()        
        gname       = self.nama_saya.text()                    
        self.lihat_ip()                                              
        self.thread = udp_server(self, 1001  )                # menjalankan udp_server sambil menjalankan variabel di bawah
        self.thread.update.connect(self.update)               # udp_server adalah fungsi yang dijalankan dengan thread berbeda
        self.thread.finished.connect(self.close)              # dari main()
        self.thread.start()

    def update_ip_dir(self ) :
        print ( "ip dir diisi dengan nilai yang diklik", self.online.currentItem().text() )   #memperlihatkan/mencetak IP yg on ke dalam variabel online
        b = self.online.currentItem().text().split(":")  #membedakan/memecah antara nama dan IP dengan parameter/pemisahnya adalah tanda ":"
        self.ip_dir.setText( b[1] )   # mencetak pada kolom ip_dir dengan variabel b yg sudah di split menjadi hanya no IP nya saja


    def update(self):
        global gstr 
#        nstr = self.online.toPlainText()
        oldStr = self.edHasil.toPlainText()  # mencetak data yg telah di kirim ke udp_server 
        if (">" in gstr) :
          self.edHasil.setPlainText( oldStr + "\n" + str(gstr) )
          self.edHasil.moveCursor( QtGui.QTextCursor.End )    # membuat supaya scroll bar ke bawah....tidak keatas
        else :
          #self.online.setPlainText( oldStr + "\n" + str(gstr) )        # tampilkan data 
          d = gstr.split( "\n" )              # memecah daftar online , supaya tidak menyatu semua , dipisahkan dengan enter
          self.online.clear()           
          for a in d :
            self.online.addItem(  a )         # tampilkan data di sebelah kanan yaitu tempat teks daftar online
        
    def btnSend_di_klik( self ) :
        port_number =int( self.port.text())   # membuat kolom daftar port
        ip_addr     =self.ip_dir.text()               # membuat kolom daftar IP

        pesan       =self.edChat.toPlainText()        # membuat kolom untuk mengisi apa yg ingin kita kirim
        print (port_number,ip_addr)

        mySocket = socket( AF_INET, SOCK_DGRAM )
        mystr    = self.nama_saya.text() + ">>  " + self.edChat.toPlainText()  
        bstr     =  str.encode( mystr ) # ['a','b','c'] 
        cstr     = bytes(mystr, "utf-8")
        nama     =  self.nama_saya.text()             # membuat kolom untuk daftar nama
        edtxt    = self.edHasil.toPlainText() + "\n" +  mystr    
        self.edHasil.setPlainText( edtxt ) 
        self.edHasil.moveCursor( QtGui.QTextCursor.End )           #membuat supaya scrollbarnya kebawah
        kirim_pesan=mySocket.sendto( cstr ,(ip_addr,port_number))  #mengirim pesan ke nomor IP yg sudah di tulis di kolom IP

    def get_ip( self ) :                     # fungsi untuk memilih ip kita sendiri dengan...
      for ifaceName in interfaces():     
        a = ifaddresses(ifaceName)         
        if(  2 in a   ) :             
          for b in a[2] :
            if( "192.168." in b['addr'] ) :  # ...dengan prefix 192.168.x.y
              pesan_ip = b['addr']
              return b['addr']

    def lihat_ip( self ):   
        port_server   = 1111                 # membuat 1 port server supaya semuanya menghubungi ke satu port
        ip_server     = "192.168.5.122"      # membuat 1 IP server supaya semuanya menghubungi ke satu port
        SIZE          =  1024
        #metode lama dapat ip tidak jalan di semua komputer    
        for ifaceName in interfaces():
           addresses  = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]           
           self.look_ip.setPlainText( '%s: %s' % (ifaceName, ', '.join(addresses)) )
        mySocket      = socket( AF_INET, SOCK_DGRAM )        
        pesan_ip      = '%s'%(addresses)               
        pesan_ip      = pesan_ip[2:-2]       # membuat IP yg online hanya di cetak dari string yg ke 2  
        pesan_ip      = self.get_ip()        # pesan_ip di isi dengan fungsi get_ip
        self.look_ip.setPlainText( pesan_ip )   
        
        print         ( "ipku ", pesan_ip )
        kirim_nama    = self.nama_saya.text()     # kirim_nama diisi dengan variabel nama_saya
        kstr          = "on:"+kirim_nama             
        kirim_pesan   = mySocket.sendto( bytes(kstr, "utf-8") + bytes(":", "utf-8")  +  bytes(pesan_ip, "utf-8") ,(ip_server,port_server))


def myExitHandler(  ) :
        global gname
        port_server   =1111
        ip_server     ="192.168.5.122"
        SIZE          = 1024
        mySocket      = socket( AF_INET, SOCK_DGRAM )
        kirim_nama    = gname #self.nama_saya.text()
        kstr          = "off:"+kirim_nama         
        kirim_pesan   =mySocket.sendto( bytes(gname, "utf-8")  ,(ip_server,port_server))
        print( "bye ")

def main():
    app   = QtGui.QApplication(sys.argv)        # A new instance of QApplication
    app.aboutToQuit.connect( myExitHandler)     # menjalankan fungsi keluar yg telah di buat oleh python yg referensinya/perintahnya adalah fungsi  myExitHandler
    form  = ExampleApp()                        # mengatur ExampleApp (design)
    form.show()                                 # menampilkan form
    app.exec_()                                 # dan mengeksekusi aplikasi

if __name__== '__main__':  # if we're running file directly and not importing it
    main()                 # menjalankan fungsi main