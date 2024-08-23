import pathlib
import os
import shutil
import datetime
import time
import glob
import logging

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.DEBUG,
    datefmt='%H:%M:%S'
)

def get_save_dir():
    save_dir = pathlib.Path.home() / "AppData" / "LocalLow"/ "DefaultCompany" / "Roguelands" 
    return save_dir

def make_backup_dir():
    backups_dir =  pathlib.Path() / "RoguelandsBackups"
    backups_dir.mkdir(exist_ok=True)
    return backups_dir

def load_backup(backups_dir, save_dir):
    logging.info("Loading Backup...")
    logging.info("Available Backups:")
    backups = list(backups_dir.glob("*.txt"))
    for i, backup in enumerate(backups, start=1):
        logging.info(f"{i}. {backup.name}")
    while True:
        choice = input("Enter the number of the backup you want to load: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(backups):
                break
            else:
                logging.info("Invalid choice. Please try again.")
        except ValueError:
            logging.info("Invalid choice. Please try again.")
    backup = backups[choice - 1]
    shutil.copy(backup, save_dir / "PlayerPrefs.txt")
    logging.info("Backup loaded successfully.")

def main():
    logging.info("Welcome to the Roguelands Backup Manager!")
    logging.info("Looking for save directory...")
    save_dir = get_save_dir()
    logging.info("Save directory found at: " + str(save_dir))
    logging.info("making Backup directory...")
    backups_dir = make_backup_dir()
    logging.info("Backup directory created at: " + str(backups_dir))
    logging.info("Making Initial Backup...")
    backupdate =datetime.datetime.now()
    backupname = "PlayerPrefs_"+ backupdate.strftime("%H_%M_%d_%m")  +".txt"
    shutil.copy(save_dir / "PlayerPrefs.txt", backups_dir / backupname )
    logging.info("Initial Backup created at: " + str(backups_dir / backupname))
    while True:
        logging.info("Backup Manager started successfully.")
        try:
            while True:
                do_backup_loop(save_dir, backups_dir)
        except KeyboardInterrupt:
            pass
        while True:
            logging.info("Backup Manager Stopped")
            logging.info("What do you want to do?")
            logging.info("1. Start Backup Manager")
            logging.info("2. Load Backup")
            logging.info("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                logging.info("Starting Backup Manager...")
                break
            elif choice == "2":
                logging.info("Loading Backup...")
                load_backup(backups_dir, save_dir)
                
            elif choice == "3":
                logging.info("Exiting Programm...")
                os._exit(0)
            else:
                logging.info("Invalid choice. Please try again.")
    
        
def do_backup_loop(save_dir, backups_dir):
    files = glob.glob(str(backups_dir) + "/*.txt")
    max_file = max(files, key=os.path.getctime)
    origpreffile = save_dir / "PlayerPrefs.txt"
    if origpreffile.stat().st_mtime > pathlib.Path(max_file).stat().st_mtime:
    # if  os.path.getmtime(save_dir / "PlayerPrefs.txt") > os.path.getmtime(backups_dir / max_file ):
            logging.info("Detected change in save file! Making backup...")
            backupdate =datetime.datetime.now()
            backupname = "PlayerPrefs_"+ backupdate.strftime("%H_%M_%d_%m")  +".txt"
            shutil.copy(save_dir / "PlayerPrefs.txt", backups_dir / backupname )
    else:
        time.sleep(60)
    

main()
