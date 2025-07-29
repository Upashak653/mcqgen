import json
import PyPDF2

def read_file(file):
    # Use file.name to access filename
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ""
        
    elif file.name.endswith('.txt'):
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return ""
        
    else:
        raise Exception("Unsupported file format. Please upload a .pdf or .txt file.")


def get_data(quiz_string):
    try:
        # Remove optional prefix
        if quiz_string.strip().startswith("### RESPONSE_JSON"):
            quiz_string = quiz_string.split("### RESPONSE_JSON", 1)[1].strip()

        # Debugging print
        print("🚀 Cleaned quiz string:", quiz_string)

        # Load JSON
        parsed = json.loads(quiz_string)
        quiz_table_data = []

        for key, value in parsed.items():
            mcq = value["mcq"]
            options = " || ".join(
                [f"{opt}:-> {desc}" for opt, desc in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({
                "mcq": mcq,
                "options": options,
                "correct": correct
            })
        return quiz_table_data
    except Exception as e:
        print("❌ Error parsing quiz data:", e)
        return None
