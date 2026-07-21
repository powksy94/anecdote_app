import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:projet_app_annecdote/core/models/content_type.dart';
import 'package:projet_app_annecdote/features/favorites/models/favorite_fact.dart';
import 'package:projet_app_annecdote/features/favorites/widgets/favorite_card.dart';
import 'package:projet_app_annecdote/generated/app_localizations.dart';

Widget _wrap(Widget child) => MaterialApp(
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: Scaffold(body: child),
    );

void main() {
  final fact = FavoriteFact.create(ContentType.anecdote, 'Un fait marquant.');

  testWidgets('tapping the card triggers onTap', (tester) async {
    var tapped = false;
    await tester.pumpWidget(_wrap(FavoriteCard(
      fact: fact,
      onDelete: () {},
      onTap: () => tapped = true,
    )));

    await tester.tap(find.text('Un fait marquant.'));
    expect(tapped, isTrue);
  });

  testWidgets('tapping the delete icon triggers onDelete without triggering onTap',
      (tester) async {
    var deleted = false;
    var tapped = false;
    await tester.pumpWidget(_wrap(FavoriteCard(
      fact: fact,
      onDelete: () => deleted = true,
      onTap: () => tapped = true,
    )));

    await tester.tap(find.byIcon(Icons.bookmark_remove_rounded));
    expect(deleted, isTrue);
    expect(tapped, isFalse);
  });

  testWidgets('shows the name and a details preview when details exist',
      (tester) async {
    final withDetails = FavoriteFact.create(
      ContentType.dinosaur,
      'Tyrannosaurus Rex',
      details: 'Un des plus grands prédateurs terrestres ayant jamais existé.',
    );

    await tester.pumpWidget(_wrap(FavoriteCard(fact: withDetails, onDelete: () {})));

    expect(find.text('Tyrannosaurus Rex'), findsOneWidget);
    expect(
      find.text('Un des plus grands prédateurs terrestres ayant jamais existé.'),
      findsOneWidget,
    );
  });
}
