<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Auth\Middleware\Authenticate;
use Illuminate\Http\Exceptions\HttpResponseException;

class AuthenticateSite extends Authenticate
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @param  string  ...$guards
     * @return mixed
     *
     * @throws \Illuminate\Auth\AuthenticationException
     */
    public function handle($request, Closure $next, ...$guards)
    {
        $this->auth = auth();

        $this->authenticate($request, ['sanctum']);

        return $next($request);
    }

    protected function unauthenticated($request, array $guards)
    {
        $response = response()->json([
            'message' => 'Access denied',
            'error' => [
                'Please provide a valid access token.'
            ],
        ], 401);

        throw new HttpResponseException($response);
    }
}
