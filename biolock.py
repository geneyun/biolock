import GUI
import vault_manager
import fps
import cryptography

main_vault = vault_manager.Vault([], "s")
main_device = fps.FPS()

gui = GUI.GUI(main_vault, main_device)
gui.mainloop()

