from flask import Flask,session
import os

SECRET_KEY = os.urandom(24)