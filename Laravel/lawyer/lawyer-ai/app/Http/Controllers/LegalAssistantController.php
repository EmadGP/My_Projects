<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use OpenAI;
use GuzzleHttp\Client;

class LegalAssistantController extends Controller
{
    private $systemPrompt = <<<EOT
Je bent een geavanceerde Nederlandse juridische AI-assistent met diepgaande kennis van het Nederlandse rechtssysteem. Je beschikt over uitgebreide kennis van wetboeken, jurisprudentie en rechtspraktijk. Je taak is om professioneel juridisch inzicht te bieden:

1. ANALYSE VAN JURIDISCHE VRAGEN:
- Geef grondige analyse op basis van actuele Nederlandse wetgeving
- Citeer specifieke wetsartikelen en relevante jurisprudentie
- Leg verbanden tussen verschillende rechtsbronnen
- Bied concrete interpretaties van de wet

2. GEDETAILLEERDE JURIDISCHE ANALYSE:
- Citeer relevante artikelen uit wetboeken (BW, Sr, Rv, etc.)
- Verwijs naar belangrijke rechtspraak en arresten
- Leg uit hoe de wet in de praktijk wordt toegepast
- Beschrijf concrete juridische procedures en termijnen
- Geef specifieke voorbeelden uit de rechtspraktijk

3. PROFESSIONELE COMMUNICATIE:
- Gebruik juridisch correcte terminologie
- Geef waar nodig heldere uitleg van juridische begrippen
- Onderbouw je antwoorden met wetsartikelen en jurisprudentie
- Wees specifiek en concreet in je adviezen

4. EXPERTISE IN:
- Burgerlijk Recht (contracten, aansprakelijkheid, etc.)
- Strafrecht (delicten, procedures, sancties)
- Bestuursrecht (vergunningen, bezwaar, beroep)
- Arbeidsrecht (contracten, ontslag, arbeidsvoorwaarden)
- Ondernemingsrecht (BV, NV, statutenwijzigingen)
- Huurrecht (woon- en bedrijfsruimte)
- Verkeersrecht (overtredingen, aansprakelijkheid)

5. PROFESSIONELE RICHTLIJNEN:
- Geef concrete, praktische adviezen gebaseerd op de wet
- Verwijs alleen naar een advocaat bij zeer complexe zaken of rechtszaakvertegenwoordiging
- Bied altijd specifieke wetsartikelen en jurisprudentie
- Leg uit welke juridische procedures mogelijk zijn

Structureer je antwoord altijd als volgt:
1. Juridische analyse van de situatie
2. Relevante wetgeving en jurisprudentie (met specifieke artikelen)
3. Concrete juridische mogelijkheden en procedures
4. Praktische stappen en termijnen
5. Aanvullende aandachtspunten of risico's

Als AI-assistent ben je in staat om gedetailleerd juridisch inzicht te geven, maar vermeld wel dat je advies niet bindend is en gebaseerd is op algemene juridische principes.
EOT;


    public function showChatInterface()
    {
        // Clear chat history when loading the page
        session()->forget('chat_history');
        return view('legal-advice');
    }

    public function getLegalAdvice(Request $request)
    {
        // Validate the incoming request
        $validated = $request->validate([
            'user_message' => 'required|string|max:1000',
        ]);

        try {
            $chatHistory = session('chat_history', []);

            // Add system message if this is the first message
            if (empty($chatHistory)) {
                $chatHistory[] = [
                    'role' => 'system',
                    'content' => $this->systemPrompt
                ];
            }

            // Add user's new message to history
            $chatHistory[] = [
                'role' => 'user',
                'content' => $validated['user_message']
            ];

            // Create a custom HTTP client with SSL verification disabled
            $client = new Client([
                'verify' => false,
                'timeout' => 30,
            ]);

            // Create OpenAI client with custom configuration
            $openai = OpenAI::factory()
                ->withApiKey(config('app.openai_api_key'))
                ->withHttpClient($client)
                ->make();

            // Send request to OpenAI with full chat history
            $result = $openai->chat()->create([
                'model' => 'gpt-4',
                'messages' => $chatHistory,
                'temperature' => 0.7,
                'max_tokens' => 1000, // Increased for more detailed responses
            ]);

            // Add AI's response to history
            $chatHistory[] = [
                'role' => 'assistant',
                'content' => $result->choices[0]->message->content
            ];

            // Save updated chat history to session
            session(['chat_history' => $chatHistory]);

            // Return the AI response to the frontend
            return response()->json([
                'response' => $result->choices[0]->message->content
            ]);

        } catch (\Exception $e) {
            // Return error message if something goes wrong
            return response()->json([
                'response' => 'Er is een fout opgetreden bij het verwerken van uw vraag: ' . $e->getMessage()
            ], 500);
        }
    }
}
