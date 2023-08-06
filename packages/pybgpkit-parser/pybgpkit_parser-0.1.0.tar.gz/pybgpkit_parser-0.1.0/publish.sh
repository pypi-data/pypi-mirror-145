#!/bin/bash 

maturin publish --interpreter python3.6 --skip-existing  && \\
maturin publish --interpreter python3.7 --skip-existing  && \\
maturin publish --interpreter python3.7 --skip-existing  && \\
maturin publish --interpreter python3.9 --skip-existing  && \\
maturin publish --interpreter python3.9 --skip-existing  && \\
maturin publish --interpreter python3.9 --skip-existing  && \\
maturin publish --interpreter python3.10 --skip-existing 
