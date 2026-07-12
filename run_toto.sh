
#!/bin/bash



# ============================================================

# TotoFra Universal Runner (Termux) — Versione Espansa

# ============================================================



ACTION=$1

ARG1=$2

ARG2=$3



# Funzione per mostrare aiuto

show_help() {

    echo "===================================================="

    echo "                 TOTO FRA — COMMANDS"

    echo "===================================================="

    echo ""

    echo "MONDIALE:"

    echo "  ./toto mondiale Squadra1 Squadra2"

    echo "  ./toto m Squadra1 Squadra2"

    echo "  ./toto mondiale_quarti"

    echo "  ./toto mondiale_semifinali"

    echo "  ./toto mondiale_finale"

    echo ""

    echo "LIGUE 1 / SERIE A / PREMIER:"

    echo "  ./toto ligue Squadra1 Squadra2"

    echo "  ./toto seriea Squadra1 Squadra2"

    echo "  ./toto premier Squadra1 Squadra2"

    echo ""

    echo "TENNIS:"

    echo "  ./toto tennis Giocatore1 Giocatore2"

    echo "  ./toto t Giocatore1 Giocatore2"

    echo "  ./toto wimbledon_schedina"

    echo "  ./toto wimbledon_quarti"

    echo "  ./toto wimbledon_semifinali"

    echo "  ./toto wimbledon_finale"

    echo ""

    echo "DASHBOARD:"

    echo "  ./toto dashboard"

    echo ""

    echo "TEST:"

    echo "  ./toto test"

    echo ""

    echo "DIAGNOSTICA:"

    echo "  ./toto path"

    echo "  ./toto ls"

    echo ""

    echo "===================================================="

}



case "$ACTION" in



  # ============================================================

  # MONDIALE

  # ============================================================

  mondiale|m)

    python -c "from worldcup.worldcup_predictor import predict_match; print(predict_match('$ARG1','$ARG2'))"

    ;;



  mondiale_quarti)

    python worldcup/main_worldcup_quarters.py

    ;;



  mondiale_semifinali)

    python worldcup/main_worldcup_phasefinals.py

    ;;



  mondiale_finale)

    python worldcup/main_worldcup_phasefinals_real.py

    ;;



  # ============================================================

  # LIGUE 1 / SERIE A / PREMIER

  # ============================================================

  ligue)

    python -c "from core.predictor import predict_match; print(predict_match('$ARG1','$ARG2'))"

    ;;



  seriea)

    python main_SA.py

    ;;



  premier)

    python main_PL.py

    ;;



  # ============================================================

  # TENNIS

  # ============================================================

  tennis|t)

    python -c "from tennis.tennis_predictor import predict_match; print(predict_match('$ARG1','$ARG2'))"

    ;;



  wimbledon_schedina)

    python -c "from tennis.tennis_schedina_wimbledon_2026 import run_schedina; run_schedina()"

    ;;



  wimbledon_quarti)

    echo "Schedina quarti Wimbledon non ancora creata."

    ;;



  wimbledon_semifinali)

    echo "Schedina semifinali Wimbledon non ancora creata."

    ;;



  wimbledon_finale)

    echo "Schedina finale Wimbledon non ancora creata."

    ;;



  # ============================================================

  # DASHBOARD

  # ============================================================

  dashboard)

    python run_dashboard.py

    ;;



  # ============================================================

  # TEST

  # ============================================================

  test)

    python -m pytest tests/

    ;;



  # ============================================================

  # DIAGNOSTICA

  # ============================================================

  path)

    pwd

    ;;



  ls)

    ls -la

    ;;



  # ============================================================

  # HELP DEFAULT

  # ============================================================

  *)

    show_help

    ;;

esac


