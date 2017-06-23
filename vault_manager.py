import cryptography


class Entry:
    def __init__(self, title, username, password):
        self.title = title
        self.username = username
        self.password = password


    def print_values(self):
        print self.title, self.username, self.password

    def compare_entry(self, entry):
        return self.title == entry.title and self.username == entry.username and self.password == entry.password

    def update_entry(self, new_title, new_username, new_password):
        self.title = new_title
        self.username = new_username
        self.password = new_password


class Vault:
    def __init__(self, entry_list, vault_name):
        self.entry_list = entry_list
        self.vault_name = vault_name
        self.key = None

    def print_all(self):
        for entry in self.entry_list:
            entry.print_values()

    def to_string(self):
        s = ""
        for entry in self.entry_list:
            s = s + entry.title + "," + entry.username + "," + entry.password + ";"
        s = s[:-1]
        return s

    def lock(self,key):
        # self.print_all()
        vault_path = self.vault_name + ".blvf"
        vault_file = open(vault_path, "w")
        encrypted_vault = cryptography.encrypt('BioLockVault:'+self.to_string(),cryptography.hash(key))
        vault_file.write(encrypted_vault)
        vault_file.close()

    def try_unlock(self,key):
        vault_path = self.vault_name + ".blvf"
        vault_file = open(vault_path, "r")
        encrypted_vault = vault_file.read()
        decrypted_vault = cryptography.decrypt(encrypted_vault,cryptography.hash(key))
        vault_file.close()
        return decrypted_vault.startswith('BioLockVault:')

    def unlock(self,key):
        vault_path = self.vault_name + ".blvf"
        vault_file = open(vault_path, "r")
        encrypted_vault = vault_file.read()
        decrypted_vault = cryptography.decrypt(encrypted_vault,cryptography.hash(key))
        vault_file.close()
        entry_list = decrypted_vault[13:].split(";")

        if len(entry_list)>0:
            if len(entry_list[0])>0:
                for entry in entry_list:
                    components = entry.split(",")
                    new_entry = Entry(components[0], components[1], components[2])
                    self.entry_list.append(new_entry)
        # print [entry for entry in self.entry_list]

    def update_name(self, new_name):
        self.vault_name = new_name

    def update_owner(self, new_owner):
        self.owner = new_owner

    def insert(self, entry):
        self.entry_list.append(entry)

    def remove(self, entry):
        for i in self.entry_list:
            if i.compare_entry(entry):
                self.entry_list.remove(i)

    def edit(self, entry_to_change, new_entry):
        for entry in self.entry_list:
            if entry.compare_entry(entry_to_change):
                entry.update_entry(new_entry.title, new_entry.username, new_entry.password)
                break
