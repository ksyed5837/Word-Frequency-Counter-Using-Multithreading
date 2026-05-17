"""
Lab 1: Word Frequency Counter Using Multithreading

This program reads a text file, divides the words into N segments, and uses
one thread per segment to count word frequencies. The main thread waits for
all worker threads, then combines the partial results into one final count.
"""

import argparse
import re
import threading
from collections import Counter
from pathlib import Path


def clean_and_split_words(text):
    """Convert text to lowercase words and remove punctuation."""
    return re.findall(r"[a-zA-Z0-9']+", text.lower())


def divide_words(words, number_of_segments):
    """Divide a list of words into N nearly equal segments."""
    segments = []
    total_words = len(words)
    segment_size = (total_words + number_of_segments - 1) // number_of_segments

    for i in range(number_of_segments):
        start = i * segment_size
        end = start + segment_size
        segments.append(words[start:end])

    return segments


def count_words_in_segment(segment_id, words, results):
    """Thread function: count word frequency for one segment."""
    word_count = Counter(words)
    results[segment_id] = word_count

    print(f"\nIntermediate count from Thread {segment_id + 1}:")
    if word_count:
        for word, count in sorted(word_count.items()):
            print(f"  {word}: {count}")
    else:
        print("  No words in this segment.")


def main():
    parser = argparse.ArgumentParser(description="Multithreaded Word Frequency Counter")
    parser.add_argument("text_file", help="Path to the input text file")
    parser.add_argument("segments", type=int, help="Number of segments/threads to use")
    args = parser.parse_args()

    file_path = Path(args.text_file)
    number_of_segments = args.segments

    if number_of_segments <= 0:
        raise ValueError("Number of segments must be greater than 0.")

    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    text = file_path.read_text(encoding="utf-8")
    words = clean_and_split_words(text)

    print(f"Total words found: {len(words)}")
    print(f"Number of segments/threads: {number_of_segments}")

    segments = divide_words(words, number_of_segments)
    results = [Counter() for _ in range(number_of_segments)]
    threads = []

    for segment_id, segment_words in enumerate(segments):
        thread = threading.Thread(
            target=count_words_in_segment,
            args=(segment_id, segment_words, results)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_count = Counter()
    for partial_count in results:
        final_count.update(partial_count)

    print("\nFinal consolidated word frequency count:")
    for word, count in sorted(final_count.items()):
        print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
