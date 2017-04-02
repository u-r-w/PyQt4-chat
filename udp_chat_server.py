
# UDP Chat Server ini hanya bisa dijalankan di LAN/WIFI dalam satu network 

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
tbl_user = {}

def udp_server() :
  PORT_NUMBER = 1111         #membuat satu port supaya semua menghubungi server ke satu port ini
  SIZE     = 1024
  port     = int(PORT_NUMBER)
  hostName = gethostbyname( '0.0.0.0' )       
  mySocket = socket( AF_INET, SOCK_DGRAM )  # 
  nuser    = 0
  mySocket.bind( (hostName, port) )         # server siap menerima data dari client
  print ("Test server listening on port {0}\n".format(port))
  while True :
    (data,addr) = mySocket.recvfrom(SIZE)   # pak lurah menerima kiriman (data orang/pertanyaan)
    print data
    b = data.split( ':' )                   # pak lurah/server memecah /membedakan antara 
    print( "b ", b )                     
    if( b[0] == "on" ) :                  

      tbl_user[ b[1]] = b[2]
      print( len( tbl_user ) , "t ", tbl_user )
      mystr = ""
      for name in tbl_user :
        mystr = mystr + name + ":" + tbl_user[ name ] + "\n"
      print( "= ", mystr )
      for name in tbl_user  :
        print( "> " + mystr )
        kirim_pesan = mySocket.sendto( mystr ,( tbl_user[name] ,3393))
        
    if( b[0] == "off" ) :
      del( tbl_user[ b[1] ])        # menghapus user yang kirim off dari tabel tbl_user[]
      print( "del ", tbl_user )

      mystr = ""
      for name in tbl_user :                                  # susun semua user yang sedang online ke dalam mystr
        mystr = mystr + name + ":" + tbl_user[ name ] + "\n"
      print( "= ", mystr )
      for name in tbl_user  :                                 # kirim mystr (semua user online) ke semua user
        print( "> " + mystr )
        kirim_pesan = mySocket.sendto( mystr ,( tbl_user[name] ,3393))

udp_server()



