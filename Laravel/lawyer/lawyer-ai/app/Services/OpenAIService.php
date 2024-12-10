<?php

namespace App\Services;

use GuzzleHttp\Client;

class OpenAIService
{
    protected $client;

    public function __construct()
    {
        $this->client = new Client([
            'base_uri' => 'https://api.openai.com/v1/',
            'headers' => [
                'Authorization' => 'Bearer ' . env('OPENAI_API_KEY'),
                'Content-Type'  => 'application/json',
            ],
        ]);
    }

    public function chat($prompt)
    {
        $response = $this->client->post('completions', [
            'json' => [
                'model' => 'text-davinci-003', // Adjust model as needed
                'prompt' => $prompt,
                'max_tokens' => 1000,
                'temperature' => 0.7,
            ],
        ]);

        return json_decode($response->getBody()->getContents(), true);
    }
}
