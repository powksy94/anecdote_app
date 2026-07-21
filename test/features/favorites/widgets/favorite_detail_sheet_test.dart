import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:projet_app_annecdote/core/models/content_type.dart';
import 'package:projet_app_annecdote/features/favorites/models/favorite_fact.dart';
import 'package:projet_app_annecdote/features/favorites/widgets/favorite_detail_sheet.dart';
import 'package:projet_app_annecdote/generated/app_localizations.dart';

void main() {
  testWidgets('shows the full preview text and the category name', (tester) async {
    final fact = FavoriteFact.create(
      ContentType.anecdote,
      'Un fait complet, jamais tronqué, même sur plusieurs lignes de texte.',
    );

    await tester.pumpWidget(MaterialApp(
      locale: const Locale('fr'),
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: Scaffold(body: FavoriteDetailSheet(fact: fact)),
    ));
    await tester.pumpAndSettle();

    expect(
      find.text('Un fait complet, jamais tronqué, même sur plusieurs lignes de texte.'),
      findsOneWidget,
    );
    expect(find.text('Anecdote'), findsOneWidget);
  });

  testWidgets('shows both the name and the full details when details exist',
      (tester) async {
    final fact = FavoriteFact.create(
      ContentType.dinosaur,
      'Tyrannosaurus Rex',
      details: 'Un des plus grands prédateurs terrestres ayant jamais existé.',
    );

    await tester.pumpWidget(MaterialApp(
      locale: const Locale('fr'),
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: Scaffold(body: FavoriteDetailSheet(fact: fact)),
    ));
    await tester.pumpAndSettle();

    expect(find.text('Tyrannosaurus Rex'), findsOneWidget);
    expect(
      find.text('Un des plus grands prédateurs terrestres ayant jamais existé.'),
      findsOneWidget,
    );
  });
}
