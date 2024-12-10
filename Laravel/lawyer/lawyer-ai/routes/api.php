<?php

use App\Http\Controllers\SiteController;
use App\Http\Middleware\AuthenticateSite;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::middleware([AuthenticateSite::class])
    ->prefix('v1')
    ->group(function () {
        Route::post('/chat', [SiteController::class, 'chat'])->name('site.chat');
    });
