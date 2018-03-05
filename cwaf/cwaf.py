#/usr/bin/env python3
import string
import re
import requests
import urllib
import titles
import MyTable
import random
import time
import sys
import argparse
import os
import socket
from col import Colours as c 

#globally set variables
is_target = None	# if argparsed or manually inputted set var to 1
user_target = None
title_shown = 0

verbose_mode = False

options = ["target(s)", "nms", "wafw00f", "cwaf"]

def show_options():
	print("""
	1 - set target, url or ipv4 addr to detect waf
	2 - advanced nmap script against target
	3 - wafw00f detection against target
	4 - cwaf against target
	clear (or c) - clear screen
	options (or o) - show options
	help (or h) - also shows options
	quit (or q) - quit program
	""")

def error_input():
	os.system("clear")
	print(c.red, end="")
	print("\n"*8)
	print("[READ] Enter either 1, 2 or 3 in order to run the deisred method to detect a waf.")
	print(c.end, end="")
	time.sleep(3.8)
	os.system("clear")
	show_menu()

def show_title():
	print(c.lightgrey, end="")
	print(titles.Title(), end="")
	print(c.end)
	global title_shown; title_shown = 1

def show_menu():
	menu = MyTable.Table(options, 2)
	menu.colour(border=c.lightgrey, number=c.red, text=c.darkgrey)
	menu.style("|", "~", "#")
	menu.make_table()

def user_selection():
	valid_input = 0
	invalid_input = 0
	while valid_input != 1:
		user_input = input("cwaf-opt-> ")
		#if user input is return key
		if user_input == "":
			invalid_input += 1
			if invalid_input == 7:
				sys.exit(0)
			print(c.red, end="")
			if invalid_input < 7:
				print("[E:] Enter a number which corresponds to your desired option.", c.end)
			if invalid_input % 3 == 0:
				error_input()
		elif user_input == "1":
			if is_target == 1:
				target(user_target)
			else: target()
		elif user_input == "2":
			nms(user_target)
			valid_input = 1
		elif user_input == "3":
			wafw00f(user_target)
			valid_input = 1
		elif user_input == "4":
			cwaf(user_target)
			valid_input = 1
		elif user_input[0] in ["c", "C"]:
			os.system("clear")
		elif user_input[0] in ["o", "O", "h", "H"]:
			os.system("clear")
			show_options()
		elif user_input[0] in ["m", "M"]:
			os.system("clear")
			show_menu()
		elif user_input[0] in ["q", "Q"]:
			break
		elif user_input[0] in ["t", "T"]:
			print("target(s) currently set as: {}{}{}".format(c.red, user_target, c.end))
		else: 
			invalid_input += 1
			if invalid_input == 7:
				sys.exit(0)
			print(c.red, end="")
			if invalid_input < 7:
				print("[E:] Enter a number which corresponds to your desired option.", c.end)
			if invalid_input % 3 == 0:
				error_input()

def target(*args):
	#   improve to see whether user list input validates ipv4 and urls
	#   better yet write a module which will validate the target input
	#   to ensure that it meets all criteria 
	global is_target
	extensions = ["org", "com", "net", "fr"]
	# write a file somewhere in the file system, to determine whether this program has been used before
	# if it has, then dont show the prompt (how to parse multiple targets)
	if os.path.exists("./.chk"):
		global verbose_mode
		if verbose_mode == True:
			print(c.cyan)
			print("[In order to add multiple targets, simply add a target separated by a comma and a space.]")
			print("e.g. example.com, something.com, somewhere.com || 192.168.44.33, books.org, 22.22.22.42")
			print(c.end)
		else: pass
	else:
		chk = open("./.chk", "w")
		chk.write("y\n")
		print(c.cyan)
		print("[In order to add multiple targets, simply add a target separated by a comma and a space.]")
		print("e.g. example.com, something.com, somewhere.com || 192.168.44.33, books.org, 22.22.22.42")
		print(c.end)
	global user_target
	is_set = 0
	if len(args) < 1:
		if is_set != 1:
			while is_set != 1:
				target = input("set-target-> ")
				if target in ["b", "B", "q", "Q"]:
					return None
				if (target == "") or ("." not in target):
					print(c.red, end="")
					print("you must enter a target, (URL or IPv4) e.g. target.com or 192.168.88.776", c.end)
					continue
				if target[0] in str([1,2,3,4,5,6,7,8,9,0]):
					if len(target)<9:
						print(c.red, end="")
						print("invalid ipv4", c.end)
						continue
	#condition used to check whether the input target address has 3 periods, and is greater than len of 9
					if  target.count(".")!=3:
						print(c.red, end="")
						print("invalid ipv4", c.end)
						continue
					is_set = 1
					is_target = 1
					continue
				else:
					is_set = 1
					is_target = 1
			if is_set == 1:
				if "," in target:
					user_target = []
					targets = target.split(", ")
					for t in targets:
						if t[0] in string.digits:
							if len(t) < 9:
								print(c.red, end="")
								print("problem with {}".format(t), c.end)
								continue
							if t.count(".")!=3:
								print(c.red, end="")
								print("problem with {}".format(t), c.end)
								continue
							else:
								user_target.append(t)
						elif "." not in t:
							print(c.red, end="")
							print("problem with: {}".format(t), c.end) 
						else:
							user_target.append(t)
				else: user_target = target
			else: pass
	else:
		print("~> target(s) already set to {}{}{};".format(c.red, args[0], c.end), end=" ")
		print("are you sure you want to change this [n]? ", end=" ")
		y_or_n = input()
		if y_or_n == "":
			return None
		elif y_or_n[0] in ["n", "N", "x", "X", "c", "C"]:
			return None
		elif y_or_n in ["y", "Y"]:
			while is_set != 1:
				target = input("set-target-> ")
				if target in ["b", "B", "q", "Q"]:
					user_target = args[0]
					return None
				if (target == "") or ("." not in target):
					print(c.red, end="")
					print("you must enter a target, (URL or IPv4) e.g. target.com or 192.168.88.776", c.end)
					continue
				if target[0] in str([1,2,3,4,5,6,7,8,9,0]):
					if len(target)<9:
						print(c.red, end="")
						print("invalid ipv4", c.end)
						continue
					if  target.count(".")!=3:
						print(c.red, end="")
						print("invalid ipv4", c.end)
						continue
					is_set = 1
					is_target = 1
					continue
				else:
					is_set = 1
					is_target = 1
			if is_set == 1:
				if "," in target:
					user_target = []
					targets = target.split(", ")
					for t in targets:
						if t[0] in string.digits:
							if len(t) < 9:
								print(c.red, end="")
								print("problem with {}".format(t), c.end)
								continue
							if t.count(".")!=3:
								print(c.red, end="")
								print("problem with {}".format(t), c.end)
								continue
							else:
								user_target.append(t)
						elif "." not in t:
							print(c.red, end="")
							print("problem with: {}".format(t), c.end) 
						else:
							user_target.append(t)
				else: user_target = target
			else: pass
	if len(target) > 2:
		print("~> target set to {}{}{}".format(c.red, user_target, c.end))
	return None

def nms(target):
	print(target)

def wafw00f(target):
	print(target)

def cwaf(target):
	print(target)

def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	parser.add_argument("--output", "-o", required=False, 
		help="output results in a text file")
	parser.add_argument("--verbose", "-v", 
		help="increase output verbosity", action="store_true")
	parser.add_argument("--proxy", "-p", type=str, required=False, 
		help="specify a proxy server and port you would like to connect to (if you're using cwaf [opt:4])\
		--proxy=\"172.443.26.26:8080\"")
	parser.add_argument("--cwaf", action="store_true", 
		help="initiate a cwaf detection scan without going through UI")
	group.add_argument("--target", "-t", required=False, type=str, 
		help="specify a target URL or IPv4 address")
	group.add_argument("--targetfile", "-tf", required=False, 
		help="specify a file with list of targets, which are separated by newline characters")
	arg = parser.parse_args()		

	if arg.target:
		global is_target; is_target = 1
		global user_target;
		if "," in arg.target:
			targets = arg.target.split(", ")
			user_target = targets
		else: 
			user_target = arg.target

	if arg.targetfile:
		target_list = []
		with open(arg.targetfile, "r") as tf:
			for target in tf.readlines():
				target_list.append(target.strip("\n"))
		user_target = target_list

	if arg.verbose:
		global verbose_mode
		verbose_mode = True

	if arg.output:
		#write output to output file
		pass 

	if arg.proxy:
		#split by ":" to verify host and port
		pass

	if arg.cwaf:
		pass

	if title_shown == 0:
		show_title()
	show_menu()
	user_selection()

if __name__ == "__main__":
	main()  
