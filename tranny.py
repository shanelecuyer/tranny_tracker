#!/usr/bin/env python3
import sys
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

def search_torrents(arg,torrents):
        for count, torrent in enumerate(torrents, start=1):
                print(f'Searching for \"{arg}\" [{count}/{len(torrents)}]', end='\r')
                if arg in torrent[8]:
                        print('')
                        print(f'Found: {torrent[8]}')
                        return(torrent[0])
                        break
        else:
                print('')
                print(f'Error: \"{arg}\" not found in torrent list')

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
        trackers = []
        filtered_trackers = []
        trackers = get_trackers(torrent)
        for index, tracker in enumerate(trackers):
                tracker = tracker[:-1]
                if not len(tracker) or tracker[0] != "Tracker":
                        del trackers[index]
                        continue
                else:
                        filtered_trackers.append(tracker[1][:-1])
                        continue
        for count, tracker in enumerate(filtered_trackers, start=1):
                print(f'Deleting tracker {count} of {len(filtered_trackers)}', end='\r')
                run_cmd(f'{tsm} -t {torrent} -tr {tracker}')

def add_trackers(torrent,new_trackers):
        for count, tracker in enumerate(new_trackers, start=1):
                print(f'Adding tracker {count} of {len(new_trackers)}', end='\r')
                run_cmd(f'{tsm} -t {torrent} -td {tracker}')

def main():
        print('')
        if len(sys.argv) > 2:
                print('Error: Too many arguments')
        elif len(sys.argv) == 2:
                arg = sys.argv[1]
                torrents = get_torrents()
                search_result = search_torrents(arg, torrents)
                if search_result:
                        print('')
                        new_trackers = get_new_trackers()
                        print('')
                        clear_trackers(search_result)
                        print('')
                        add_trackers(search_result,new_trackers)
                        print('')
                        print('')
                        print('Done')
        else:
                torrents = get_torrents()
                new_trackers = get_new_trackers()
                for count, torrent in enumerate(torrents, start=1):
                        print('')
                        print(f'Torrent #{torrent[0]} ({count}/{len(torrents)}):')
                        clear_trackers(torrent[0])
                        print('')
                        add_trackers(torrent[0],new_trackers)
                        print('Done')

if __name__ == "__main__":
        main()
