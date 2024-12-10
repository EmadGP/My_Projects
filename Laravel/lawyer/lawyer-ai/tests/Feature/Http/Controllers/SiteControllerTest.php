<?php

namespace Tests\Feature\Http\Controllers;

use App\Models\Site;

it('should authenticate api request', function () {
    $response = $this->postJson('/api/v1/chat', []);
    $response->assertStatus(401);
});

it('should validate api request', function () {
    $site = Site::factory()->create();
    $token = $site->createToken('test')->plainTextToken;

    $response = $this->postJson('/api/v1/chat', [], [
        'Authorization' => 'Bearer ' . $token,
    ]);

    $response->assertStatus(422);
});

it('should successfully api request', function () {
    $site = Site::factory()->create();
    $token = $site->createToken('test')->plainTextToken;

    $response = $this->postJson('/api/v1/chat', [], [
        'Authorization' => 'Bearer ' . $token,
    ]);

    $response->assertStatus(422);

    expect($response->json())
        ->toBe([
            "message" => "Invalid data send",
            "error" => [
                "Message is required"
            ]
        ]);
});
