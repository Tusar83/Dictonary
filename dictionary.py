import sys
from nltk.corpus import wordnet

def get_definitions_and_synonyms(word):
    """Get definitions and synonyms for a given word."""
    word = word.lower().strip()
    
    # Get all synsets for the word
    synsets = wordnet.synsets(word)
    
    if not synsets:
        print(f"Error: No definitions found for '{word}'")
        return False
    
    # Collect unique definitions and synonyms
    definitions = []
    synonyms = set()
    
    for synset in synsets:
        # Get definition
        definition = synset.definition()
        definitions.append(definition)
        
        # Get synonyms from all lemmas in the synset
        for lemma in synset.lemmas():
            if lemma.name() != word:  # Exclude the word itself
                synonyms.add(lemma.name().replace('_', ' '))
    
    # Display results
    print(f"\n{'='*60}")
    print(f"Word: {word.capitalize()}")
    print(f"{'='*60}")
    
    print(f"\nDefinitions ({len(definitions)}):")
    for i, defn in enumerate(definitions, 1):
        print(f"  {i}. {defn}")
    
    if synonyms:
        print(f"\nSynonyms:")
        for syn in sorted(synonyms):
            print(f"  - {syn}")
    else:
        print("\nNo synonyms found.")
    
    print()
    return True

def main():
    """Main function to run the CLI dictionary app."""
    print("="*60)
    print("NLTK WordNet Dictionary CLI")
    print("="*60)
    print("Type 'quit' or 'exit' to exit the program.\n")
    
    while True:
        try:
            word = input("Enter a word: ").strip()
            
            # Check for exit commands
            if word.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                sys.exit(0)
            
            # Check for empty input
            if not word:
                print("Please enter a word.\n")
                continue
            
            # Get definitions and synonyms
            get_definitions_and_synonyms(word)
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}\n")

if __name__ == "__main__":
    main()
