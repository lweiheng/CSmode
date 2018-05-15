import socket
host = '127.0.0.1'
port = 9999

def readFile(filename):
    '''
    :param filename:
    :return:
    '''
    with open(file=filename) as f:
        data = f.read()
        data = data.rstrip()
        return data


def writeFile(filename, data):
    '''
    :param filename:
    :param data:
    :return:
    '''
    data = bytes(data, 'utf-8')
    with open(file=filename) as f:
        result = f.write(data)
        return result

def excFileCommand(conn):
    '''
    :param conn:
    :return:
    '''

    hello = conn.recv(4096)
    print(str(hello, 'utf-8'))

    # input and send the filename
    filename = input("FileName:")
    conn.send(filename.encode())

    # read and send the data
    filedata = readFile(filename)
    conn.send(bytes(str(len(filedata)), 'utf-8'))
    conn.sendall(bytes(filedata, 'utf-8'))

def main():
    '''
    :return:
    '''
    sock = socket.socket()
    print("Socket Created...")
    sock.bind((host, port))
    #while 1:
    sock.listen(10)

    while 1:
        conn, addr = sock.accept()
        print(conn)
        print(addr)
        while 1:

            # input and send the command
            command = input('>>>')
            if command == 'break': break
            conn.send(command.encode())

            # exc file command
            if command == 'Send File':
                excFileCommand(conn)
                continue
            # rev the response date' length
            rev_len = conn.recv(4096)
            rev_len = int(str(rev_len, 'utf-8'))
            print('rev_len:' + str(rev_len))

            # rev the response data
            rev_answer = bytes()
            while len(rev_answer) != rev_len:
                data = conn.recv(1024)
                rev_answer += data
            rev_answer = str(rev_answer, 'utf-8')
            print(rev_answer)


        conn.close()

if __name__ == '__main__':
    main()