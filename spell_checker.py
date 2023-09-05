import csv

""" Custom cost of Levenshtein Distance """
INSERTION_COST = 1.0
DELETION_COST = 1.0
SUBSTITUTION_COST = 1.0
MODIFIED_COST = 0.5
INSERTION_DICT = ['a', 'i', 'u', 'e', 'o']
SUBTITUTION_DICT = {
    'o' : ['u', 'a'],
    'e' : ['a', 'i'],
    'c': ['k', 's'],
    'q': ['k'],
    'w': ['u'],
    'k': ['g']
}
DELETION_DICT = ['h', 'c', 'd']

def is_valid_word(word, dictionary):
  """Checks if a word is in the dictionary."""
  return word in dictionary

def is_vowel(c):
  """Returns True if c is a vowel, False otherwise."""
  vowels = ["a", "e", "i", "o", "u"]
  return c in vowels

def load_dictionary_from_tsv(filename):
  """Loads a dictionary from a TSV file and returns it as a list."""
  try:
    with open(filename, "r") as f:
      reader = csv.reader(f, delimiter="\t")
      words = []
      for row in reader:
        words.append(row[0])
      return words
  except FileNotFoundError:
    raise FileNotFoundError(f"Could not find file: {filename}")
  except Exception as e:
    raise Exception(f"Failed to load dictionary from file: {filename}. Error: {e}")

def deletion_cost(s, c):
    if s == '':
        return 0
    cost = DELETION_COST
    if c in DELETION_DICT:
        cost = MODIFIED_COST
    return cost

def insertion_cost(s, i, c):
    if not s or i >= len(s):
        return INSERTION_COST
    cost = INSERTION_COST
    if c in INSERTION_DICT:
        cost = MODIFIED_COST
    return cost

def subtitution_cost(s, i, c):
    if not s or i >= len(s):
        return SUBSTITUTION_COST
    cost = SUBSTITUTION_COST
    if s[i] in SUBTITUTION_DICT and c in SUBTITUTION_DICT[s[i]]:
        cost = MODIFIED_COST
    return cost

def edit_distance(word1, word2):
  """Computes the Levenshtein edit distance between two strings."""
  source = str(word1)
  target = str(word2)
  m = len(source)
  n = len(target)

  # A multidimensional array of 0s with len(s) rows and len(t) columns.
  d = [[0]*(len(target) + 1) for i in range(len(source) + 1)]

  for i in range(len(source) + 1):
      d[i][0] = sum([deletion_cost(source, j - 1) for j in range(i)])

  for i in range(len(target) + 1):
      intermediate_string = ""
      cost = 0.0
      for j in range(i):
          cost += insertion_cost(intermediate_string, j - 1, target[j - 1])
          intermediate_string = intermediate_string + target[j - 1]
      d[0][i] = cost

  for j in range(1, len(target) + 1):
      for i in range(1, len(source) + 1):
          if source[i - 1] == target[j - 1]:
              d[i][j] = d[i - 1][j - 1]
          else:
              del_cost = deletion_cost(source, i - 1)
              insert_cost = insertion_cost(source, i, target[j - 1])
              sub_cost = subtitution_cost(source, i - 1, target[j - 1])
              d[i][j] = min(d[i - 1][j] + del_cost,
                      d[i][j - 1] + insert_cost,
                      d[i - 1][j - 1] + sub_cost)

  return d[m][n]

def spell_checker(word, dictionary):
  """Returns the 5 most likely correct spellings of a word, along with the similarity score and edit distance."""
  best_words = []
  min_distance = float("inf")
  best_score = 0
  for w in dictionary:
    distance = edit_distance(word, w)
    score = 1 - distance / len(word)
    if distance < min_distance or (distance == min_distance and score > best_score):
      min_distance = distance
      best_score = score
      best_words = [w]
    elif distance == min_distance and score == best_score:
      best_words.append(w)
  return best_words[:5]

def main():
  filename = "/content/kbbi-root-word.tsv"
  words = load_dictionary_from_tsv(filename)

  word = input("Enter a word: ")
  corrected_words = spell_checker(word, words)
  print(f"The most likely correct spellings of {word} are:")
  for w in corrected_words:
    print(f"- {w}")

if __name__ == "__main__":
  main()
