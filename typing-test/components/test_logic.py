import time

def calculate_wpm(start_time: float, end_time: float, char_count: int) -> float:
    """
    Calculate the word per minute (WPM): 1 word = 5 characters
    """
    elapsed = end_time - start_time
    if elapsed <= 0:
        return 0.0
    words = char_count / 5
    return words / (elapsed / 60)

def calculate_accuracy(sample: str, typed: str) -> float:
    """
    compute accuracy as percentage of correctly typed characters.
    """
    correct = sum(1 for i, c in enumerate(typed) if i < len(sample) and c == sample[i])
    total = len(sample)
    return (correct / total) * 100 if total > 0 else 0.0
