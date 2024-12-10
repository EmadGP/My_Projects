<!DOCTYPE html>
<html>
<head>
    <title>Legal Assistant</title>
</head>
<body>
<h1>Legal Assistant for Dutch Law</h1>
<form id="legalForm">
    <textarea name="query" id="query" rows="5" placeholder="Enter your legal query here..."></textarea>
    <button type="submit">Analyze</button>
</form>
<div id="response"></div>

<script>
    document.getElementById('legalForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('query').value;

        const response = await fetch('/legal-analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
        });

        const data = await response.json();
        document.getElementById('response').innerText = data.response;
    });
</script>
</body>
</html>
