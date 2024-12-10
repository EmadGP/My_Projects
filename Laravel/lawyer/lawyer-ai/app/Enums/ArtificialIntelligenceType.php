<?php

namespace App\Enums;

use ArchTech\Enums\InvokableCases;
use ArchTech\Enums\Options;
use ArchTech\Enums\Values;
use Illuminate\Support\Str;

enum ArtificialIntelligenceType: string
{
    use InvokableCases;
    use Values;
    use Options;

    case OPEN_AI = 'OpenAI';

    public static function options(): array
    {
        return collect(self::cases())
            ->mapWithKeys(fn ($case) => [
                $case->value => Str::of($case->name)
                    ->replace('_', ' ')
                    ->value()
            ])
            ->toArray();
    }
}
