@extends('layouts.app')

@section('content')
<div class="container">
    <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
            <!-- Messages will be displayed here -->
        </div>
        
        <form method="POST" action="{{ url('legal-advice') }}" class="chat-form" id="legal-advice-form">
            @csrf
            <div class="input-group">
                <textarea 
                    name="user_message" 
                    class="form-control" 
                    placeholder="Beschrijf uw juridische vraag hier..." 
                    required
                ></textarea>
                <button type="submit" class="btn btn-primary">Verstuur</button>
            </div>
        </form>
    </div>
</div>

@push('scripts')
<script>
document.getElementById('legal-advice-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const form = this;
    const userMessage = form.user_message.value;

    // Show user message
    appendMessage(userMessage, 'user-message');
    
    // Show loading indicator
    const loadingMessage = appendMessage('Bezig met verwerken...', 'loading-message');
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({
                user_message: userMessage
            })
        });
        
        const data = await response.json();
        
        // Remove loading message
        loadingMessage.remove();
        
        // Add the AI response
        appendMessage(data.response, 'ai-message');
        
        // Clear the input field
        form.user_message.value = '';
        
    } catch (error) {
        loadingMessage.remove();
        appendMessage('Er is een fout opgetreden bij het verwerken van uw vraag.', 'error-message');
    }
});

function appendMessage(message, className) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return messageElement;
}
</script>
@endpush

@push('styles')
<style>
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.chat-messages {
    height: 400px;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 5px;
}

.chat-form {
    margin-top: 20px;
}

.message {
    margin-bottom: 10px;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 5px;
}

.user-message {
    background-color: #e3f2fd;
    margin-left: 20%;
    margin-right: 5px;
}

.ai-message {
    background-color: #f5f5f5;
    margin-right: 20%;
    margin-left: 5px;
}

.loading-message {
    background-color: #fff3cd;
    font-style: italic;
}

.error-message {
    background-color: #f8d7da;
    color: #721c24;
}
</style>
@endpush
@endsection 