<?php

namespace App\Filament\Resources;

use App\AI\OpenAI\Actions\GetOpenAIModelsAction;
use App\Enums\ArtificialIntelligenceType;
use App\Filament\Resources\SiteResource\Pages;
use App\Filament\Resources\SiteResource\RelationManagers;
use App\Models\Site;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

class SiteResource extends Resource
{
    protected static ?string $model = Site::class;

    protected static ?string $navigationIcon = 'heroicon-o-rectangle-stack';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\TextInput::make('name')
                    ->required(),
                Forms\Components\TextInput::make('url')
                    ->required()
                    ->url(),
                Forms\Components\Select::make('provider')
                    ->live()
                    ->label('AI')
                    ->required()
                    ->options(ArtificialIntelligenceType::options()),
                Forms\Components\Select::make('model')
                    ->searchable()
                    ->options(fn (Forms\Get $get) => match ($get('provider')) {
                        ArtificialIntelligenceType::OPEN_AI() => openaiModels(),
                        default => [],
                    }),
                Forms\Components\Textarea::make('prompt')
                    ->required()
                    ->rows(10),
            ])
            ->columns(1);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('name'),
                Tables\Columns\TextColumn::make('url'),
                Tables\Columns\TextColumn::make('provider'),
                Tables\Columns\TextColumn::make('model'),
                Tables\Columns\TextColumn::make('created_at')
                    ->dateTime(),
            ])
            ->filters([
                //
            ])
            ->actions([
                Tables\Actions\EditAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getRelations(): array
    {
        return [
            RelationManagers\TokensRelationManager::class,
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListSites::route('/'),
            'edit' => Pages\EditSite::route('/{record}/edit'),
        ];
    }
}
