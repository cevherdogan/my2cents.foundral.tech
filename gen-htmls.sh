bash source init-env.sh
python3 ops/md_to_magic_html.py --dirs templates docs ops samples 
python3 ops/md_to_magic_html.py --dirs templates docs ops samples --force

