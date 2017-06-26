import GUI
import vault_manager
import fps

# creates main vault and main device as global variables, so that they could be used by the entire program
main_vault = vault_manager.Vault([], "s")
main_device = fps.FPS()

# sets up GUI
gui = GUI.GUI(main_vault, main_device)
gui.mainloop()

