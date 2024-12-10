<?php

namespace App\AI\OpenAI\Requests;

use Illuminate\Support\Facades\Cache;
use Saloon\CachePlugin\Contracts\Cacheable;
use Saloon\CachePlugin\Contracts\Driver;
use Saloon\CachePlugin\Drivers\LaravelCacheDriver;
use Saloon\CachePlugin\Traits\HasCaching;
use Saloon\Enums\Method;
use Saloon\Http\Connector;
use Saloon\Http\Request;
use Saloon\Traits\Request\HasConnector;

class GetOpenAIModelsRequest extends Request implements Cacheable
{
    use HasCaching;
    use HasConnector;

    protected Method $method = Method::GET;

    public function resolveConnector(): Connector
    {
        return OpenAIConnector::make();
    }

    public function resolveEndpoint(): string
    {
        return '/models';
    }

    public function resolveCacheDriver(): Driver
    {
        return new LaravelCacheDriver(Cache::store(env('CACHE_STORE')));
    }

    public function cacheExpiryInSeconds(): int
    {
        return 3600; // One Hour
    }
}
