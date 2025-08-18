from flask import Flask, render_template, request, jsonify
import time
import logging
import base64
import string
from collections import defaultdict

app = Flask(__name__)

# Logging setup
logging.basicConfig(
    filename='ctf_web.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)
logging.info("Starting CTF Challenge Maker server")

# Cipher Helpers
def vigenere_decode(ciphertext, key):
    try:
        alphabet = string.ascii_uppercase
        key = key.upper()
        plaintext = ""
        key_idx = 0
        for char in ciphertext.upper():
            if char in alphabet:
                key_char = key[key_idx % len(key)]
                shift = alphabet.index(key_char)
                plain_idx = (alphabet.index(char) - shift) % 26
                plaintext += alphabet[plain_idx]
                key_idx += 1
            else:
                plaintext += char
        return plaintext
    except Exception as e:
        logging.error(f"Vigenère decode error: {str(e)}")
        return None

def rail_fence_decode(ciphertext, rails):
    try:
        if rails == 1:
            return ciphertext
        n = len(ciphertext)
        fence = [['' for _ in range(n)] for _ in range(rails)]
        row, col, direction = 0, 0, 1
        for i in range(n):
            fence[row][col] = '*'
            col += 1
            row += direction
            if row == rails - 1 or row == 0:
                direction *= -1
        idx = 0
        for r in range(rails):
            for c in range(n):
                if fence[r][c] == '*' and idx < len(ciphertext):
                    fence[r][c] = ciphertext[idx]
                    idx += 1
        plaintext = ""
        row, col, direction = 0, 0, 1
        for i in range(n):
            plaintext += fence[row][col]
            col += 1
            row += direction
            if row == rails - 1 or row == 0:
                direction *= -1
        return plaintext
    except Exception as e:
        logging.error(f"Rail Fence decode error: {str(e)}")
        return None

# Challenge Data
CHALLENGES = {
    "puzzle": {
        "question": "What is the capital of France?",
        "answer": "Paris",
        "flag": "CTF{Paris}",
        "hint": "The answer is a well-known European city."
    },
    "base64": {
        "question": "Decode this Base64 string: Q1RGe0Jhc2U2NEZsYWd9",
        "answer": "CTF{Base64Flag}",
        "flag": "CTF{Base64Flag}",
        "hint": "Use a Base64 decoder (e.g., Python's base64 module or online tools)."
    },
    "vigenere": {
        "question": "Decode this Vigenère cipher: FJHLTKAF with key: KEY",
        "answer": "CTF{VigFlag}",
        "flag": "CTF{VigFlag}",
        "hint": "Use the Vigenère cipher with the provided key. Letters only, case-insensitive."
    },
    "railfence": {
        "question": "Decode this Rail Fence cipher (3 rails): CcrctT{ye_euiyFbsr}",
        "answer": "CTF{cyber_security}",
        "flag": "CTF{cyber_security}",
        "hint": "Rearrange the text using a Rail Fence cipher with 3 rails."
    },
    "stego": {
        "question": "Extract the hidden flag from this JPG's LSB data: '01000011 01010100 01000110 01111011 01010011 01110100 01100101 01100111 01101111 01000110 01101100 01100001 01100111 01111101'. Convert binary to ASCII.",
        "answer": "CTF{StegoFlag}",
        "flag": "CTF{StegoFlag}",
        "hint": "Convert each 8-bit binary sequence to ASCII characters."
    },
    "forensics": {
        "question": "Convert this PDF text extract: 'Metadata: Author=CTF{ForensicFlag}, Date=2025-06-23'. Extract the flag.",
        "answer": "CTF{ForensicFlag}",
        "flag": "CTF{ForensicFlag}",
        "hint": "Look for a string in the format CTF{...} in the simulated PDF metadata."
    }
}

# Rate limiting and blocking
MAX_REQUESTS = 5
MAX_INPUT_LEN = 50
INVALID_LIMIT = 3
client_activity = defaultdict(lambda: [0, 0, 0])  # timestamp, req_count, invalid_count
blocked_ips = set()
# Optional: Time-based blocking
# blocked_until = defaultdict(lambda: 0)

@app.route('/')
def index():
    try:
        ip = request.remote_addr
        logging.debug(f"Connection to / from {ip}")
        return render_template('Front_End.html')
    except Exception as e:
        logging.error(f"Error rendering index.html: {str(e)}")
        return jsonify({"error": "Internal Server Error: Template issue"}), 500

@app.route('/api/submit', methods=['POST'])
def submit_command():
    try:
        ip = request.remote_addr
        current_time = time.time()
        logging.debug(f"Submit request from {ip}")

        # Handle blocked IP
        if ip in blocked_ips:
            logging.warning(f"Blocked access attempt from {ip}")
            return jsonify({
                "response": f"Access denied for {ip}: Blocked due to repeated suspicious activity. Please try later."
            })

        # Reset counters every 60s
        if client_activity[ip][0] == 0 or current_time - client_activity[ip][0] > 60:
            client_activity[ip] = [current_time, 1, client_activity[ip][2]]
        else:
            client_activity[ip][1] += 1

        # Too many requests
        if client_activity[ip][1] > MAX_REQUESTS:
            blocked_ips.add(ip)
            logging.warning(f"Blocked {ip}: Too many requests per minute")
            return jsonify({
                "response": f"{ip} has been blocked: Too many requests. Please wait before trying again."
            })

        command = request.form.get('command', '').strip()
        if not command:
            logging.info(f"{ip} sent empty command")
            return jsonify({"response": "No command provided."})

        # Input too long
        if len(command) > MAX_INPUT_LEN:
            client_activity[ip][2] += 1
            logging.warning(f"{ip} sent long input ({len(command)} chars)")
            if client_activity[ip][2] >= INVALID_LIMIT:
                blocked_ips.add(ip)
                logging.warning(f"Blocked {ip}: Too many invalid inputs")
                return jsonify({
                    "response": f"{ip} has been blocked: Too many invalid attempts (long or malformed input)."
                })
            return jsonify({"response": "Input too long. Try again."})

        # Command processing
        if command == "HELP":
            response = "Commands:\nHELP - Show this help\nLIST - List challenges\nCHALLENGE <name> - Get challenge details\nSOLVE <challenge> <answer> - Submit answer\n"
        elif command == "LIST":
            response = "Available challenges: " + ", ".join(CHALLENGES.keys()) + "\n"
        elif command.startswith("CHALLENGE "):
            challenge_name = command[10:].strip().lower()
            if challenge_name in CHALLENGES:
                c = CHALLENGES[challenge_name]
                response = f"Challenge: {challenge_name}\nTask: {c['question']}\nHint: {c['hint']}\nSubmit with: SOLVE {challenge_name} <answer>\n"
            else:
                client_activity[ip][2] += 1
                response = "Invalid challenge name. Use LIST to see available challenges.\n"
        elif command.startswith("SOLVE "):
            parts = command[6:].strip().split(" ", 1)
            if len(parts) != 2:
                client_activity[ip][2] += 1
                response = "Usage: SOLVE <challenge> <answer>\n"
            else:
                challenge_name, answer = parts[0].lower(), parts[1].strip()
                expected_answer = CHALLENGES.get(challenge_name, {}).get('answer')
                is_correct = False
                if expected_answer:
                    if challenge_name == "base64":
                        try:
                            decoded = base64.b64decode(answer).decode()
                            is_correct = decoded == expected_answer
                        except:
                            is_correct = answer == expected_answer
                    elif challenge_name == "vigenere":
                        decoded = vigenere_decode("FJHLTKAF", "KEY")
                        is_correct = answer == expected_answer or (decoded and decoded == answer)
                    elif challenge_name == "railfence":
                        decoded = rail_fence_decode("TFCRal{iFlaegn}c", 3)
                        is_correct = answer == expected_answer or (decoded and decoded == answer)
                    else:
                        is_correct = answer == expected_answer

                    if is_correct:
                        response = f"Correct! Flag: {CHALLENGES[challenge_name]['flag']}\n"
                    else:
                        client_activity[ip][2] += 1
                        response = "Wrong answer. Try again.\n"
                else:
                    client_activity[ip][2] += 1
                    response = "Invalid challenge name. Use LIST to see challenges.\n"
        else:
            client_activity[ip][2] += 1
            response = "Invalid command. Type HELP for list of commands.\n"

        # Block after too many invalids
        if client_activity[ip][2] >= INVALID_LIMIT:
            blocked_ips.add(ip)
            logging.warning(f"Blocked {ip}: Too many invalid attempts")
            return jsonify({
                "response": f"{ip} has been blocked: Too many invalid commands or answers."
            })

        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error in submit_command: {str(e)}")
        return jsonify({"error": "Internal Server Error: Processing issue"}), 500

if __name__ == '__main__':
    try:
        app.run(host='localhost', port=5000, debug=True)
    except Exception as e:
        logging.error(f"Server startup error: {str(e)}")
        print(f"Failed to start server: {str(e)}")

