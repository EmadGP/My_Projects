<?php

namespace App\AI\OpenAI\Requests;

use App\Models\Site;
use Saloon\Contracts\Body\HasBody;
use Saloon\Enums\Method;
use Saloon\Http\Connector;
use Saloon\Http\Request;
use Saloon\Traits\Body\HasJsonBody;
use Saloon\Traits\Request\HasConnector;

class PostOpenAIChatCompletionRequest extends Request implements HasBody
{
    use HasConnector;
    use HasJsonBody;

    protected Method $method = Method::POST;

    public function __construct(
        protected Site $site
    ) {
    }

    public function resolveConnector(): Connector
    {
        return OpenAIConnector::make();
    }

    public function resolveEndpoint(): string
    {
        return '/chat/completions';
    }

    public function defaultBody(): array
    {
        return [
            'model' => $this->site->model,
        ];
    }
}
