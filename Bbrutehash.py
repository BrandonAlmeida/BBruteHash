#!/bin/python3
import re
import argparse
import hashlib


# Help:        python BBruteHash.py -h
# Example:     python BBruteHash.py -w ./wordlist.txt -a MD5 --hash e2fc714c4727ee9395f324cd2e7f331f


class BBruteHash:
    def __init__(self):
        self.args = self.getArgs()
        self.checkArgs()
        self.hashType = self.getHashType()
        self.exec()

    def exec(self):
        with open(self.args.wordlistpath, "r", encoding="utf-8") as wl:
            for word in wl:
                self.compare(word)

        print(f"No password matches hash `{self.args.hash}`")
        quit()

    def getArgs(self):
        parser = argparse.ArgumentParser(description="Program Description")
        parser.add_argument(
            "-w",
            "--wordlistpath",
            type=str,
            help="Enter the path of the `word list.txt` file",
        )
        parser.add_argument(
            "--hash",
            type=str,
            help="Enter the hash",
        )
        parser.add_argument(
            "-a",
            "--algorithm",
            choices=["MD5", "SHA256", "SHA512", "Yescrypt"],
            type=str,
            help="Choose an algorithm",
        )
        parser.add_argument(
            "-s",
            "--salt",
            type=str,
            help="Enter the salt",
            default=None,
        )

        return parser.parse_args()

    def compare(self, word):
        hashPassword = self.createHashByWord(word)
        if self.args.hash == hashPassword.hexdigest():
            print(f"Password found: {word}")
            quit()

    def createHashByWord(self, word):
        if self.hashType == "MD5":
            return hashlib.md5(word.encode("UTF-8"))
        if self.hashType == "SHA-256":
            return hashlib.sha256(word.encode("UTF-8"))
        if self.hashType == "SHA-512":
            return hashlib.sha512(word.encode("UTF-8"))
        else:
            print("Unknown algorithm")
            quit()

    def checkHashType(self):
        if re.match(r"^\$1\$[a-zA-Z0-9./]{8}\$", self.args.hash):
            return "MD5"
        elif re.match(r"^\$5\$[a-zA-Z0-9./]{16}\$", self.args.hash):
            return "SHA-256"
        elif re.match(r"^\$6\$[a-zA-Z0-9./]{16}\$", self.args.hash):
            return "SHA-512"
        elif re.match(r"^\$y\$[a-zA-Z0-9./]+\$[a-zA-Z0-9./]{16}\$", self.args.hash):
            return "Yescrypt"
        else:
            print("Unknown hash type")
            quit()

    def checkArgs(self):
        if not self.args.wordlistpath:
            print("The --wordlistpath parameter is required")
            quit()
        if not self.args.hash:
            print("The --hash parameter is required")
            quit()
        if not self.args.algorithm:
            print("The --algorithm parameter is required")
            quit()
        if self.args.algorithm == "Yescrypt" and not self.args.salt:
            print("Yescrypt algorithm needs salt parameter")
            quit()

    def getHashType(self):
        return self.args.algorithm if self.args.algorithm else self.checkHashType()


BBruteHash()
