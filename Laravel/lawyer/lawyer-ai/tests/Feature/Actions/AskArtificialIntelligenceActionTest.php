<?php

namespace Tests\Feature\Actions;

use App\Actions\AskArtificialIntelligenceAction;
use App\AI\OpenAI\Actions\AskOpenAIAction;
use App\AI\OpenAI\Requests\PostOpenAIChatCompletionRequest;
use App\Enums\ArtificialIntelligenceType;
use App\Models\Site;
use Illuminate\Http\Exceptions\HttpResponseException;
use Mockery\MockInterface;
use Saloon\Http\Faking\MockResponse;
use Saloon\Laravel\Facades\Saloon;

it('should validate site AI provider', function () {
    $site = Site::factory()->create([
        'provider' => 'invalid',
    ]);

    $action = app(AskArtificialIntelligenceAction::class);

    $this->assertThrows(fn () => $action->execute($site, 'sample'), HttpResponseException::class);
});

it('should create a new history record', function () {
    $site = Site::factory()->create([
        'provider' => ArtificialIntelligenceType::OPEN_AI(),
    ]);

    $result = file_get_contents(storage_path('/test/open_ai/chat-response.json'));
    Saloon::fake([
        PostOpenAIChatCompletionRequest::class => MockResponse::make(json_decode($result, true))
    ]);

    app(AskArtificialIntelligenceAction::class)->execute($site, 'sample');

    $this->assertDatabaseHas('histories', [
        'site_id' => $site->id,
        'message' => 'sample',
        'provider' => $site->provider,
    ]);
});
