#!/data/data/com.termux/files/usr/bin/bash

# Avvia Pydroid 3
am start -n ru.iiec.pydroid3/.MainActivity

# Attendi che l'app sia pronta
sleep 2

# Esegui TotoFra
input text "python /storage/emulated/0/totofra/main.py"
input keyevent 66
