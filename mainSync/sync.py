#Backuper έκδοση 1.0.1 Κωνσταντίνος Καρακασίδης

from dirsync import sync
import configparser
import os



def main():
    paths = 'options.cfg'
    if os.path.isfile(paths):

        config = configparser.ConfigParser()
        config.read(paths)
        source_path = config.get('DEFAULT','source')
        target_path = config.get('DEFAULT','target')
        option = 'sync'

        sync(r'{}'.format(source_path), r'{}'.format(target_path), option, verbose=True, purge=True) #for syncing one way + purge

    else:
        print(f'Δεν βρέθηκε το {paths}')


if __name__=="__main__":
    main()