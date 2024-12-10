<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Http;

class AppServiceProvider extends ServiceProvider
{
    public function register()
    {
        //
    }

    public function boot()
    {
        Http::macro('openai', function () {
            return Http::withoutVerifying()
                      ->withHeaders([
                          'Authorization' => 'Bearer ' . config('app.openai_api_key'),
                          'Content-Type' => 'application/json',
                      ]);
        });
    }
}
