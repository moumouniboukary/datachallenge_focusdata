@echo off
title FocusEduc - Dashboard Web Streamlit
echo ===============================================================
echo     FOCUSEDUC : SYSTEME D'AIDE A LA DECISION (DEFI 2)
echo ===============================================================
echo Lancement du dashboard web interactif...
cd /d "%~dp0"
streamlit run app.py
pause
