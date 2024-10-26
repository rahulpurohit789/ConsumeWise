


import requests
import sys

def evaluate_product(product_name):
    # Replace with your Hugging Face token
    hugging_face_token = "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"
    
    # Refined prompt to strictly request only JSON output
    prompt = (
        f"For the product '{product_name}', respond in JSON format with only the following fields:\n"
        "{\n"
        "  'product': 'product_name',\n"
        "  'evaluation': {\n"
        "    'should_consume': 'Yes or No',\n"
        "    'nutrition_label': {\n"
        "      'serving_size': 'serving size in ml or g',\n"
        "      'calories': 'number of calories',\n"
        "      'sugar': 'amount of sugar in grams',\n"
        "      'fat': 'amount of fat in grams'\n"
        "    },\n"
        "    'reason': 'Please provide a complete justification for the Yes or No answer, focusing on overall malnutrition, potential health risks, and long-term health implications associated with this product.'\n"
        "  }\n"
        "}\n"
        "Provide only the JSON response, without any introductory or additional text."
    )

    headers = {
        "Authorization": f"Bearer {hugging_face_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.5,  # Lower temperature for more deterministic output
            "top_k": 40,         
            "top_p": 0.8
        }
    }
    
    # Send the request to the Hugging Face API
    response = requests.post(
        "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct",
        headers=headers,
        json=payload
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        
        if result and len(result) > 0:
            generated_text = result[0]['generated_text']
            # Return the raw JSON string to avoid parsing issues
            return generated_text
        else:
            return "No response from the model."
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

if __name__ == "__main__":
    product_name = sys.argv[1]  # Get product name from command line argument
    evaluation = evaluate_product(product_name)
    print(evaluation)  # Print the output
 