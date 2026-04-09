// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'Daily Facts';

  @override
  String get chooseCategory => 'Choose your category';

  @override
  String get showDetails => 'Show details';

  @override
  String get hideDetails => 'Hide details';

  @override
  String get unableToLoad => 'Unable to load content';

  @override
  String get retry => 'Retry';

  @override
  String newContentIn(String time) {
    return 'New content in $time';
  }

  @override
  String get categoryAnecdote => 'Anecdote';

  @override
  String get categoryChuckNorris => 'Chuck Norris';

  @override
  String get categoryAdvice => 'Advice';

  @override
  String get categoryHistory => 'History';

  @override
  String get categoryAnimals => 'Animals';

  @override
  String get categoryCountry => 'Countries';

  @override
  String get categoryExoplanet => 'Exoplanet';

  @override
  String get showAnecdote => 'Show anecdote';

  @override
  String get translate => 'Translate to French';

  @override
  String get tapToHide => 'Tap again to hide details';

  @override
  String get error => 'Error';

  @override
  String get translationError => 'Translation error';

  @override
  String get english => 'English';

  @override
  String get french => 'French';

  @override
  String get spanish => 'Spanish';
}
