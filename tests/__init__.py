""" Init module to add source directory to the tests path environment"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/")))
