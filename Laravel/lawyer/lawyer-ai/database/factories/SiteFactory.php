<?php

namespace Database\Factories;

use App\Enums\ArtificialIntelligenceType;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class SiteFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => $this->faker->name(),
            'url' => $this->faker->url(),
            'provider' => $this->faker->randomElement(ArtificialIntelligenceType::values()),
            'model' => $this->faker->word(),
            'prompt' => $this->faker->realText(50),
        ];
    }
}
