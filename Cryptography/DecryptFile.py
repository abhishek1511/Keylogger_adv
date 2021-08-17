from cryptography.fernet import Fernet

key = "1lk8ktjhT5YEPccna6wHwtT_aKXu0sEchAdbTlncYmw="

keys_info_e = "e_key_log.txt"
system_information_e = "e_sys_info.txt"
clipboard_info_e = "e_clipboard.txt"

encrypted_files = [keys_info_e, clipboard_info_e, system_information_e]
count = 0

for decrypted_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1