<?php

namespace App\Actions;

use App\AI\OpenAI\Actions\AskOpenAIAction;
use App\Enums\ArtificialIntelligenceType;
use App\Models\Site;
use Illuminate\Http\Exceptions\HttpResponseException;

class AskArtificialIntelligenceAction
{
    public function execute(Site $site, string $message)
    {
        $action = match ($site->provider) {
            ArtificialIntelligenceType::OPEN_AI() => app(AskOpenAIAction::class),
            default => null
        };

        if (! $action) {
            $response = response()->json([
                'message' => 'AI provider not found',
                'error' => [
                    'Site do not have a valid AI provider'
                ],
            ], 422);

            throw new HttpResponseException($response);
        }

        $response = $action->execute($site, $message);

        $site->history()->create([
            'message' => $message,
            'provider' => $site->provider,
            'model' => $site->model,
            'prompt' => $site->prompt,
            'response' => $response,
        ]);

        return match ($site->provider) {
            ArtificialIntelligenceType::OPEN_AI() => $response['choices'][0]['message'],
            default => null
        };

    }
}
