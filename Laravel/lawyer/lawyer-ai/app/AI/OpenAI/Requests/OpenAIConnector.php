<?php

namespace App\AI\OpenAI\Requests;

use Saloon\Contracts\Authenticator;
use Saloon\Http\Auth\TokenAuthenticator;
use Saloon\Http\Connector;

class OpenAIConnector extends Connector
{

    public function resolveBaseUrl(): string
    {
        return 'https://api.openai.com/v1';
    }

    public function defaultAuth(): TokenAuthenticator
    {
        return new TokenAuthenticator(config('openai.api_key'));
    }

    public function defaultHeaders(): array
    {
        return [
            "OpenAI-Organization" => config('openai.organization'),
            "OpenAI-Project" => env('OPENAI_PROJECT'),
        ];
    }
}
