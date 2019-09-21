#!/bin/bash
if [ "$1" == "-c" ]; then
  echo "converting blackjackBotMainWindow"
  pyuic5 -x blackjackBotMainWindow.ui -o blackjackBotMainWindow.py
  echo "done, starting blackjackBot"
fi
python3 blackjackbotUI.py
