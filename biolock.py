import GUI
import vault_manager
import fps
import cryptography

mainVault = vault_manager.Vault([], "s")
main_device = fps.FPS()

gui = GUI.GUI(mainVault,main_device)
gui.mainloop()

