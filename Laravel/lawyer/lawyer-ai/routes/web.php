<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LegalAssistantController;

// Show the chat interface on the main page
Route::get('/', [LegalAssistantController::class, 'showChatInterface']);

// Handle the chat interactions
Route::post('/legal-advice', [LegalAssistantController::class, 'getLegalAdvice']);
