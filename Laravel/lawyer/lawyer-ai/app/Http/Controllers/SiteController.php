<?php

namespace App\Http\Controllers;

use App\Actions\AskArtificialIntelligenceAction;
use App\Http\Requests\SiteArtificialIntelligenceRequest;

class SiteController extends Controller
{
    public function chat(SiteArtificialIntelligenceRequest $request, AskArtificialIntelligenceAction $askArtificialIntelligenceAction)
    {
        $validated = $request->validate([
            'message' => 'required|string',
        ]);

        $site = auth()->user();

        $response = $askArtificialIntelligenceAction->execute($site, $validated['message']);

        return response()->json($response);
    }
}
