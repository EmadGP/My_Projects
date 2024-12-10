<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Laravel\Sanctum\HasApiTokens;

class Site extends Model
{
    use HasFactory;
    use HasApiTokens;

    public $fillable = ['name', 'url', 'provider', 'model', 'prompt'];

    public function history(): HasMany
    {
        return $this->hasMany(History::class);
    }
}
