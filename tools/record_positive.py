# record_positive.py
# -----------------------------------------
# Description:
# Records positive wake word samples ("Hana") for training.
# Each recording captures a single utterance of the wake word.
# Vary your tone, speed, and distance from the mic between takes.
# -----------------------------------------

import soundfile as sf
import sounddevice as sd
import os

# --- Configuration ---
WAKE_WORD = "Hana"
SAVE_DIR = os.path.join("training_data", "positive")
SAMPLE_RATE = 16000
DURATION = 2       # seconds per recording (enough for a short word)
NUM_SAMPLES = 100  # total recordings to collect

os.makedirs(SAVE_DIR, exist_ok=True)

# Find the next available file index (allows resuming)
existing = [f for f in os.listdir(SAVE_DIR) if f.startswith("pos_") and f.endswith(".wav")]
start_index = len(existing) + 1

print(f"\nPositive sample recorder — wake word: '{WAKE_WORD}'")
print(f"Target: {NUM_SAMPLES} recordings | Saving to: {SAVE_DIR}")
print(f"Starting from sample #{start_index}\n")
print("Tips for better accuracy:")
print("  - Say the word naturally, as you would to your assistant")
print("  - Vary your distance: close, arm's length, across the room")
print("  - Vary your tone: normal, slightly raised, casual")
print("  - Stay quiet before and after saying the word\n")

recorded = 0
i = start_index

while recorded < NUM_SAMPLES:
    input(f"[{recorded + 1}/{NUM_SAMPLES}] Press Enter, then say '{WAKE_WORD}'...")
    print("  Recording...")

    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()

    filename = f"pos_{i:04d}.wav"
    filepath = os.path.join(SAVE_DIR, filename)
    sf.write(filepath, audio, SAMPLE_RATE)

    print(f"  Saved: {filename}")

    recorded += 1
    i += 1

    # Offer a break every 25 recordings
    if recorded % 25 == 0 and recorded < NUM_SAMPLES:
        cont = input(f"\n--- {recorded} recordings done. Take a break? Press Enter to continue or Ctrl+C to stop. ---\n")

print(f"\nDone! {recorded} recordings saved to '{SAVE_DIR}'.")
print("Run 'nanowakeword-train -c hana_config.yaml' when ready to train.")
