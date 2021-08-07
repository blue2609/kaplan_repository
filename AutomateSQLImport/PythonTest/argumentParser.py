import argparse

# help flag provides flag help
# store_true actions stores argument as True

parser = argparse.ArgumentParser()
parser.add_argument('--folderName',required=True,help="specify folder name")
args = parser.parse_args()

print(f'Hello {args.foldername}')
