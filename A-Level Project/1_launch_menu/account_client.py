#Encrypting a password. My plan is to have every client ship with the same encryption key, away from the server side.
#By the time the password is sent to the server, it should already be encrypted clientside.
from cryptography.fernet import cryptography