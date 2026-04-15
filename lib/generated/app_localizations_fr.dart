// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for French (`fr`).
class AppLocalizationsFr extends AppLocalizations {
  AppLocalizationsFr([String locale = 'fr']) : super(locale);

  @override
  String get appTitle => 'Faits du jour';

  @override
  String get chooseCategory => 'Choisissez votre catégorie';

  @override
  String get showDetails => 'Voir les détails';

  @override
  String get hideDetails => 'Masquer les détails';

  @override
  String get unableToLoad => 'Impossible de charger le contenu';

  @override
  String get retry => 'Réessayer';

  @override
  String newContentIn(String time) {
    return 'Nouveau contenu dans $time';
  }

  @override
  String get categoryAnecdote => 'Anecdote';

  @override
  String get categoryChuckNorris => 'Chuck Norris';

  @override
  String get categoryAdvice => 'Conseil';

  @override
  String get categoryHistory => 'Histoire';

  @override
  String get categoryAnimals => 'Animaux';

  @override
  String get categoryCountry => 'Pays';

  @override
  String get categoryExoplanet => 'Exoplanète';

  @override
  String get showAnecdote => 'Afficher l\'anecdote';

  @override
  String get translate => 'Traduire en français';

  @override
  String get tapToHide => 'Appuyez à nouveau pour cacher les détails';

  @override
  String get error => 'Erreur';

  @override
  String get translationError => 'Erreur de traduction';

  @override
  String get english => 'Anglais';

  @override
  String get french => 'Français';

  @override
  String get spanish => 'Espagnol';

  @override
  String get popMillion => 'M';

  @override
  String get popBillion => 'Md';
}
