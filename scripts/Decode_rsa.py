import argparse

parser = argparse.ArgumentParser(description="Decode RSA")
parser.add_argument("file", help="The file containing the encrypted text")
parser.add_argument("d", help="The Private Key", type=int)
parser.add_argument("n", help="The Modulus", type=int)
args=parser.parse_args()

with open(args.file, "r") as coded:
    data = [int(i.strip("\n")) for i in coded.read().split(" ")]

for i in data:
    print(chr(i**args.d % args.n), end="")
