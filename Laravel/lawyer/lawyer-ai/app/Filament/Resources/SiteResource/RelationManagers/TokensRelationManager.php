<?php

namespace App\Filament\Resources\SiteResource\RelationManagers;

use Filament\Forms;
use Filament\Forms\Form;
use Filament\Notifications\Actions\Action;
use Filament\Notifications\Notification;
use Filament\Resources\RelationManagers\RelationManager;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Support\Carbon;

class TokensRelationManager extends RelationManager
{
    protected static string $relationship = 'tokens';

    public function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\TextInput::make('name')
                    ->required()
                    ->maxLength(255),
                Forms\Components\DatePicker::make('expires_at')
                    ->minDate(now()),
            ])
            ->columns(1);
    }

    public function table(Table $table): Table
    {
        return $table
            ->recordTitleAttribute('name')
            ->columns([
                Tables\Columns\TextColumn::make('name'),
                Tables\Columns\TextColumn::make('expires_at')
                    ->date(),
                Tables\Columns\TextColumn::make('created_at')
                    ->dateTime(),
            ])
            ->filters([
                //
            ])
            ->headerActions([
                Tables\Actions\CreateAction::make()
                    ->label('Create access token')
                    ->modalWidth('sm')
                    ->createAnother(false)
                    ->using(function (array $data) {
                        $expiredAt = null;
                        if ($data['expires_at']) {
                            $expiredAt = Carbon::create($data['expires_at']);
                        }

                        $token = $this->ownerRecord->createToken($data['name'], ['*'], $expiredAt);

                        Notification::make()
                            ->title('Access token created.')
                            ->body($token->plainTextToken)
                            ->duration(60*60)
                            ->actions([
                                Action::make('Copy')
                                    ->icon('heroicon-o-clipboard')
                                    ->extraAttributes([
                                        'x-data' => '',
                                        'x-on:click' => 'window.navigator.clipboard.writeText(`'.$token->plainTextToken.'`);'
                                            .'$tooltip(`'.__('Copied to clipboard').'`);',
                                    ])
                            ])
                            ->send();

                        return $token->accessToken;
                    }),
            ])
            ->actions([
                Tables\Actions\DeleteAction::make(),
            ])
            ->bulkActions([
            ]);
    }
}
