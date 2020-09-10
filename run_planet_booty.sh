source venv/bin/activate

# PYTHONPATH=src python src/interactive_conditional_samples.py --top_p 40 --temperature 1.618 --nsamples 1 --seed 42 run1
PYTHONPATH=src python src/generate_unconditional_samples.py --top_p 40 --temperature 1.618 --nsamples 1 --seed 42 run1
