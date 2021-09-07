#!/usr/bin/env python3
import subprocess
from urllib.request import urlopen


ip = '192.168.1.123'
port = '1234'
user = 'username'
passwd = 'password'
tracker_url = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'

torrents = []
new_trackers = []
tsm = f'transmission-remote {ip}:{port} -n {user}:{passwd}'

def run_cmd(cmd):
        result = subprocess.getoutput(cmd).splitlines()
        for index, line in enumerate(result):
                result[index] = line.split()
        return result

def get_torrents():
        print(f'Getting list of torrents')
        return run_cmd(f'{tsm} -l')[1:-1]

def get_trackers(torrent):
        print(f'        Getting list of trackers')
        return run_cmd(f'{tsm} -t {torrent} -it')

def get_new_trackers():
        print(f'Fetching trackers from {tracker_url}')
        result = urlopen(tracker_url).read().decode('utf-8').splitlines()
        for index, line in enumerate(result):
                if not len(line):
                        del result[index]
                        continue
        return result

def clear_trackers(torrent):
        print(f'        Clearing trackers...')
        trackers = []
        trackers = get_trackers(torrent)
        for index, tracker in enumerate(trackers):
                if not len(tracker):
                        del trackers[index]
                        continue
                if tracker[0] != "Tracker":
                        del trackers[index]
                        continue
                #print(f'Deleting tracker {tracker[1]} from torrent #{torrent}')
                run_cmd(f'{tsm} -t {torrent} -tr {tracker[1]}[:-1]')

def add_trackers(torrent,new_trackers):
        print(f'        Adding trackers...')
        for tracker in new_trackers:
                run_cmd(f'{tsm} -t {torrent} -td {tracker}')

def main():
        print('')
        torrents = get_torrents()
        new_trackers = get_new_trackers()
        for torrent in torrents:
                print('')
                print(f'Torrent #{torrent[0]}:')
                clear_trackers(torrent[0])
                add_trackers(torrent[0],new_trackers)

if __name__ == "__main__":
        main()
