<?php

namespace App\AI\OpenAI\Actions;

use App\AI\OpenAI\Requests\PostOpenAIChatCompletionRequest;
use App\Models\Site;

class AskOpenAIAction
{
    public function execute(Site $site, string $message): array
    {
        $aiRequest = PostOpenAIChatCompletionRequest::make($site);
        $aiRequest->body()->add('messages', [
            [
                'role' => 'system',
                'content' => $site->prompt,
            ],
            [
                'role' => 'user',
                'content' => $message,
            ]
        ]);

        return $aiRequest->send()->json();
    }
}
