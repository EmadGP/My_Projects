from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# In-memory database for URL mappings
url_db = {}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate a simple hash for the URL
    short_url = str(hash(original_url))[:6]
    url_db[short_url] = original_url

    # Full URL for redirection (not shown in the UI)
    short_url_full = f'http://localhost:5000/{short_url}'

    # Pass only the short part to the template
    return render_template('index.html', short_url=short_url_full)


@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    original_url = url_db.get(short_url)

    if not original_url:
        return jsonify({'error': 'URL not found'}), 404

    return redirect(original_url)

if __name__ == '__main__':
    app.run(debug=True)
