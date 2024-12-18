"""
blocklist.py

This file contains the blocklist of the JWT tokens. It will be imported by the app and 
the logout resource so that tokens can be added ot the blocklist when the user logsout
"""

BLOCKLIST = set()