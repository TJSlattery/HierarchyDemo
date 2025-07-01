import random
import json

def generate_single_hierarchy_id():
    """
    Generates a single hierarchy_id string with a variable, weighted depth.
    Shorter hierarchy strings are generated less frequently.
    """
    # Define the segments and the probability for each hierarchy depth
    segments = ['CLI', 'BAN', 'AGE', 'COM', 'DIV', 'DEP']
    # Probabilities for depths 1 through 6. (e.g., 1% chance for depth 1)
    weights = [0.01, 0.04, 0.10, 0.20, 0.30, 0.35] 
    
    # Randomly choose the depth of the hierarchy based on the weights
    # The population `range(1, 7)` corresponds to depths 1 through 6.
    chosen_depth = random.choices(population=range(1, 7), weights=weights, k=1)[0]
    
    # Build the hierarchy string segment by segment to the chosen depth
    id_parts = []
    for i in range(chosen_depth):
        segment_name = segments[i]
        random_num = random.randint(0, 100)
        id_parts.append(f"{segment_name}_{random_num:06d}")
        
    return "-".join(id_parts)

def main():
    """
    Generates a list of 1,500 unique, mixed-depth hierarchy_ids and saves it to a JSON file.
    """
    num_to_generate = 1500
    output_filename = "hierarchy_query.json"
    unique_ids = set()

    # Loop until we have collected the desired number of unique IDs.
    # A set is used to automatically handle and prevent duplicates.
    while len(unique_ids) < num_to_generate:
        unique_ids.add(generate_single_hierarchy_id())

    # Convert the set to a list for the final JSON output
    hierarchy_id_array = list(unique_ids)

    # Write the list to the specified JSON file
    with open(output_filename, 'w') as f:
        json.dump(hierarchy_id_array, f, indent=4)
    
    print(f"✅ Successfully generated and saved {len(hierarchy_id_array)} unique, mixed-depth IDs to {output_filename}")

if __name__ == "__main__":
    main()