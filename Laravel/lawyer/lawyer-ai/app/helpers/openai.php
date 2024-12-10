<?php

use App\AI\OpenAI\Requests\GetOpenAIModelsRequest;

if (! function_exists('openaiModels')) {
    function openaiModels(): array
    {
        $request = new GetOpenAIModelsRequest();
        $response = $request->send()->collect('data');

        return $response
            ->sortByDesc('created')
            ->pluck('id', 'id')
            ->toArray();
    }
}
