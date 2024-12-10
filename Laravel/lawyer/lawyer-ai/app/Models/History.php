<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class History extends Model
{
    public $fillable = [
        'message', 'provider', 'model', 'prompt', 'response', 'site_id',
    ];

    public $casts = [
        'response' => 'array',
    ];
}
